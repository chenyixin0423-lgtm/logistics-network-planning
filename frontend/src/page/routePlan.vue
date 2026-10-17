<template>
    <div class="mixin-components-container">
        <div class="content-container">

            <el-row  :gutter="20">

                <el-col span=18 style="background-color: white">
                    <div class="home">
                        <div id="container"></div>
                    </div>
                </el-col>

                <el-col span=6 style="background-color: #E9EEF3" >

                    <el-divider content-position="center">线路规划策略</el-divider>
                    <el-form :model="formdata1">
                        <el-upload
                            class="upload-demo"
                            ref="uploadRoutePlanData"
                            action="http://127.0.0.1:5000/upload/routePlanData"
                            :auto-upload="false"
                            :on-success="handleuploadWarehouseDataSuccess"
                            :on-error="handleuploadWarehouseDataError">
                            <el-button type="primary"  slot="trigger" size="small" >选取文件</el-button>
                            <el-button type="primary"  style="margin-left: 10px;" size="small"  @click="submitUpload">上传到服务器</el-button>

                        </el-upload>
                        <el-form-item label="取货or送货">
                            <el-radio-group v-model="formdata1.pickup_delivery">
                                <el-radio label="取货"></el-radio>
                                <el-radio label="送货"></el-radio>
                            </el-radio-group>
                        </el-form-item>

                        <el-form-item label="策略">
                            <el-radio-group v-model="formdata1.strategy" @change="getWaitingTimeInput">
                                <el-radio label="时间最短"></el-radio>
                                <el-radio label="不走高速"></el-radio>
                                <el-radio label="长期规划" ></el-radio>
                                <el-radio label="长途规划" ></el-radio>
                            </el-radio-group>
                        </el-form-item>
                        <el-form-item v-if="showInputBox" label="车辆在站点最长等待时间（小时）">
                            <el-input   v-model="formdata1.waiting_time"></el-input>
                        </el-form-item>
                        <el-form-item label="是否使用缓存文件">
                            <el-radio-group v-model="formdata1.use_cache_flag">
                                <el-radio label="是"></el-radio>
                                <el-radio label="否"></el-radio>
                            </el-radio-group>
                        </el-form-item>
                        <el-form-item label="计算时长上限（秒）">
                            <el-input v-model="formdata1.time_limit" type="number" :min="1" ></el-input>
                        </el-form-item>
                        <el-dialog
                            title="提示"
                            :visible.sync="dialog2Visible"
                            width="30%"
                        >
                            <span>模型计算中，请等待</span>
                        </el-dialog>
                        <el-button type="primary" size="small"  @click="submitForm">开始计算</el-button>
                        <el-button type="primary"  size="small" @click="getRoutePlanResultFile">结果下载</el-button>
                    </el-form>
                    <el-dialog
                        title="提示"
                        :visible.sync="getRoutePlanDiagVisible"
                        width="30%"
                    >
                        <span>计算错误, {{getRoutePlanMessage}}</span>
                    </el-dialog>

                    <el-divider content-position="center">线路规划结果展示</el-divider>
                        <div>
                        <el-button type="primary" size="small" style="margin-left: 10px;" @click="startAnimationButton">开始动画</el-button>
                        <el-button type="primary" size="small"  @click="pauseAnimationButton">暂停动画</el-button>
                        </div>

                </el-col>
            </el-row>

        </div>

    </div>
</template>

<script>

