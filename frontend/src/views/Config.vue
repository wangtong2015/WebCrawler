<template>
    <div class="fill">
        <div class="fill row left">
            <div class="label left">
                Cookie
            </div>
            <el-input v-model="cookie"
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
                    return this.$store.state.cookie
                },
                set: function (newvalue) {
                    this.$store.state.cookie = newvalue;
                }
            }
        },
        methods:{

        }
    }
</script>

<style scoped>
    @import "../assets/css/wt.css";
</style>