from django.shortcuts import render
from django.http import HttpResponse
from datetime import date, datetime
import time
import json
from spider import weibo
from WebCrawler import settings
from spider import net
from WebCrawler import header
import os

def parseInt(value, default=0):
    try:
        value = int(value)
    except ValueError:
        value = default
    return value


# Create your views here.
class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        elif isinstance(obj, time.struct_time):
            return time.strftime(format, obj)
        elif isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        elif isinstance(obj, Exception):
            return str(obj)
        else:
            return json.JSONEncoder.default(self, obj)


def json_response(result):
    return HttpResponse(json.dumps(result, ensure_ascii=False, cls=CJsonEncoder), content_type="application/json,charset=utf-8")


def search(request):
    packets = []
    if request.method == 'GET':
        page = request.GET.get('page', 1)
        username = request.GET.get('username', '')
        keyword = request.GET.get('keyword', '')
        topic = request.GET.get('topic', '')
        like_num = request.GET.get('like_num', 0)
        comment_num = request.GET.get('comment_num', 0)
        cookie = request.GET.get('cookie', '')
        count = request.GET.get('cookie', -1)
        page = parseInt(page, 1)
        like_num = parseInt(like_num)
        comment_num = parseInt(comment_num)
        count = parseInt(count, -1)
        wb = weibo.Weibo(page=page,
                         user_name=username,
                         topic=topic,
                         keyword=keyword,
                         like_num=like_num,
                         comment_num=comment_num,
                         cookie=cookie,
                         count=count)
        packets = wb.result
    return json_response(packets)


def confirm(request):
    res = {
        'success': False,
        'message': '请使用POST方法'
    }
    if request.method == 'POST':
        data = json.loads(request.body)
        packets = data.get('packets', [])
        cookie = data.get('cookie', '')
        header.set_cookie(cookie)
        for packet in packets:
            imageList = packet['imageList']
            image_path_list = net.downloadImage(imageList, modify=True)
            imageList = net.crop_resize_images(imageList)
            net.upload_image(imageList, modify=True)
            packet['imageList'] = imageList
            # 删除文件
            # for image_path in image_path_list:
            #     if os.path.exists(image_path):
            #         os.remove(image_path)
        res = net.batch_save_dynamic(packets)
    return json_response(res)


def fetch_user(request):
    res = {
        'success': False,
        'message': '请使用GET方法'
    }
    if request.method == 'GET':
        count = request.GET.get('count', 100)
        count = parseInt(count, 100)
        res = net.fetch_vest_user_list(count)
    return json_response(res)


def groups(request):
    return json_response(settings.GROUPS)


def test(request):
    print(request.FILES)
    return json_response({})


def upload_avatar(request):
    res = {
        'success': False,
        'message': '请使用POST方法'
    }
    if request.method == 'POST':
        file = request.FILES.get('file')
        image_path = os.path.join(settings.IMAGE_DIR, file.name)
        f = open(image_path, 'wb')
        for chunk in file.chunks(chunk_size=1024):
            f.write(chunk)
        f.close()
        avatar_list = net.upload_image([image_path], mode='avatar')
        if avatar_list:
            res = {
                'base_url': settings.TEST_URL,
                'avatarImg': avatar_list[0]
            }
        else:
            res = {
                'success': False,
                'message': '上传失败'
            }
    return json_response(res)


def upload_image(request):
    res = {
        'success': False,
        'message': '请使用POST方法'
    }
    if request.method == 'POST':
        file = request.FILES.get('file')
        image_path = os.path.join(settings.IMAGE_DIR, file.name)
        f = open(image_path, 'wb')
        for chunk in file.chunks(chunk_size=1024):
            f.write(chunk)
        f.close()
        avatar_list = net.upload_image([image_path])
        if avatar_list:
            res = {
                'base_url': settings.TEST_URL,
                'avatarImg': avatar_list[0]
            }
        else:
            res = {
                'success': False,
                'message': '上传失败'
            }
    return json_response(res)


def add_user(request):
    res = {
        'success': False,
        'message': '请使用POST方法'
    }
    if request.method == 'POST':
        data = json.loads(request.body)
        user = data.get('user')
        print(user)
        res = net.add_vest_user([user])
        print(res)
    return json_response(res)

