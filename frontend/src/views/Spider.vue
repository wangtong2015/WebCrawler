<template>
    <div id="app" class="fill col center top">
        <div class="header">
            <div class="fill">
                <el-row :gutter="4" class="fill">
                    <el-col :span="3">
                        <div class="fill row left">
                            <div class="label left">
                                用户名
                            </div>
                            <el-input v-model="username"
                                      class="inline-block"
                                      placeholder="用户名">
                            </el-input>
                        </div>
                    </el-col>
                    <el-col :span="5">
                        <div class="fill row left">
                            <div class="label left">
                                关键词
                            </div>
                            <el-input v-model="keyword"
                                      placeholder="关键词">
                            </el-input>
                        </div>

                    </el-col>
                    <el-col :span="4">
                        <div class="fill row left">
                            <div class="label left">
                                主题
                            </div>
                            <el-input v-model="topic"
                                      placeholder="主题">
                            </el-input>
                        </div>
                    </el-col>
                    <el-col :span="3">
                        <div class="fill row left">
                            <div class="label left">
                                点赞数
                            </div>
                            <el-input-number v-model="like_num"
                                             controls-position="right"
                                             :min="0"
                                             :max="100">
                            </el-input-number>
                        </div>
                    </el-col>
                    <el-col :span="3">
                        <div class="fill row left">
                            <div class="label left">
                                评论数
                            </div>
                            <el-input-number v-model="comment_num"
                                             controls-position="right"
                                             :min="0"
                                             :max="100">
                            </el-input-number>
                        </div>
                    </el-col>
                    <el-col :span="3">
                        <div class="fill row left">
                            <div class="label left">
                                页数
                            </div>
                            <el-input-number v-model="page"
                                             controls-position="right"
                                             :min="1"
                                             :max="100">
                            </el-input-number>
                        </div>
                    </el-col>
                    <el-col :span="3">
                        <el-button type="primary"
                                   @click="search"
                                   class="fillW">开始抓取</el-button>
                    </el-col>
                </el-row>
            </div>
        </div>
        <div class="main" style="margin: 0;">
            <div class="fill col center top">
                <el-input type="textarea"
                          show-word-limit
                          rows="6"
                          resize="vertical"
                          v-model="packet.content" placeholder="内容"></el-input>
                <div class="fill row center">
                    <div v-for="(image, index) in images" class="col center" style="margin: 2%">
                        <el-image
                                style="width: 130px; height: 130px; cursor:pointer;"
                                :src="image.url"
                                @click.native="show_toolbox(index)"
                                fit="fill">
                        </el-image>
                        <el-checkbox v-model="image.select"></el-checkbox>
                    </div>
                </div>
                <div class="fill row center">
                    <div v-for="group in groups" style="margin:1% 2%;">
                        <div v-if="group.select"
                             class="pointer group topic select"
                             :key="group.name"
                             @click="changeSelect(group)">
                            {{ group.name }}
                        </div>
                        <div v-else
                             :key="group.name"
                             class="pointer group topic"
                             @click="changeSelect(group)">
                            {{ group.name }}
                        </div>
                    </div>
                </div>
                <div class="fill col center">
                    <div v-for="comment in comments" class="fillW col top center">
                        <div class="fillW row left middle" style="margin-top: 1%">
                            <el-checkbox v-model="comment.select"></el-checkbox>
                            <el-avatar class="pointer"
                                       shape="square"
                                       size="large"
                                       @click.native="changeSelect(comment)"
                                       :src="comment.user.avatar"></el-avatar>

                            <div class="col left top fill">
                                <el-tag type="info" size="mini" style="margin-left: 0.56%">{{comment.user.value}}</el-tag>
                                <el-input type="textarea"
                                          style="margin: 10px; width: 99%"
                                          show-word-limit
                                          rows="2"
                                          resize="vertical"
                                          v-model="comment.content"
                                          placeholder="评论">
                                </el-input>
                            </div>
                        </div>
                        <div class="line"></div>
                    </div>
                    <a :href="packet.weibo_url" target="_blank" class="pointer">{{packet.weibo_url}}</a>
                </div>
            </div>
            <div style="height: 100px"></div>
        </div>
        <div class="footer">
            <div class="fill">
                <el-row :gutter="20"
                        type="flex"
                        align="middle"
                        justify="space-around">

                    <el-col :span="1">
                        {{progress}}/{{packets.length}}
                    </el-col>

                    <el-col :span="3">
                        <div class="fill col center middle" style="text-align: center; vertical-align: center">
                            <el-switch
                                    style="width: 100%; height: 100%; margin: auto"
                                    v-model="packet.select"
                                    active-text="选择"
                                    inactive-text="不选择">
                            </el-switch>
                        </div>
                    </el-col>

                    <el-col :span="3">
                        <el-button type="primary"
                                   @click="previous"
                                   :disabled="progress <= 0 || packets.length <= 0"
                                   class="fillW">上一条</el-button>
                    </el-col>

                    <el-col :span="3">
                        <el-button v-if="progress === packets.length - 1"
                                   type="danger"
                                   @click="confirm"
                                   :disabled="packets.length <= 0"
                                   class="fillW">提交</el-button>
                        <el-button v-else
                                   type="primary"
                                   @click="confirm"
                                   :disabled="packets.length <= 0"
                                   class="fillW">确认</el-button>
                    </el-col>

                    <el-col :span="3">
                        <el-button v-if="progress >= packets.length - 1"
                                   type="danger"
                                   @click="skip"
                                   :disabled="packets.length <= 0"
                                   class="fillW">跳过并提交</el-button>
                        <el-button v-else
                                   type="primary"
                                   @click="skip"
                                   :disabled="packets.length <= 0"
                                   class="fillW">跳过</el-button>
                    </el-col>

                    <el-col :span="5">
                        <div class="fill row left">
                            <div class="label left">
                                马甲号
                            </div>
                            <el-autocomplete
                                    class="inline-input"
                                    v-model="packet.robot.value"
                                    :fetch-suggestions="robotSearch"
                                    style="width: 100%"
                                    placeholder="马甲号">
                            </el-autocomplete>
                        </div>
                    </el-col>

                    <el-col :span="4">
                        <div class="fill row left">
                            <div class="label left">
                                发送时间
                            </div>
                            <el-date-picker
                                    v-model="packet.sent_time"
                                    align="right"
                                    type="datetime"
                                    placeholder="选择日期"
                                    :picker-options="date_picker_options">
                            </el-date-picker>
                        </div>
                    </el-col>

                </el-row>
            </div>
        </div>

        <el-dialog title="图片预览"
                   width="80%"
                   :visible.sync="toolbox_show">
            <el-carousel :autoplay="false"
                         indicator-position="outside"
                         height="800px"
                         id="carousel"
                         ref="carousel"
                         :initial-index="image_index"
                         arrow="hover">
                <el-carousel-item v-for="(image, index) in images"
                                  class="fill row center middle"
                                  style="text-align: center; "
                                  :key="index">
                    <div style="width: 100%; height: 100%; ">
                        <div style="width: 90%; height: 90%; padding: 0;margin:0 auto; ">
                            <div class="cropbox" :style="crop_style(image)">

                            </div>
                            <img :src="image.url" class="preview"/>
                        </div>
                        <div class="row space-around middle" style="margin-top: 2%">
                            <el-input-number v-model="image.crop[0]" controls-position="right" :min="0" :max="100"></el-input-number>
                            <el-input-number v-model="image.crop[1]" controls-position="right" :min="0" :max="100"></el-input-number>
                            <el-input-number v-model="image.crop[2]" controls-position="right" :min="0" :max="100"></el-input-number>
                            <el-input-number v-model="image.crop[3]" controls-position="right" :min="0" :max="100"></el-input-number>
                        </div>
                    </div>
                </el-carousel-item>
            </el-carousel>

        </el-dialog>

    </div>
