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
                    <el-form :model="formData1">

                        <el-divider content-position="center">GIS 设置</el-divider>
                        <el-form-item label="路线粗细" >
                            <el-input v-model="formData1.lineBorderWeight" type="number" :min="1" @change="onLineBorderWeightChange" ></el-input>
                        </el-form-item>

                        <el-divider content-position="center">分仓选址</el-divider>
                            <el-tag>导入需求点和指定仓：</el-tag>
                            <el-upload
                                class="upload-demo"
                                ref="uploadWarehouseData"
                                action="http://127.0.0.1:5000/upload/warehouseData"
                                :auto-upload="false"
                                :on-success="handleuploadWarehouseDataSuccess"
                                :on-error="handleuploadWarehouseDataError">
                                <el-button type="primary" slot="trigger" size="small" >选取文件</el-button>
                                <el-button type="primary" style="margin-left: 10px;" size="small"  @click="submitUpload">上传到服务器</el-button>

                            </el-upload>

                            <el-form-item label="新建仓数量" prop="newWarehouseLocationNumber">
                                <el-input v-model="formData1.warehouseLocationNumber" type="number" :min="1" ></el-input>
                            </el-form-item>

                            <el-form-item label="是否指定仓">
                                <el-radio-group v-model="formData1.specWarehouse">
                                    <el-radio label="指定仓"></el-radio>
                                    <el-radio label="不指定仓"></el-radio>
                                </el-radio-group>
                            </el-form-item>

                            <el-dialog
                                title="提示"
                                :visible.sync="dialog2Visible"
                                width="30%"
                            >
                                <span>模型计算中，请等待</span>
                            </el-dialog>
                            <el-button type="primary" @click="submitForm('formData1')">开始计算</el-button>
                            <el-button type="primary" @click="submitgetTimeLimit">结果下载</el-button>
                    </el-form>

                </el-col>
            </el-row>
        </div>
    </div>
</template>

<script>

import { postWarehouseLocation } from "../api";