import AMapLoader from '@amap/amap-jsapi-loader';
import axios from 'axios';
export default {
  data() {
    return {
      showInputBox: false,
      getRoutePlanDiagVisible: false,
      getRoutePlanMessage: "",

      formdata1: {
        pickup_delivery: '取货',
        strategy: '时间最短',
        use_cache_flag: '否',
        time_limit: 5,
        waiting_time: 5

      },

      mapList: [],

      startAnimation: null,
      map: null,
      dialog2Visible: false

    };
  },

  mounted() {
    var countyInfo = [117.000923, 36.675807];

    this.initAMap(countyInfo);
  },
  methods: {
    submitUpload() {
      this.$refs.uploadRoutePlanData.submit();
    },
    getWaitingTimeInput(value) {
      if (value == "长途规划") {
        this.showInputBox = true;
      } else {
        this.showInputBox = false;
      }
    },
    handleuploadWarehouseDataSuccess(response, file, fileList) {
      alert("已成功上传到服务器");
      this.$refs.uploadRoutePlanData.clearFiles();
    },
    handleuploadWarehouseDataError(err, file, fileList) {
      alert("上传失败");
    },
    submitForm() {
      this.getRoutePlanResult(this.formdata1);
    },
    async getRoutePlanResult(data) {
      this.dialog2Visible = true;
      axios.post('http://127.0.0.1:5000/routeplan_result2', data).then(res => {
        var result = JSON.parse(res.headers.message_dict);
        this.dialog2Visible = false;
        if (result.status != "success") {
          this.getRoutePlanDiagVisible = true;
          this.getRoutePlanMessage = result.message;
        } else {
          this.initAMap(result.center_coord, result.routeplan);
        }
      });
    },

    async getRoutePlanResultFile() {
      axios.post('http://127.0.0.1:5000/download/routeplan_result', { user_id: '1' }, { responseType: 'arraybuffer' }).then(res => {
        try {
          var result = JSON.parse(res.headers.message_dict);

          const blobUrl = window.URL.createObjectURL(new Blob([res.data]));
          const a = document.createElement('a');
          a.style.display = 'none';
          a.download = result.filename;
          a.href = blobUrl;
          a.click();
          window.URL.revokeObjectURL(blobUrl);
        } catch (e) {
          alert('保存文件出错');
        }
      });
    },

    initAMap(countyInfo, routes) {
      const that = this;
      var strategy = this.formdata1.strategy;
      const dict = {
        "时间最短": 0,
        "不走高速": 1,
        "长期规划": 2,
        "长途规划": 0
      };
      var index_of_strategy = dict[strategy];

      AMapLoader.load({
        key: process.env.AMAP_JS_KEY,
        version: '2.1Beta',
        plugins: ['AMap.ToolBar', 'AMap.Driving', 'AMap.DistrictSearch'],
        AMapUI: {
          version: '1.1',
          plugins: []
        },
        Loca: {
          version: '2.0'
        }
      }).then(AMap => {
        const colorList = ['#FF00FF', '#4B0082', '#FF0000', '#0000FF', '#006400', '#A36462', '#C96457', '#00C957', '#A52A2A', '#DC143C', '#082E54', '#D2B48C', '#00FFFF', '#292421', '#FFFF00'];

        var opts = {
          subdistrict: 0,
          extensions: 'all',
          level: 'city'
        };
        var map = new AMap.Map('container', {
          resizeEnable: false,
          zoom: 12,
          center: countyInfo

        });
        that.map = map;

        AMap.plugin(['AMap.DistrictSearch', 'AMap.Driving', 'AMap.MoveAnimation'], function () {
          var district = new AMap.DistrictSearch(opts);
          district.search('济南市', function (status, result) {
            if (status = 'complete') {}

            var townCenterIcon = undefined;

            var villageIcon = undefined;

            var postalTruckIcon = undefined;

            var str = '经';

            var cumulatedIndices = 0;

            var driving = new AMap.Driving({
              map: map,
              hideMarkers: true,
              autoFitView: true,
              isOutline: false,
              policy: index_of_strategy,

              showTraffic: false
            });

            AMap.plugin('AMap.MoveAnimation', function () {
              var carMarkers = [];
              var lineArrs = [];
              var routeColorDict = {};
              var routeLineArrsDict = {};
              var routeCarMarkerIndexDict = {};

              for (var townCenter in routes) {
                var townRoutes = routes[townCenter];

                for (var j = 0; j < townRoutes.length; j++) {
                  var route = townRoutes[j];
                  var color = colorList[cumulatedIndices % colorList.length];
                  cumulatedIndices++;
                  str = "车" + cumulatedIndices + "_1经";
                  for (var k = 0; k < route.length; k++) {
                    if (k != route.length - 1) {
                      routeColorDict[route[k].geoCoord[0] + ', ' + route[k].geoCoord[1] + '_' + route[k + 1].geoCoord[0] + ', ' + route[k + 1].geoCoord[1]] = color;
                      routeCarMarkerIndexDict[route[k].geoCoord[0] + ', ' + route[k].geoCoord[1] + '_' + route[k + 1].geoCoord[0] + ', ' + route[k + 1].geoCoord[1]] = carMarkers.length;

                      driving.search(new AMap.LngLat(route[k].geoCoord[0], route[k].geoCoord[1]), new AMap.LngLat(route[k + 1].geoCoord[0], route[k + 1].geoCoord[1]), function (status, result) {
                        if (status === 'complete') {
                          var lineArr = [];
                          var driveRoutes = result.routes;
                          for (var l = 0; l < driveRoutes.length; l++) {
                            var steps = driveRoutes[l].steps;
                            for (var m = 0; m < steps.length; m++) {
                              if (l == 0 && m == 0) {
                                var stepStartPosition = steps[m].start_location;
                                lineArr.push([stepStartPosition.lng, stepStartPosition.lat]);
                              }

                              var stepPath = steps[m].path;
                              for (var n = 1; n < stepPath.length; n++) {
                                var pathPosition = stepPath[n];
                                lineArr.push([pathPosition.lng, pathPosition.lat]);
                              }
                            }
                          }

                          routeLineArrsDict[result.origin.lng + ', ' + result.origin.lat + '_' + result.destination.lng + ', ' + result.destination.lat] = lineArr;
                          color = routeColorDict[result.origin.lng + ', ' + result.origin.lat + '_' + result.destination.lng + ', ' + result.destination.lat];

                          var polyline = new AMap.Polyline({
                            map: map,
                            path: lineArr,
                            showDir: true,
                            strokeColor: color,
                            strokeWeight: 5 });
                        } else {
                          throw new Error("Map route lookup failed");
                        }
                      });

                      var labelStr = k == 0 ? townCenter : str.concat(k);
                      var labelClass = k == 0 ? 'townCenterInfo' : 'villageInfo';
                      var icon = k == 0 ? townCenterIcon : villageIcon;
                      var zIndex = k == 0 ? 9999 : 9999;

                      var marker = new AMap.Marker({
                        icon: icon,
                        position: route[k].geoCoord,
                        anchor: 'bottom-center',
                        zIndex: zIndex
                      });

                      marker.setMap(map);
                      if (k != 0) {
                        labelStr = route[k].name + ":" + labelStr;
                      }

                      var contentStr = "<div class='".concat(labelClass).concat("' style='color:").concat(color).concat("'>").concat(labelStr).concat('</div>');

                      marker.setLabel({
                        direction: 'right',
                        offset: new AMap.Pixel(0, 0),
                        content: contentStr });
                    }
                  }

                  var carMarker = new AMap.Marker({
                    map: map,
                    position: route[0].geoCoord,
                    icon: postalTruckIcon,
                    offset: new AMap.Pixel(-7, -13)
                  });

                  map.setFitView();

                  carMarkers.push(carMarker);
                  lineArrs.push([]);
                }
              }

              var isLineArrsReady = false;
              function startAnimation() {
                if (!isLineArrsReady) {
                  for (var townCenter in routes) {
                    var townRoutes = routes[townCenter];
                    for (var j = 0; j < townRoutes.length; j++) {
                      route = townRoutes[j];
                      for (var k = 0; k < route.length; k++) {
                        if (k != route.length - 1) {
                          var key = route[k].geoCoord[0] + ', ' + route[k].geoCoord[1] + '_' + route[k + 1].geoCoord[0] + ', ' + route[k + 1].geoCoord[1];
                          var lineArrsIndex = routeCarMarkerIndexDict[key];
                          var lineArr = routeLineArrsDict[key];
                          lineArrs[lineArrsIndex] = lineArrs[lineArrsIndex].concat(lineArr);
                        }
                      }
                    }
                  }
                  isLineArrsReady = true;
                }

                for (var i = 0; i < carMarkers.length; i++) {
                  carMarkers[i].moveAlong(lineArrs[i], {
                    duration: 1,
                    autoRotation: true,
                    circlable: true
                  });
                }
              };
              window.startAnimation = startAnimation;
              that.startAnimation = startAnimation;

              window.pauseAnimation = function () {
                for (var i = 0; i < carMarkers.length; i++) {
                  carMarker = carMarkers[i];
                  carMarker.pauseMove();
                }
              };

              window.resumeAnimation = function () {
                for (var i = 0; i < carMarkers.length; i++) {
                  carMarker = carMarkers[i];
                  carMarker.resumeMove();
                }
              };

              window.stopAnimation = function () {
                for (var i = 0; i < carMarkers.length; i++) {
                  carMarker = carMarkers[i];
                  carMarker.stopMove();
                }
              };
            });
          });
        });
        this.map = map;
      }).catch(e => {});
    },
    startAnimationButton() {
      window.startAnimation();
    },
    pauseAnimationButton() {
      window.pauseAnimation();
    }
  }
};
</script>

<style scoped>
.home { width: 100%; height: 70vh; }
#container { width: 100%; height: 100%; }
</style>
