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
                                :src="image.img"
                                alt="加载失败"
                                @click.native="show_toolbox(index)"
                                fit="fill">
                        </el-image>
                        <el-checkbox v-model="image.select"></el-checkbox>
                    </div>
                </div>
                <div class="fillW row center" style="margin-top: 1%">
                    <div class="col center">
                        <el-badge :value="packet.like_num">
                            <el-button @click="packet.like_num += 1">点赞</el-button>
                        </el-badge>
                        <div class="pad"></div>
                        <div class="row space-around">
                            <el-button type="primary"
                                       size="mini"
                                       @click="packet.like_num -= 1"
                                       icon="el-icon-minus" circle></el-button>
                            <el-button type="danger"
                                       size="mini"
                                       @click="packet.like_num = 0"
                                       icon="el-icon-refresh" circle></el-button>
                        </div>
                    </div>

                    <div style="width: 8%"></div>
                    <div class="col center">
                        <el-badge :value="packet.comment_num">
                            <el-button @click="packet.comment_num += 1">评论</el-button>
                        </el-badge>
                        <div class="pad"></div>
                        <div class="row space-around">
                            <el-button type="primary"
                                       size="mini"
                                       @click="packet.comment_num -= 1"
                                       icon="el-icon-minus" circle></el-button>
                            <el-button type="danger"
                                       size="mini"
                                       @click="packet.comment_num = 0"
                                       icon="el-icon-refresh" circle></el-button>
                        </div>
                    </div>
                    <div style="width: 8%"></div>

                    <div class="col center">
                        <el-badge :value="packet.repost_num">
                            <el-button @click="packet.repost_num += 1">转发</el-button>
                        </el-badge>
                        <div class="pad"></div>
                        <div class="row space-around">
                            <el-button type="primary"
                                       size="mini"
                                       @click="packet.repost_num -= 1"
                                       icon="el-icon-minus" circle></el-button>
                            <el-button type="danger"
                                       size="mini"
                                       @click="packet.repost_num = 0"
                                       icon="el-icon-refresh" circle></el-button>
                        </div>
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
                                       alt="头像"
                                       :src="comment.user.avatar"></el-avatar>

                            <div class="col left top fill">
                                <div class="row left middle" style="margin: 0 10px; width: 99%">
                                    <!--<el-tag type="info" style="margin-left: 1%">{{comment.user.value}}</el-tag>-->
                                    <el-autocomplete
                                            class="inline-input"
                                            v-model="comment.user.value"
                                            :fetch-suggestions="robotSearch"
                                            style="width: 20%"
                                            @select="select_robot($event, comment.user)"
                                            placeholder="用户">
                                    </el-autocomplete>

                                    <el-date-picker
                                            style="margin-left: 1%;"
                                            v-model="comment.addTime"
                                            align="right"
                                            type="datetime"
                                            placeholder="选择日期"
                                            :picker-options="date_picker_options">
                                    </el-date-picker>
                                </div>
                                <el-input type="textarea"
                                          style="margin: 10px; width: 99%"
                                          show-word-limit
                                          rows="2"
                                          resize="vertical"
                                          v-model="comment.commentContent"
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
                            <el-avatar class="pointer"
                                       shape="square"
                                       size="large"
                                       style="margin-right: 1%"
                                       alt="头像"
                                       :src="packet.user.avatar"></el-avatar>

                            <el-autocomplete
                                    v-model="packet.user.value"
                                    :fetch-suggestions="robotSearch"
                                    style="width: 100%"
                                    @select="select_robot($event, packet.user)"
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
                                    v-model="packet.addTime"
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
                   width="840px"
                   :visible.sync="toolbox_show">
            <el-carousel :autoplay="false"
                         indicator-position="outside"
                         height="670px"
                         id="carousel"
                         ref="carousel"
                         style="width: 800px;"
                         :initial-index="image_index"
                         arrow="hover">

                <el-carousel-item v-for="(image, index) in images"
                                  class="fill col center middle"
                                  style="text-align: center;"
                                  :key="index">
                    <div style="width: 800px; height: 600px;">
                        <div class="cropbox" :style="crop_style(image)"></div>
                        <img :src="image.img"
                             alt="加载失败"
                             style="object-fit: fill;width: 800px; height: 600px; position: absolute; left: 0; top: 0; z-index: 4"/>
                    </div>
                    <div class="row space-around middle" style="margin-top: 2%">
                        <el-input-number v-model="image.crop[0]" controls-position="right" :min="0" :max="100"></el-input-number>
                        <el-input-number v-model="image.crop[1]" controls-position="right" :min="0" :max="100"></el-input-number>
                        <el-input-number v-model="image.crop[2]" controls-position="right" :min="0" :max="100"></el-input-number>
                        <el-input-number v-model="image.crop[3]" controls-position="right" :min="0" :max="100"></el-input-number>
                    </div>
                </el-carousel-item>
            </el-carousel>
        </el-dialog>

    </div>
