// 深拷贝对象
function copy(data) {
    return JSON.parse(JSON.stringify(data));
}

// 判断对象是否为空
function isObjEmpty(obj){
    if(!obj){return true}
    else {
        let obj_str = JSON.stringify(obj)
        return obj_str === "{}" || obj_str === "[]";
    }
}

// 判断字符串是否为空
function isStrEmpty(obj) {
    return typeof obj == "undefined" || obj == null || obj === "";
}



// 输出Obj
function display(obj){
    let text = '';
    for(let key in obj){
        if(key === 'display'){
            continue;
        }
        text += key + ':' + obj[key] + '\n';
    }
    return text;
}

//判断鼠标点击的位置是否在某个div区域内
function isInDiv(event,divId){
    let div = document.getElementById(divId);
    let x=event.clientX;
    let y=event.clientY;
    let divx1 = div.offsetLeft;
    let divy1 = div.offsetTop;
    let divx2 = div.offsetLeft + div.offsetWidth;
    let divy2 = div.offsetTop + div.offsetHeight;
    return ( x < divx1 || x > divx2 || y < divy1 || y > divy2)
}

export {copy, display, isStrEmpty, isObjEmpty, isInDiv}