import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import ElementUI from 'element-ui' //element-ui的全部组件
import 'element-ui/lib/theme-chalk/index.css'//element-ui的css
import * as net from './assets/js/net'
import * as utils from './assets/js/utils'
import { Loading } from 'element-ui';


Vue.prototype.$net = net;
Vue.prototype.$utils = utils;

Vue.use(ElementUI); //使用elementUI
Vue.use(Loading);
Vue.config.productionTip = false;

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app');
