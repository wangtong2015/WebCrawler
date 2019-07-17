import Vue from 'vue'
import Vuex from 'vuex'
import {isObjEmpty} from "./assets/js/utils";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    cookie: '',
    robots: [],
    groups: []
  },
  mutations: {
    changeCookie(state, cookie){
      state.cookie = cookie;
    },
    changeRobots(state, robots){
      state.robots = robots;
    }
  },
  actions: {
    changeCookie(context, cookie){
      context.commit("changeCookie", cookie);
    },
    changeRobots(context, robots){
      context.commit("changeRobots", robots);
    }
  }
})
