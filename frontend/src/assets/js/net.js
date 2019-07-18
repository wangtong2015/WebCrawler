import axios from 'axios';
import * as utils from './utils';
import sourceEmoji from 'emoji-convert-resource-base';

import convert from 'emoji-convert';

convert.extend(sourceEmoji);


const baseURL = '/spider';
let GROUPS = [];
let ROBOTS = [];


// ROBOTS = ROBOTS.map(function (robot) {
//     let gender = "";
//     if(robot.gender === 1){
//         gender = " 👩";
//     }else if(robot.gender === 2){
//         gender = " 👨";
//     }
//     return {
//         uid: robot.uid,
//         avatar: robot.avatar,
//         gender: robot.gender,
//         userId: robot.userId,
//         nickName: robot.nickName,
//         age: 8,
//         value: robot.nickName + '#' + robot.userId + gender
//     }
// });

function generateGroup() {
    return GROUPS.map(function (group) {
        return {
            name: group,
            select: false
        }
    });
}


function randomNum(minv, maxv) {
    let range = maxv - minv;
    let rand = Math.random();
    let num = minv + Math.floor(rand * range); //舍去
    return num;
}

function getRandomRobot() {
    if (!utils.isObjEmpty(ROBOTS)){
        let robot = ROBOTS[randomNum(0, ROBOTS.length)];
        return utils.copy(robot);
    }else{
        getRobots();
        return null
    }
}


// const URL_DICT = {};
function getJSON(url, params={}) {
    return new Promise((resolve, reject) =>{
        // if(URL_DICT.hasOwnProperty(url) && URL_DICT[url]){
        //     reject({});
        //     return
        // }
        // URL_DICT[url] = true;
        axios.get(baseURL + url, {
            params: params
        }).then(function (response) {
            // URL_DICT[url] = false;
            if(response.data === false){
                reject(response.message);
            }else{
                resolve(response.data);
            }
        }).catch(function (err) {
            // URL_DICT[url] = false;
            reject(err)
        });
    });
}

function postJSON(url, data={}) {
    console.log(url, data);
    return new Promise((resolve, reject) =>{
        // if(URL_DICT.hasOwnProperty(url) && URL_DICT[url]){
        //     reject({});
        //     return
        // }
        // URL_DICT[url] = true;
        axios.post(baseURL + url, data).then(function (response) {
            // URL_DICT[url] = false;
            if(response.data === false){
                reject(response.message);
            }else{
                resolve(response.data);
            }
        }).catch(function (err) {
            // URL_DICT[url] = false;
            reject(err);
        });
    });
}


function search(page, username, keyword, topic, like_num, comment_num, cookie) {
    let url = '/search/';
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
                let images = packet.imageList.map(function (image) {
                    let new_image = {
                        img: image.img,
                        select: true,
                        crop: [0, 0, 100, 100, 100],
                        size: [800, 600, 1]
                    };
                    utils.getImageSize(image.img).then((size)=>{
                        new_image.size = size;
                    });
                    return new_image;
                });
                let comments = packet.commentsList.map(function (comment) {
                    return {
                        commentContent: convert.toUnicode(comment.commentContent),
                        select: true,
                        user: getRandomRobot(),
                        addTime: Date.now() + randomNum(100000, 1000000)
                    }
                });
                let groups = generateGroup();

                return {
                    weibo_url: packet.weibo_url,
                    select: true,
                    user: getRandomRobot(),
                    addTime: Date.now() + randomNum(10000, 100000),
                    content: convert.toUnicode(packet.content),
                    imageList: images,
                    commentsList: comments,
                    groups: groups,
                    comment_num: packet.comment_num,
                    like_num: packet.like_num,
                    repost_num: packet.repost_num
                }
            });
            resolve(res);
        }).catch(reject);
    });
}

function confirm(all_data, cookie) {
    let url = '/confirm/';
    let packets = [];
    for(let index in all_data){
        if(!all_data.hasOwnProperty(index)){
            continue;
        }
        let data = all_data[index];
        if(!data.select){
            continue;
        }
        let imageList = [];
        for(let im_index in data.imageList){
            if(!data.imageList.hasOwnProperty(im_index)){
                continue;
            }
            let image = data.imageList[im_index];
            if(!image.select){
                continue;
            }
            imageList.push({
                img: image.img,
                crop: image.crop
            })
        }
        let commentsList = [];
        for(let com_index in data.commentsList){
            if(!data.commentsList.hasOwnProperty(com_index)){
                continue;
            }
            let comment = data.commentsList[com_index];
            if(!comment.select){
                continue;
            }
            commentsList.push({
                commentContent: comment.commentContent,
                addTime: utils.timeFix(comment.addTime)
            })
        }
        packets.push({
            content: data.content,
            addTime: utils.timeFix(data.addTime),
            userId: data.user.userId,
            imageList: imageList,
            commentsList: commentsList
        });
    }
    return postJSON(url, {
        'packets': packets,
        'cookie': cookie
    })
}


function getRobots(count=100, force=false) {
    let url = '/user/fetchUser/';
    return new Promise((resolve, reject) =>{
        if(utils.isObjEmpty(ROBOTS) || force){
            getJSON(url, {count: count}).then((data)=>{
                ROBOTS = data.map(function (robot) {
                    let gender = "";
                    // if(robot.gender === 1){
                    //     gender = " 👩";
                    // }else if(robot.gender === 2){
                    //     gender = " 👨";
                    // }
                    return {
                        "uid": robot.uid,
                        "avatar": robot.avatar,
                        "gender": robot.gender,
                        "userId": robot.userId,
                        "nickName": robot.nickName,
                        "age": 8,
                        "mobileNum": robot.mobileNum,
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
    let url = '/groups/';
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


function addUser(user) {
    let url = '/user/addUser/';
    return postJSON(url, {
        user: user
    });
}

function generateComment() {
    return new Promise((resolve, reject) => {
        getRobots().then((robots)=>{
            resolve({
                commentContent: "",
                addTime: Date.now() + 100000,
                user: getRandomRobot()
            })
        })
    })
}


function generatePacket() {
    let packet = {
        content: "",
        addTime: Date.now() + 10000,
        user: {},
        imageList: [],
        commentsList: [],
        like_num: 0,
        repost_num: 0
    };
    return new Promise((resolve, reject) => {
        getRobots().then((robots)=>{
            return getGroups()
        }).then((groups)=>{
            packet.user = getRandomRobot();
            packet.groups = generateGroup();
            generateComment.then((comment)=>{
                packet.commentsList.push(comment);
                resolve(packet);
            })
        })
    });
}

export {
    search,
    confirm,
    getRobots,
    getGroups,
    addUser,
    getRandomRobot,
    generateGroup,
    generatePacket,
    generateComment
}