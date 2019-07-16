import axios from 'axios'
import * as utils from './utils'
const baseURL = '/spider';
let GROUPS = [];
let ROBOTS = [];
let Cookie = "_T_WM=69123916494; ALF=1565588631; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5QEWjyIX6.D_oANg-g_4xg5JpX5K-hUgL.FoMp1hqNS0nN1Kn2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMNeKncS0MRS0.R; SCF=AgSbdYVSHluSlWBFhJ9RgknGZ7KLyz1jSCifFGi8I_Dilc0sBwzrArQa35ap__rV0hEJeQm4SscjljzsuVBbjqQ.; SUB=_2A25wLQFdDeRhGeFP41QW9ybLwjSIHXVT0a8VrDV6PUJbktBeLWbGkW1NQRZCWASaXclenfSaSZz-YXqhiphYyaET; SUHB=0qjk3ElI68Zhi_";

ROBOTS = ROBOTS.map(function (robot) {
    let gender = "";
    if(robot.gender === 1){
        gender = " 👩";
    }else if(robot.gender === 2){
        gender = " 👨";
    }
    return {
        "uid": robot.uid,
        "avatar": robot.avatar,
        "gender": robot.gender,
        "userId": robot.userId,
        "nickName": robot.nickName,
        "age": 8,
        "value": robot.nickName + '#' + robot.userId + gender
    }
});
// const PACKETS = [{"weibo_url": "https://weibo.com/5498972025/HDJA10Nx8", "like_num": 115666, "repost_num": 85815, "comment_num": 31985, "images": [], "content": "【RNG战队英雄联盟分部人员变动公告】 即日起，RNG-Mlxg（刘世宇）正式退役。 从2015年加入RNG至今，刘世宇以RNG队长的身份与RNG相伴成长，并以他独特的打野方式与凶悍的进攻风格为人所称道，在役期间带领队伍收获诸多赛场荣誉与宝贵的团队回忆。 由于身体原因，2019年LPL春季赛前香锅暂离赛场进行休养，而在调养身体的过程中，俱乐部充分尊重选手的个人意愿，香锅也在深思熟虑和积极沟通后，正式向俱乐部提出了退役的决定。退役后，刘世宇依然还是RNG大家庭中不可或缺的一份子，下一步俱乐部将与刘世宇共同探讨退役后的发展道路，并为他创造更多的可能性。 感谢Gank Machine在峡谷里给大家带来的点滴回忆，我们会记住你义无反顾的“香锅式”gank，记住一起度过的那些有笑有泪的日子。 过去的这些年，遇见你很高兴。接下来的岁月，就让我们陪你在人生的赛场继续驰骋，继续闪耀，陪你尝试那些不曾体验的事情，陪你探索一个全新的世界。 辛苦了，RNG-Mlxg，你好，RNG-刘世宇，天高海阔，后会有期。 http://t.cn/AiWuigW5", "comments": [{"content": "不后悔跟兄弟们走过这一段人生旅程，这一站我先下车了，兄弟们加油，RNG加油。"}, {"content": "德玛西亚恭送野王[允悲][允悲][泪]"}, {"content": "回复@mlxgzzz:锅老师加油"}, {"content": "回复@VITALITY电子竞技俱乐部:最出动心弦的s7 评论配图"}, {"content": "[泪][泪][泪]"}, {"content": "嗯 再见 我也要正式跟你说再见了"}, {"content": "姿态尴尬不，还复出。。。我的天呐 退役了还复出 真特么"}, {"content": "再见香锅。"}, {"content": "回复@一蓑烟雨任苹笙:德玛西亚恭送野王[允悲][允悲][泪]"}, {"content": "回复@mlxgzzz:一定要好好休息吃好喝好！！胖胖的！！！！"}, {"content": "回复@一蓑烟雨任苹笙:剑网三跨界恭送野王。。青山不改，江湖再见[作揖]"}]}, {"weibo_url": "https://weibo.com/7184574431/HDN3Hd6nq", "like_num": 0, "repost_num": 0, "comment_num": 0, "images": ["http://wx1.sinaimg.cn/wap180/9a789c84gy1g51m03jprmj20u016khdv.jpg"], "content": "孟美岐呀//@不止不迟:#孟美岐舞出我人生6# [紫心]#舞出我人生舞所不能# 厚积薄发，舞所不能。你好，亲爱的小飞。你好，孟美岐。【代@DoreamonER 】 //@火箭少女101_孟美岐:#舞出我人生舞所不能# 背水一战，勇敢追梦！ 你好，小飞[太阳]", "comments": []}, {"weibo_url": "https://weibo.com/1929999277/HDN3HbpPL", "like_num": 0, "repost_num": 0, "comment_num": 0, "images": [], "content": "这段舞蹈真的令人极度舒适 四天过去了我还在看//@一个帅桃:呜呜呜我他妈来//@豆你玩:草 搞舞担真快落", "comments": []}, {"weibo_url": "https://weibo.com/1769742473/HDN3GAsD2", "like_num": 0, "repost_num": 0, "comment_num": 0, "images": [], "content": "#薛之谦[超话]##薛之谦717生日快乐# 薛之谦哥哥717生日快乐[蛋糕] 哥哥我们都好爱你好爱你[爱心] 毋容置疑！很爱很爱！并且会一直都在[爱心] 你的音乐值得我们每一次的期待！ 真的很好听！[爱心] 好想抱抱你！ 我的沙雕哥哥！我希望你永远开心幸福！ 我们爱你[爱心]我爱你[爱心] 今天的新歌巨好听[大哭]好听到没朋友[大哭]", "comments": []}, {"weibo_url": "https://weibo.com/5940691014/HDN3G0rAJ", "like_num": 0, "repost_num": 0, "comment_num": 0, "images": ["http://wx2.sinaimg.cn/wap180/006u2x70ly1g524rts3e4j32o02o0b29.jpg"], "content": "人类的悲观并不相通。 漫漫长夜 愿你好梦。", "comments": []}, {"weibo_url": "https://weibo.com/3242237345/HDN3FENTH", "like_num": 0, "repost_num": 0, "comment_num": 0, "images": ["http://wx4.sinaimg.cn/wap180/006dUtOVgy1g5238b5vnxj30u011ik08.jpg"], "content": "//@印乘:温柔又有绅士的男孩子简直是宝藏//@Lockdowne:以前看到的，一个女孩子走在路上，突然有一个男孩子拍拍她的肩膀：“你好啊，你今天穿的真好看，但我觉得你把外套系在腰上会更好看！”女孩子迷迷糊糊照着坐了，当她回到家，她才发现，她的特殊时期到啦", "comments": []}, {"weibo_url": "https://weibo.com/1765867473/HDN3CqCoP", "like_num": 0, "repost_num": 0, "comment_num": 0, "images": ["http://wx4.sinaimg.cn/wap180/6940ffd1gy1g524sdankpj23401r1x6p.jpg"], "content": "谢谢各位粉丝朋友发照片给我，真的幸好有你们，我才可以和更多海内外朋友分享《你好，我是丘俊鑫！》音乐会的精彩回忆。 #丘俊鑫 ##音乐会 # [组图共6张]", "comments": []}, {"weibo_url": "https://weibo.com/3670041902/HDN3BxiEd", "like_num": 0, "repost_num": 0, "comment_num": 0, "images": [], "content": "#薛之谦[超话]##薛之谦717生日快乐##薛之谦慢半拍# 36岁的你要快乐 36岁的你要唱很多歌 36岁的你一定不负所有人的喜欢 36岁的薛之谦你好 36岁的薛之谦生日快乐[蛋糕][气球]", "comments": []}, {"weibo_url": "https://weibo.com/5771629344/HDN3Bgag2", "like_num": 0, "repost_num": 0, "comment_num": 0, "images": ["http://wx4.sinaimg.cn/wap180/006iBarSgy1g524si3v9fj30u06re1jm.jpg"], "content": "[cp]#热门小说推荐##言情小说推荐# 爱你就是让你做正确的事，管你是为你好。爱之深故望之切，穿书文，女配文，霸道总裁，肉肉多的文，popo小说，小说安利，重生文，校园甜宠文，虐心小说，电竞甜文“阳府境强者何等可怕,就算双方的距离已经隔了十几丈,可他一道掌风依然可以将阴脉境的武者轰杀 [/cp]君子一言难尽", "comments": []}, {"weibo_url": "https://weibo.com/5146885726/HDN3B1uiO", "like_num": 0, "repost_num": 0, "comment_num": 0, "images": ["http://wx2.sinaimg.cn/wap180/005CjO5Ugy1g524shmz8vj30d62yvq8n.jpg"], "content": "#热门小说推荐##言情小说推荐# 爱你就是让你做正确的事，管你是为你好。爱之深故望之切，穿书文，女配文，霸道总裁，肉肉多的文，popo小说，小说安利，重生文，校园甜宠文，虐心小说，电竞甜文“还不是因为张铁森那小王八。”村长一提到张铁森是一肚子的火，拳头重重的捶在了桌上。甄霸天得知村长在生张铁森的气，心中暗暗松了口气，同时脸上也露出了一", "comments": []}, {"weibo_url": "https://weibo.com/5650139745/HDN3AoRqK", "like_num": 0, "repost_num": 0, "comment_num": 0, "images": ["http://wx4.sinaimg.cn/wap180/006dAXvGly1g51vvsuxz4j30xc11inpd.jpg"], "content": "你好我好大家好哈哈哈哈哈哈哈", "comments": []}];

