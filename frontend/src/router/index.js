import Vue from 'vue'
import Router from 'vue-router'
import WarehouseLocation from '../page/warehouseLocation.vue'
import RoutePlan from '../page/routePlan.vue'

Vue.use(Router)

export default new Router({
  routes: [
    { path: '/', redirect: '/warehouseLocation' },
    { path: '/warehouseLocation', component: WarehouseLocation },
    { path: '/routePlan', component: RoutePlan }
  ]
})