import axios from 'axios';
import AMapLoader from '@amap/amap-jsapi-loader';
export default {
  data() {
    return {
      echarts_data: [],

      dialog2Visible: false,

      map_list: [],

      formData1: {
        warehouseLocationNumber: 4,
        specWarehouse: '不指定仓',
        algori: '综合最优',
        needgetJingWeiDu: '需要',
        lineBorderWeight: 2

      }

    };
  },

  mounted() {
    this.echarts_data.forEach(item => {
      let temp = item.coords[0];
      item.coords[0] = item.coords[1];
      item.coords[1] = temp;
    });
    this.map_list = this.echarts_data;
    this.initAMap1();
  },
  methods: {
    onLineBorderWeightChange(value) {
      this.formData1.lineBorderWeight = value;
    },
    initAMap1() {
      var data = this.map_list;
      const that = this;

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
        var countyInfo = { 'name': '济南市', 'centerGeoCoord': [117.000923, 36.675807] };
        const colorList = ['#FF00FF', '#4B0082', '#FF0000', '#0000FF', '#006400', '#A36462', '#C96457', '#00C957', '#A52A2A', '#DC143C', '#082E54', '#D2B48C', '#00FFFF', '#292421', '#FFFF00'];
        var routes = {
          '济南仓': [[{ 'name': '济南仓', 'geoCoord': [117.2187, 36.65717] }, { 'name': 'BB60', 'geoCoord': [116.9677, 36.64082] }, { 'name': 'BB8A', 'geoCoord': [116.455335, 36.288724] }, { 'name': 'BB8B', 'geoCoord': [116.447678, 36.273443] }, { 'name': 'BB04', 'geoCoord': [117.0742, 36.64804] }, { 'name': 'BB43', 'geoCoord': [117.095027, 36.669696] }, { 'name': '济南仓', 'geoCoord': [117.2187, 36.65717] }]]
        };
        var opts = {
          subdistrict: 0,
          extensions: 'all',
          level: 'city'
        };
        var map = new AMap.Map('container', {
          resizeEnable: false,
          zoom: 5.5,
          center: countyInfo['centerGeoCoord']
        });

        let markers = [{
          name: '北京',
          position: [116.397428, 39.90923],
          fixed: true
        }, {
          name: '天津',
          position: [117.210813, 39.08],
          fixed: true
        }, {
          name: '石家庄',
          position: [114.51486, 38.042302],
          fixed: true
        }, {
          name: '太原',
          position: [112.548879, 37.87059],
          fixed: true
        }, {
          name: '呼和浩特',
          position: [111.749181, 40.842585],
          fixed: true
        }, {
          name: '沈阳',
          position: [123.431475, 41.805698],
          fixed: true
        }, {
          name: '长春',
          position: [125.323544, 43.817072],
          fixed: true
        }, {
          name: '哈尔滨',
          position: [126.534967, 45.803775],
          fixed: true
        }, {
          name: '上海',
          position: [121.472644, 31.231706],
          fixed: true
        }, {
          name: '南京',
          position: [118.767413, 32.046534],
          'fixed': true
        }, {
          name: '杭州',
          position: [120.15507, 30.274085],
          fixed: true
        }, {
          name: '合肥',
          position: [117.283042, 31.861184],
          fixed: true
        }, {
          name: '福州',
          position: [119.306239, 26.075302],
          fixed: true
        }, {
          name: '南昌',
          position: [115.892151, 28.689578],
          fixed: true
        }, {
          name: '济南',
          position: [117.120343, 36.651216],
          fixed: true
        }, {
          name: '郑州',
          position: [113.649644, 34.75661],
          fixed: true
        }, {
          name: '武汉',
          position: [114.298572, 30.584355],
          fixed: true
        }, {
          name: '长沙',
          position: [113.019455, 28.19409],
          fixed: true
        }, {
          name: '广州',
          position: [113.264435, 23.129163],
          fixed: true
        }, {
          name: '南宁',
          position: [108.327546, 22.815478],
          fixed: true
        }, {
          name: '海口',
          position: [110.33119, 20.031971],
          fixed: true
        }, {
          name: '成都',
          position: [104.066541, 30.572269],
          fixed: true
        }, {
          name: '贵阳',
          position: [106.713478, 26.578343],
          fixed: true
        }, {
          name: '昆明',
          position: [102.712251, 24.880095],
          fixed: true
        }, {
          name: '拉萨',
          position: [91.132212, 29.660361],
          fixed: true
        }, {
          name: '西安',
          position: [108.948024, 34.263161],
          fixed: true
        }, {
          name: '兰州',
          position: [103.823305, 36.061082],
          fixed: true
        }, {
          name: '西宁',
          position: [101.778916, 36.623178],
          fixed: true
        }, {
          name: '银川',
          position: [106.278179, 38.46637],
          fixed: true
        }, {
          name: '乌鲁木齐',
          position: [87.616848, 43.792818],
          fixed: true
        }, {
          name: '重庆',
          position: [106.551557, 29.56301],
          fixed: true
        }];

        markers.forEach(function (marker) {
          var contentStr = "<div class='".concat('marker_label').concat("'>").concat(marker.name).concat('</div>');

          new AMap.Marker({
            map: map,

            label: {
              content: contentStr
            },
            position: [marker.position[0], marker.position[1]],
            zooms: [2, 5]
          });
        });
        var sources = [];
        var demandPoints = [];

        for (var line in data) {
          var coord = data[line]['coords'][0];
          var point = data[line]['coords'][1];
          sources.push(coord);
          demandPoints.push(point);
        }

        var Icon = undefined;

        sources.forEach(function (source) {
          var contentStr = "<div class='".concat('marker_label').concat("'>").concat(parseFloat(source[0]).toFixed(2) + ',' + parseFloat(source[1]).toFixed(2)).concat('</div>');

          new AMap.Marker({
            map: map,
            icon: Icon,
            anchor: 'center',
            offset: new AMap.Pixel(0, 0),
            position: [source[0], source[1]],
            label: {
              content: contentStr
            }

          });
        });

        var PointIcon = undefined;
        demandPoints.forEach(function (source) {
          var contentStr = "<div class='".concat('marker_label').concat("'>").concat('</div>');

          new AMap.Marker({
            map: map,
            icon: PointIcon,
            anchor: 'center',
            offset: new AMap.Pixel(0, 0),
            position: [source[0], source[1]]
          });
        });

        for (var line in data) {
          var source = data[line]['coords'][0];
          var target = data[line]['coords'][1];
          var path = [new AMap.LngLat(source[0], source[1]), new AMap.LngLat(target[0], target[1])];

          var polyline = new AMap.Polyline({
            path: path,

            strokeColor: 'red',
            strokeWeight: this.formData1.lineBorderWeight,
            geodesic: true,
            height: 20
          });
          map.add(polyline);
        }

        that.map = map;
        this.map = map;
      }).catch(e => {});
    },

    async submitForm(formName) {
      this.dialog2Visible = true;
      let result = await postWarehouseLocation(this.formData1);
      if (result.status == 'success') {
        this.dialog2Visible = false;
        this.$message({
          type: 'success',
          message: '计算完成'
        });
      } else {
        this.dialog2Visible = false;
        this.$message({
          type: 'error',
          message: result.message
        });
      }

      this.map_list = result.map_list;
      this.initAMap1();
    },
    submitUpload() {
      this.$refs.uploadWarehouseData.submit();
    },
    handleuploadWarehouseDataSuccess(response, file, fileList) {
      alert("已成功上传到服务器");
      this.$refs.uploadWarehouseData.clearFiles();
    },
    handleuploadWarehouseDataError(err, file, fileList) {
      alert("上传失败");
    },

    async submitgetTimeLimit() {
      const url = 'http://127.0.0.1:5000/getTimeLimit';
      const config = {
        responseType: 'arraybuffer',
        headers: {}
      };
      axios.post(url, { user_id: '1' }, { responseType: 'arraybuffer' }).then(res => {
        try {
          var result = JSON.parse(res.headers.message_dict);

          const blobUrl = window.URL.createObjectURL(new Blob([res.data]));
          const a = document.createElement('a');
          a.style.display = 'none';
          a.download = result.filename;
          a.href = blobUrl;
          a.click();
          window.URL.revokeObjectURL(blobUrl);
          a.remove();
        } catch (e) {
          alert('保存文件出错');
        }
      });
    }
  }
};
</script>

<style scoped>
.home { width: 100%; height: 70vh; }
#container { width: 100%; height: 100%; }
</style>