function randomNum(minv, maxv) {
    let range = maxv - minv;
    let rand = Math.random();
    let num = minv + Math.floor(rand * range); //舍去
    return num;
}

function getRandomRobot() {
    if (!utils.isObjEmpty(ROBOTS)){
        return ROBOTS[randomNum(0, ROBOTS.length)];
    }else{
        getRobots();
        return null
    }
}

function getJSON(url, params={}) {
    return new Promise((resolve, reject) =>{
        axios.get(baseURL + url, {
            params: params
        }).then(function (response) {
            resolve(response.data);
        }).catch(function (err) {
            reject(err)
        });
    });
}

function postJSON(url, data={}) {
    return new Promise((resolve, reject) =>{
        axios.post(baseURL + url, data).then(function (response) {
            resolve(response.data);
        }).catch(function (err) {
            reject(err)
        });
    });
}


function search(page, username, keyword, topic, like_num, comment_num, cookie) {
    let url = '/search';
    // return new Promise((resolve, reject)=>{
    //     //     resolve(PACKETS);
        // })
    return new Promise((resolve, reject) => {
        getRobots().then((robots)=>{
            return getGroups()
        }).then((groups)=>{
            // return new Promise((resolve, reject) => {
            //     resolve(PACKETS);
            // });
            return getJSON(url, {
                page: page,
                username: username,
                keyword: keyword,
                topic: topic,
                like_num: like_num,
                comment_num: comment_num,
                cookie: cookie
            });
        }).then((packets)=>{
            let res = packets.map(function (packet) {
                let images = packet.images.map(function (image) {
                    return {
                        url: image,
                        select: true,
                        crop: [0, 0, 100, 100]
                    }
                });
                let comments = packet.comments.map(function (comment) {
                    return {
                        content: comment.content,
                        select: true,
                        user: getRandomRobot()
                    }
                });
                let groups = GROUPS.map(function (group) {
                    return {
                        name: group,
                        select: false
                    }
                });

                return {
                    weibo_url: packet.weibo_url,
                    select: true,
                    robot: getRandomRobot(),
                    sent_time: Date.now(),
                    content: packet.content,
                    images: images,
                    comments: comments,
                    groups: groups
                }
            });
            resolve(res);
        }).catch(reject);
    });
}

