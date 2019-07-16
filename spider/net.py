import requests
import json
from urllib import parse
from requests_toolbelt import MultipartEncoder
import time
from WebCrawler import settings
log = settings.log


#  图片上传
def upload_image(image_path, mode='dynamic'):
    url = settings.TEST_URL + '/component/upload2/uploadByForm/' + mode
    m = MultipartEncoder(
        fields={
            'file': ('test.png', open(image_path, 'rb'), 'image/png'),
            'originalName': 'test.png'
        }
    )
    headers = {
        'Content-Type': m.content_type
    }
    res = []
    try:
        r = requests.request('POST', url, headers=headers, data=m)
        res = json.loads(parse.unquote(r.text))['data']
    except Exception as e:
        log.error(e)
    return res


# 马甲用户添加
def add_vest_user(gender, avatarImg, nickName, birthday, sign, school):
    url = settings.TEST_URL + '/api/user/generateVestUsers'
    headers = {
        'Content-Type': 'application/json'
    }
    data = [
            {
                'gender': gender,
                'avatarImg': avatarImg,
                'nickName': nickName,
                'birthday': birthday,
                'sign': sign,
                'school': school
            }
        ]
    res = []
    try:
        r = requests.post(url, json=data, headers=headers)
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
def batch_save_dynamic(userid, image):
    url = settings.TEST_URL + '/api/dynamic/batchSaveDynamic'
    headers = {
        'Content-Type': 'application/json'
    }
    data = [
        {
            "content": "测试动态1",
            "addTime": int(time.time()),
            "userId": userid,
            "imageList": [
                    {
                        "img": image,
                        "width": 1024,
                        "high": 508
                    }
                ],
            "commentsList": [
                {
                    "commentContent": "心烦意乱",
                    "addTime": int(time.time())
                }
            ]
        }
    ]
    r = requests.post(url, json=data, headers=headers)
    res = json.loads(parse.unquote(r.text))
    return res


def main():
    # img_path = '1.png'
    # res = upload_image(img_path)
    # img_url = res[0]['relativePath']
    # add_vest_user(gender=1,
    #               avatarImg=img_url,
    #               nickName='测试用户1',
    #               birthday=time.time(),
    #               sign='我爱学习',
    #               school='清华大学')
    user_list = fetch_vest_user_list()
    user = user_list[0]
    res = batch_save_dynamic(149, '/upload/dynamic/2019/07/16/c165861c1e6b49f21a8bcd71f969b501/file.png')
    print(res)


if __name__ == '__main__':
    main()

