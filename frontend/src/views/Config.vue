<template>
    <div class="fill">
        <el-form ref="form" :model="config" label-width="80px" size="mini">
            <el-form-item label="Cookie">
                <el-input v-model="config.cookie"></el-input>
            </el-form-item>

            <el-form-item size="large">
                <el-button type="primary" @click="submit">提交</el-button>
            </el-form-item>
        </el-form>
    </div>
</template>

<script>
    export default {
        name: "Config",
        data(){
            return {
                config: {
                    cookie: "_T_WM=69123916494; ALF=1565588631; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5QEWjyIX6.D_oANg-g_4xg5JpX5K-hUgL.FoMp1hqNS0nN1Kn2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMNeKncS0MRS0.R; SCF=AgSbdYVSHluSlWBFhJ9RgknGZ7KLyz1jSCifFGi8I_Dilc0sBwzrArQa35ap__rV0hEJeQm4SscjljzsuVBbjqQ.; SUB=_2A25wLQFdDeRhGeFP41QW9ybLwjSIHXVT0a8VrDV6PUJbktBeLWbGkW1NQRZCWASaXclenfSaSZz-YXqhiphYyaET; SUHB=0qjk3ElI68Zhi_"
                }
            }
        },
        methods:{
            submit: function (event) {

            }
        }
    }
</script>

<style scoped>

</style>