</template>

<script>

    export default {
        name: 'Spider',
        data() {
            return {
                page: 1,
                progress: 0,
                username: '',
                keyword: '你好',
                topic: '',
                like_num: 0,
                comment_num: 0,
                sent_time: (function () {
                    return Date.now();
                })(),
                packets: [],
                preset_robots: [],
                date_picker_options: {
                    disabledDate(time) {
                        let now = new Date();
                        if(time.getTime() < now.getTime()){
                            return time.getDate() !== now.getDate();
                        }else{
                            return false;
                        }
                    },
                    shortcuts: [{
                        text: '一小时后',
                        onClick(picker) {
                            const date = new Date();
                            picker.$emit('pick', date.getTime() + 3600 * 1000);
                        }
                    },
                        {
                            text: '两小时后',
                            onClick(picker) {
                                const date = new Date();
                                picker.$emit('pick', date.getTime() + 3600 * 1000 * 2);
                            }
                        },
                        {
                            text: '半天后',
                            onClick(picker) {
                                const date = new Date();
                                picker.$emit('pick', date.getTime() + 3600 * 1000 * 12);
                            }
                        },
                        {
                            text: '明天',
                            onClick(picker) {
                                const date = new Date();
                                date.setTime(date.getTime() + 3600 * 1000 * 24);
                                picker.$emit('pick', date);
                            }
                        }, {
                            text: '下周',
                            onClick(picker) {
                                const date = new Date();
                                date.setTime(date.getTime() + 3600 * 1000 * 24 * 7);
                                picker.$emit('pick', date);
                            }
                        }]
                },
                toolbox_show: false,
                image_index: 0
            }
        },
        computed :{
            packet: function(){
                let packets = this.packets;
                let progress = this.progress;
                if(packets.length > progress){
                    return packets[progress];
                }else{
                    return {
                        select: false,
                        robot: "",
                        sent_time: Date.now(),
                        content: "",
                        images: [],
                        comments: [],
                        groups: []
                    }
                }
            },
            images: function () {
                return this.packet.images;
            },
            groups: function () {
                return this.packet.groups;
            },
            comments: function () {
                return this.packet.comments;
            }
        },
        created(){

        },
        mounted(){
            let that = this;
            this.$net.getRobots().then((data)=>{
                that.preset_robots = data;
                that.search();
            });
        },
        methods: {
            changeSelect(obj){
                obj.select = !obj.select;
                this.$forceUpdate()
            },
            robotSearch(robot_name, cb){
                let robots = this.preset_robots;
                let result = robot_name ? robots.filter(this.robotFilter(robot_name)) : robots;
                // 调用 callback 返回建议列表的数据
                cb(result);
            },
            robotFilter(robot_name){
                return (robot)=>{
                    return (robot.value.toLowerCase().indexOf(robot_name.toLowerCase()) !== -1);
                }
            },
            search(){
                let that = this;
                this.$net.search(
                    this.page,
                    this.username,
                    this.keyword,
                    this.topic,
                    this.like_num,
                    this.comment_num).then((packets)=>{
                    that.packets = packets;
                    that.progress = 0;
                    that.$forceUpdate();
                })
            },
            previous(){
                if(this.progress > 0){
                    this.progress -= 1;
                }
            },
            confirm(){
                this.packets[this.progress].select = true;
                this.next();
            },
            skip(){
                this.packets[this.progress].select = false;
                this.next();
            },
            next(){
                if(this.progress >= this.packets.length - 1){
                    this.$net.confirm(this.packets);
                    this.page += 1;
                    this.search();
                }else{
                    this.progress += 1;
                    if(this.packets[progress].sent_time < Date.now()){
                        this.packets[progress].sent_time = Date.now();
                    }
                }
            },
            show_toolbox(index){
                this.image_index = index;
                if(this.$refs.carousel){
                    this.$refs.carousel.setActiveItem(index);
                }
                this.toolbox_show = true;
            },
            crop_style: function (image) {
                let xL = image.crop[0];
                let yL = image.crop[1];
                let xR = image.crop[2];
                let yR = image.crop[3];
                let x = xL + '%';
                let y = yL + '%';
                let w = (xR - xL) * 0.99 + '%';
                let h = (yR - yL) * 0.91 + '%';
                // return {
                //   width: '100%',
                //   height: '100%'
                // }
                return {
                    left: x,
                    top: y,
                    width: w,
                    height: h
                }
            }
        }
    }
</script>
<style>
    @import "../assets/css/wt.css";
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

    .header{
        width: 100%;
        height: 5%;
        top: 0;
    }

    .main{
        overflow-y:scroll;
        width: 100%;
        height: 80%;

    }

    .footer{
        position: fixed;
        width: 100%;
        height: 5%;
        bottom: 0;
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