</template>

<script>
    const imageWidth = 800;
    const imageHeight = 600;

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
                if(packets.length > this.progress){
                    return packets[this.progress];
                }else{
                    return {
                        select: false,
                        user: {},
                        sent_time: Date.now(),
                        content: "",
                        images: [],
                        comments: [],
                        groups: []
                    }
                }
            },
            images: function () {
                return this.packet.imageList;
            },
            groups: function () {
                return this.packet.groups;
            },
            comments: function () {
                return this.packet.commentsList;
            }
        },
        created(){

        },
        mounted(){
            let that = this;
            // that.search();
        },
        methods: {
            changeSelect(obj){
                obj.select = !obj.select;
                this.$forceUpdate()
            },
            robotSearch(robot_name, cb){
                let robots = this.$store.state.robots;
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
                let loading = this.$loading({
                    lock: true,
                    text: '爬取数据中',
                    spinner: 'el-icon-loading',
                    background: 'rgba(0, 0, 0, 0.7)'
                });

                this.$net.search(
                    this.page,
                    this.username,
                    this.keyword,
                    this.topic,
                    this.like_num,
                    this.comment_num,
                    this.$store.state.cookie
                ).then((packets)=>{
                    that.packets = packets;
                    that.progress = 0;
                    that.$forceUpdate();
                    loading.close();
                    that.$message({
                        showClose: true,
                        message: "操作成功",
                        type: 'success'
                    });
                }).catch((message)=>{
                    loading.close();
                    that.$message({
                        showClose: true,
                        message: message,
                        type: 'error'
                    });
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
                let that = this;
                if(this.progress >= this.packets.length - 1){
                    this.$net.confirm(this.packets, this.$store.state.cookie).then((data)=>{
                        that.$message({
                            showClose: true,
                            message: "操作成功",
                            type: 'success'
                        });
                    }).catch((message)=>{
                        that.$message({
                            showClose: true,
                            message: message,
                            type: 'error'
                        });
                    });
                    this.page += 1;
                    this.search();
                }else{
                    this.progress += 1;
                    if(this.packets[this.progress].sent_time < Date.now()){
                        this.packets[this.progress].sent_time = Date.now();
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
                let width = 796;
                let height = 596;
                let xL = image.crop[0] / 100;
                let yL = image.crop[1] / 100;
                let xR = image.crop[2] / 100;
                let yR = image.crop[3] / 100;
                let l = xL * width;
                let t = yL * height;
                let w = (xR - xL) * width;
                let h = (yR - yL) * height;
                // return {
                //   width: '100%',
                //   height: '100%'
                // }
                return {
                    left: l + 'px',
                    top: t + 'px',
                    width: w + 'px',
                    height: h + 'px'
                }
            },
            select_robot(robot, user){
                user.uid = robot.uid;
                user.avatar = robot.avatar;
                user.gender = robot.gender;
                user.userId = robot.userId;
                user.nickName = robot.nickName;
                user.age = robot.age;
                user.value = robot.value;
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
        overflow: hidden;
        border: 2px solid red;
        z-index: 10;
        position: absolute;
    }

    .preview{
        object-fit: fill;
        width: 800px;
        height: 600px;
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



</style>
