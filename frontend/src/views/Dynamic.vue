<template>
    <div id="app" class="fill col center top">
        <div class="header">
            <div class="fillW row left">
                <el-select v-model="spider_url.base" placeholder="请选择">
                    <el-option
                            v-for="item in spider_url_options"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value">
                    </el-option>
                </el-select>
                <el-input type="text"
                          resize="vertical"
                          v-model="spider_url.url" placeholder="链接（注意是具体内容的链接）"></el-input>
                <el-button type="primary"
                @click="crawl"
                :disabled="spider_url.url.length > 0"
                style="width: 10%"
                >爬取</el-button>
            </div>
        </div>
        <div class="main" style="margin: 0;">
            <div class="fill col center top">
                <el-input type="textarea"
                          rows="6"
                          resize="vertical"
                          v-model="packet.content" placeholder="内容"></el-input>
                <div class="fillW row center" style="margin-top: 1%">
                    <el-upload
                            action="https://jsonplaceholder.typicode.com/posts/"
                            list-type="picture-card"
                            show-file-list="true"
                            :file-list="imageList"
                            :on-preview="handlePictureCardPreview"
                            :on-remove="handleRemove">
                        <i class="el-icon-plus"></i>
                    </el-upload>
                </div>
                <div class="fill row center">
                    <div v-for="group in packet.groups" style="margin:1% 2%;">
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
                    <div v-for="comment in packet.commentsList" class="fillW col top center">
                        <div class="fillW row left middle" style="margin-top: 1%">
                            <el-checkbox v-model="comment.select"></el-checkbox>
                            <el-avatar class="pointer"
                                       shape="square"
                                       size="large"
                                       @click.native="changeSelect(comment)"
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
                </div>
            </div>
        </div>


        <el-dialog :visible.sync="dialogVisible">
            <img width="100%" :src="dialogImageUrl" alt="">
        </el-dialog>


    </div>
</template>

<script>
    const imageWidth = 800;
    const imageHeight = 600;
    import source from 'emoji-convert-resource-base';
    import convert from 'emoji-convert';
    convert.extend(source);

    export default {
        name: 'Dynamic',
        data() {
            return {
                spider_url: {
                    base: "m.weibo.cn",
                    url: ""
                },
                spider_url_options: [
                    {value: 'weibo.cn', label: 'weibo.cn'},
                    {value: 'm.weibo.cn', label: 'm.weibo.cn'}
                ],
                packet: {
                    content: this.$convert.toUnicode("[大笑]"),
                    addTime: Date.now() + 10000,
                    user: {
                        avatar: "",
                        gender: 0,
                        userId: 0,
                        nickName: "",
                        value: ""
                    },
                    imageList: [{
                        name: "food.jpeg",
                        url: 'https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100'
                    }],
                    commentsList:[{
                        user: {
                            avatar: "",
                            gender: 0,
                            userId: 0,
                            nickName: "",
                            value: ""
                        },
                        commentContent: "",
                        addTime: Date.now() + 100000
                    }]
                },
                toolbox_show: false,


                // dialog
                dialogImageUrl: "",
                dialogVisible: false,


                image_index: 0,
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
                }
            }
        },
        computed :{

        },
        created(){

        },
        mounted(){
            let that = this;
            this.$net.getGroups().then((group)=>{
                that.packet.groups = group;
            })
        },
        methods: {
            crawl(event){

            },
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
            submit(){
                let that = this;
                // let packet = this.packet.map(function (value) {
                //     // return {
                //     //     content:
                //     // }
                // });
                // this.$net.confirm([this.packet], this.$store.state.cookie).then((data)=>{
                //     that.$message({
                //         showClose: true,
                //         message: "操作成功",
                //         type: 'success'
                //     });
                // }).catch((message)=>{
                //     that.$message({
                //         showClose: true,
                //         message: message,
                //         type: 'error'
                //     });
                // });
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