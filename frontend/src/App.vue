<template>
  <div class="container" v-if="$store.state.robots && $store.state.groups">
    <el-tabs v-model="active_pane" style="width: 100%; height: 100%">
      <el-tab-pane label="爬虫" name="Spider" style="width: 100%; height: 100%">
        <div class="fill"><Spider></Spider></div>
      </el-tab-pane>
      <el-tab-pane label="动态" name="Dynamic" style="width: 100%; height: 100%">
        <div class="fill"><Dynamic></Dynamic></div>
      </el-tab-pane>
      <el-tab-pane label="用户" name="User" style="width: 100%; height: 100%">
        <div class="fill"><User></User></div>
      </el-tab-pane>

      <el-tab-pane label="控制台" name="Config" style="width: 100%; height: 100%">
        <div class="fill"><Config></Config></div>
      </el-tab-pane>
    </el-tabs>
  </div>

</template>

<script>
  import Spider from './views/Spider'
  import Dynamic from './views/Dynamic'
  import Config from './views/Config'
  import User from './views/User'


  export default {
    components: {
      Spider: Spider,
      Dynamic: Dynamic,
      Config: Config,
      User: User
    },
    data() {
      return {
        active_pane: "Spider"
      }
    },
    computed :{
      // loading: {
      //   get: function () {
      //     return this.$store.state.loading
      //   },
      //   set: function (new_value) {
      //     this.$store.state.loading = new_value
      //   }
      // }
    },
    created(){
      let that = this;
      this.$net.getRobots().then((data)=>{
        that.$store.state.robots = data;
      });
      this.$net.getGroups().then((data) => {
        that.$store.state.groups = data;
      });
    },
    mounted(){

    }
  }
</script>
<style>
  @import "./assets/css/wt.css";

</style>
