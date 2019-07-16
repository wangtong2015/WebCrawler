from django.shortcuts import render
from django.http import HttpResponse
from datetime import date, datetime
import time
import json
from spider import weibo
from WebCrawler import settings
from spider import net


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
        page = parseInt(page, 1)
        like_num = parseInt(like_num)
        comment_num = parseInt(comment_num)
        wb = weibo.Weibo(page=page,
                         user_name=username,
                         topic=topic,
                         keyword=keyword,
                         like_num=like_num,
                         comment_num=comment_num,
                         cookie=cookie)
        packets = wb.result
    return json_response(packets)


def confirm(request):

    pass


def robots(request):
    res = []
    if request.method == 'GET':
        count = request.GET.get('count', 100)
        count = parseInt(count, 100)
        res = net.fetch_vest_user_list(count)
    return json_response(res)


def groups(request):
    return json_response(settings.GROUPS)
