<template>
    <div class="fill">
        <div style="margin: 1% 0"></div>
        <div class="fill row left">
            <div class="label left">
                Cookie
            </div>
            <el-input v-model="cookie"
                      type="textarea"
                      :rows="3"
                      class="inline-block"
                      placeholder="Cookie">
            </el-input>
        </div>


    </div>
</template>

<script>
    export default {
        name: "Config",
        data(){
            return {

            }
        },

        computed: {
            cookie: {
                get: function () {
                    return this.$store.state.cookie;
                },
                set: function (new_cookie) {
                    this.$store.state.cookie = new_cookie;
                }
            }
        },

        mounted(){

        },
        methods:{

        }
    }
</script>

<style scoped>
    @import "../assets/css/wt.css";

</style>