function confirm(data) {
    let url = '/confirm';
    axios.post(baseURL + url, data);
}


function getRobots(count=100) {
    let url = '/robots';
    return new Promise((resolve, reject) =>{
        if(utils.isObjEmpty(ROBOTS)){
            getJSON(url, {count: count}).then((data)=>{
                ROBOTS = data.map(function (robot) {
                    let gender = "";
                    if(robot.gender === 1){
                        gender = " 👩";
                    }else if(robot.gender === 2){
                        gender = " 👨";
                    }
                    return {
                        "uid": robot.uid,
                        "avatar": robot.avatar,
                        "gender": robot.gender,
                        "userId": robot.userId,
                        "nickName": robot.nickName,
                        "age": 8,
                        "value": robot.nickName + '#' + robot.userId + gender
                    }
                });
                resolve(ROBOTS);
            }).catch(reject)
        }else{
            resolve(ROBOTS);
        }
    });
}


function getGroups() {
    let url = '/groups';
    return new Promise((resolve, reject) => {
        if(utils.isObjEmpty(GROUPS)){
            getJSON(url).then((data)=>{
                GROUPS = data;
                resolve(GROUPS);
            }).catch(reject);
        }else{
            resolve(GROUPS);
        }
    });
}


export {search, confirm, getRobots, getGroups}