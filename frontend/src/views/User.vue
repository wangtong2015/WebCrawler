<template>
    <div class="fill">
        <el-row style="margin-top: 1%">
            <el-col :span="6" :offset="1">
                <div class="fillW col center top">
                    <div style="border: 1px dashed gray; width: 100px; height: 100px">
                        <el-upload
                                action="/spider/upload/image/avatar/"
                                :show-file-list="false"
                                :on-success="handleAvatarSuccess"
                                :before-upload="beforeAvatarUpload">
                            <img v-if="user.avatarImg" :src="base_url + user.avatarImg" class="avatar">
                            <i v-else class="el-icon-plus avatar-uploader-icon"></i>
                        </el-upload>
                    </div>


                    <div class="pad"></div>

                    <div class="fillW row left">
                        <div class="label left">昵称</div>
                        <el-input placeholder="昵称" v-model="user.nickName"></el-input>
                    </div>

                    <div class="pad"></div>

                    <div class="fillW row left">
                        <div class="label left">签名</div>
                        <el-input placeholder="签名" v-model="user.sign"></el-input>
                    </div>

                    <div class="pad"></div>

                    <div class="fillW row left">
                        <div class="label left">学校</div>
                        <el-input placeholder="学校" v-model="user.school"></el-input>
                    </div>

                    <div class="pad"></div>

                    <div class="fillW row left">
                        <div class="label left">生日</div>
                        <el-date-picker
                                style="width: 100%"
                                v-model="user.birthday"
                                type="date"
                                placeholder="选择生日">
                        </el-date-picker>
                    </div>

                    <div class="pad"></div>

                    <div class="fillW row left">
                        <div class="label">
                            性别
                        </div>
                        <div style="margin-left: 10%">
                            <el-radio-group v-model="user.gender" size="small">
                                <el-radio-button label="秘密"></el-radio-button>
                                <el-radio-button label="女"></el-radio-button>
                                <el-radio-button label="男"></el-radio-button>
                            </el-radio-group>
                        </div>

                    </div>

                    <div class="fillW row center" style="margin-top: 30px">
                        <el-button type="primary" @click="addUser" :disabled="!canSubmit">添加用户<i class="el-icon-upload el-icon--right"></i></el-button>
                    </div>
                </div>
            </el-col>

            <el-col :span="13" :offset="3">
                <el-table
                        :data="robots"
                        style="width: 100%"

                        max-height="800">
                    <el-table-column
                            fixed
                            prop="userId"
                            label="ID"
                            width="80">
                    </el-table-column>
                    <el-table-column
                            prop="avatar"
                            label="头像"
                            width="100">
                        <!-- 图片的显示 -->
                        <template   slot-scope="scope">
                            <img :src="scope.row.avatar"  min-width="70" height="70" />
                        </template>
                    </el-table-column>
                    <el-table-column
                            prop="nickName"
                            label="昵称"
                            width="250">
                    </el-table-column>
                    <el-table-column
                            prop="gender"
                            label="性别"
                            :formatter="formatter"
                            width="80">
                    </el-table-column>
                    <el-table-column
                            prop="age"
                            label="年龄"
                            width="80">
                    </el-table-column>
                    <el-table-column
                            prop="mobileNum"
                            label="手机"
                            width="200">
                    </el-table-column>
                </el-table>
            </el-col>
        </el-row>

        <!--<div style="margin: 30px 0; text-align: center">-->
            <!--图片管理-->
        <!--</div>-->

        <!--<div class="fill row space-around top">-->

            <!--<el-upload-->
                    <!--action="https://jsonplaceholder.typicode.com/posts/"-->
                    <!--list-type="picture-card"-->
                    <!--:on-preview="handlePictureCardPreview"-->
                    <!--:on-remove="handleRemove">-->
                <!--<i class="el-icon-plus"></i>-->
                <!--<div slot="tip" class="el-upload__tip">-->

                <!--</div>-->
            <!--</el-upload>-->

        <!--</div>-->
        <!--<el-dialog :visible.sync="dialogVisible">-->
            <!--<img width="100%" :src="dialogImageUrl" alt="">-->
            <!--<div class="row space-around">-->
                <!--<el-button class="ml10" type="text" size="medium"-->
                           <!--v-clipboard:copy="dialogImageUrl">复制图片链接</el-button>-->
                <!--<el-button class="ml10" type="text" size="medium"-->
                           <!--@click="robot.avatarImg = dialogImageUrl">切换为头像</el-button>-->
            <!--</div>-->
        <!--</el-dialog>-->
    </div>
</template>

<script>
    export default {
        name: "User",
        data(){
            return{
                user: {
                    gender: "男",
                    avatarImg: "",
                    nickName: "一枝独秀",
                    birthday: Date.now() - 3600 * 24 * 1000 * 365 * 23,
                    sign: "好好学习，天天向上",
                    school: "清华大学"
                },
                base_url: '',
                dialogImageUrl: '',
                dialogVisible: false,
            }
        },
        computed:{
            robots: function () {
                return this.$store.state.robots;
            },
            canSubmit: function () {
                return this.user.avatarImg && this.user.nickName;
            }
        },
        methods: {
            addUser(){
                let user = this.$utils.copy(this.user);
                if(user.gender === '秘密'){
                    user.gender = 0;
                }else if(user.gender === '女'){
                    user.gender = 1;
                }else{
                    user.gender = 2;
                }
                user.birthday = this.$utils.timeFix(user.birthday);
                let that = this;
                this.$net.addUser(user).then((res)=>{
                    if(res.success === false){
                        that.$error('res.message');
                    }else{
                        that.$net.getRobots(100, true).then((robots) => {
                            that.$store.state.robots = robots;
                            // that.$forceUpdate()
                        })
                    }
                })
            },
            formatter(row, column, cellValue, index){
                if(cellValue===0){
                    return '秘密'
                }else if(cellValue===1){
                    return '女'
                }else{
                    return '男'
                }
            },
            handleRemove(file, fileList) {
                console.log(file, fileList);
            },
            handlePictureCardPreview(file) {
                this.dialogImageUrl = file.url;
                this.dialogVisible = true;
            },
            handleAvatarSuccess(res, file) {
                if(res.success === false){
                    this.$message.error(res.message);
                }else{
                    this.user.avatarImg = res.avatarImg;
                    if(res.base_url){
                        this.base_url = res.base_url;
                    }else{
                        this.base_url = '';
                    }
                }
            },
            beforeAvatarUpload(file) {
                const isJPG = file.type === 'image/jpeg' || file.type === 'image/png';
                const isLt2M = file.size / 1024 / 1024 < 2;

                if (!isJPG) {
                    this.$message.error('上传头像图片只能是 JPG 或 PNG 格式!');
                }
                if (!isLt2M) {
                    this.$message.error('上传头像图片大小不能超过 2MB!');
                }
                return isJPG && isLt2M;
            }
        }
    }
</script>

<style scoped>
    .avatar-uploader .el-upload {
        border: 2px solid gray;
        border-radius: 6px;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    .avatar-uploader .el-upload:hover {
        border-color: #409EFF;
    }

    .avatar-uploader-icon {
        font-size: 28px;
        color: #8c939d;
        width: 100px;
        height: 100px;
        line-height: 100px;
        text-align: center;
    }
    .avatar {
        width: 100px;
        height: 100px;
        display: block;
    }
</style>