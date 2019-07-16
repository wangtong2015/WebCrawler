import Vue from 'vue'
import Router from 'vue-router'
import Spider from './views/Spider'
import Config from './views/Config'

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'spider',
      component: Spider
    },
    {
      path: '/config',
      name: 'config',
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: Config
    }
  ]
})
