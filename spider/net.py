import sys
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)
import requests
import json
from urllib import parse
from requests_toolbelt import MultipartEncoder
import time
from WebCrawler import settings, header
import whatimage
from PIL import Image
from spider import utils
log = settings.log


# 图片下载
def downloadImage(imageList, image_dir=settings.IMAGE_DIR, threshold=800, modify=False, cookie=''):
    res = []
    header.set_cookie(cookie)
    for image in imageList:
        if isinstance(image, dict):
            image_url = image.get('img', 'no')
        else:
            image_url = image
        if not image_url:
            continue
        try:
            response = requests.get(image_url, headers=header.get_header())
            img = response.content
        except Exception as e:
            log.error(e)
            image['img'] = ''
            continue
        ext = os.path.splitext(image_url)[-1]
        if not ext:
            ext = whatimage.identify_image(img)
        if not ext:
            image['img'] = ''
            continue
        if ext[0] != '.':
            ext = '.' + ext
        image_name = str(hash(image_url)) + ext
        image_path = os.path.join(image_dir, image_name)
        with open(image_path, 'wb') as f:
            f.write(img)
        log.info("下载成功" + image_path)
        res.append(image_path)
        if modify:
            image['img'] = image_path
    return res


def crop_resize_images(images):
    res = []
    for image in images:
        image_path = image['img']
        if not image_path:
            continue
        image_crop = image['crop']
        im = Image.open(image_path)
        width, height = im.size
        crop = (
            image_crop[0] / 100 * width,
            image_crop[1] / 100 * height,
            image_crop[2] / 100 * width,
            image_crop[3] / 100 * height
        )
        im = im.crop(crop)
        width, height = im.size
        ratio = image_crop[4] / 100
        width = int(ratio * width)
        height = int(ratio * height)
        im = im.resize((width, height))
        # image_path_split = os.path.splitext(image_path)
        # new_image_path = image_path_split[0] + '.' + str(width) + 'x' + str(height) + image_path_split[1]
        im.save(image_path)
        log.info("crop成功"+image_path)
        res.append({
            'img': image_path,
            'width': width,
            'high': height
        })
    return res


#  图片上传
def upload_image(imageList, mode='dynamic', modify=False):
    url = settings.TEST_URL + '/component/upload2/uploadByForm/' + mode
    data = []
    files = []
    for image in imageList:
        if isinstance(image, dict):
            image_path = image.get('img')
        else:
            image_path = image
        if not image_path:
            continue
        image_name = os.path.split(image_path)[-1]
        ext = os.path.splitext(image_name)[-1]
        data.append(('originalName', image_name))
        files.append(('file', (image_name, open(image_path, 'rb'), 'image/%s' % ext)))
    res = []
    try:
        r = requests.request('POST', url, files=files, data=data)
        data = json.loads(parse.unquote(r.text))['data']
        for index, line in enumerate(data):
            relativePath = line.get('relativePath')
            if relativePath:
                res.append(relativePath)
                imageList[index]['img'] = relativePath
            else:
                imageList[index]['img'] = ''
    except Exception as e:
        log.error(e)
    return res


# 马甲用户添加
def add_vest_user(users):
    url = settings.TEST_URL + '/api/user/generateVestUsers'
    headers = {
        'Content-Type': 'application/json'
    }
    res = []
    try:
        r = requests.post(url, json=users, headers=headers)
        res = json.loads(parse.unquote(r.text))
    except Exception as e:
        log.error(e)
    return res


def fetch_vest_user_list(count=100):
    url = settings.TEST_URL + '/api/user/fetchVestUserList'
    res = []
    try:
        r = requests.get(url, params={"listSize": count})
        res = json.loads(parse.unquote(r.text))['data']
    except Exception as e:
        log.error(e)
    return res


# 批量保存动态及评论
def batch_save_dynamic(packets):
    url = settings.TEST_URL + '/api/dynamic/batchSaveDynamic'
    headers = {
        'Content-Type': 'application/json'
    }
    data = packets
    res = {"success": False}
    try:
        r = requests.post(url, json=data, headers=headers)
        res = json.loads(parse.unquote(r.text))
    except Exception as e:
        res["message"] = str(e)
    return res


def main():
    imageList = [{
        'img': "https://weibo.cn/mblog/oripic?id=HfS2Na6l8&u=006ZH3qjgy1g009lzkmzwj334022r7wk&rl=2"
    }]
    downloadImage(imageList, modify=True)
    print(imageList)
    # img_path = '1.png'
    # res = upload_image(img_path)
    # img_url = res[0]['relativePath']
    # add_vest_user(gender=1,
    #               avatarImg=img_url,
    #               nickName='测试用户1',
    #               birthday=time.time(),
    #               sign='我爱学习',
    #               school='清华大学')
    # user_list = fetch_vest_user_list()
    # user = user_list[0]
    # res = batch_save_dynamic(149, '/upload/dynamic/2019/07/16/c165861c1e6b49f21a8bcd71f969b501/file.png')
    # print(res)
    # res = upload_image(['./spider/stone.jpeg', './spider/turtle.jpeg'])
    # print(res)


if __name__ == '__main__':
    main()

