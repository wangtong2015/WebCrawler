<template>
  <div class="container">
    <el-tabs v-model="active_pane" style="width: 100%; height: 100%">
      <el-tab-pane label="Spider" name="Spider" style="width: 100%; height: 100%">
        <div class="fill"><Spider></Spider></div>
      </el-tab-pane>
      <el-tab-pane label="Config" name="Config" style="width: 100%; height: 100%">
        <div class="fill"><Config></Config></div>
      </el-tab-pane>
    </el-tabs>
  </div>

</template>

<script>
  import Spider from './views/Spider'
  import Config from './views/Config'

  export default {
    components: {
      Spider: Spider,
      Config: Config
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

    },
    mounted(){

    }
  }
</script>
<style>
  @import "./assets/css/wt.css";
  #app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    width: 100%;
    height: 100%;
  }

  .group{
    min-width: 4em;
    padding: 0.2%;
    border-radius: 4px;
  }

  .group.name{
    background-color: #f8edd2;
  }
  .group.topic{
    background-color: lightgray;
  }
  .group.topic.select{
    background-color: #ffb3da;
  }

  /*#toolbox{*/
    /*z-index: 10;*/
    /*position: fixed;*/
    /*margin: auto;*/
    /*top: 10%;*/
    /*width: 80%;*/
    /*height: 80%;*/
    /*background-color: gray;*/
  /*}*/


  .cropbox{
    border: 2px solid red;
    z-index: 20;
    overflow: hidden;
    padding: 0;
    position: absolute;
  }

  .preview{
    object-fit: fill;
    position: absolute;
    left: 0;
    top: 0;
    width: 99.1%;
    height: 91.2%;
  }
  .img_fill{
    object-fit: fill;
  }
  .img_contain{
    object-fit: contain;
  }

  .label{
    /*width: 1px;*/
    text-align:center;
    vertical-align: middle;
    border: 1px solid #DCDFE6;
    background-color: #F5F7FA;
    margin: 0;
    border-radius: 4px 0 0 4px;
    white-space: nowrap;
    padding:0 10px;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
  }

  .label.left{
    border-right:none;
  }

</style>
