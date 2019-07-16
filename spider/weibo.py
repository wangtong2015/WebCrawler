import requests
import time
import re
from lxml import etree
import json
import os
import yaml
import datetime
from WebCrawler import settings
import os
from spider import utils


log = settings.log
from random import randint

with open(os.path.join(settings.BASE_DIR, 'spider', 'cookie.json'), 'r') as f:
    COOKIES = json.load(f)
# 爬虫参数
def get_random_acount():
    return COOKIES[4]

# # 搜索参数
# USERNAME = ''
# TOPIC = ''
# KEYWORD = '蔡徐坤'
# LIKENUM = 10
# COMMENTNUM = 10


def time_fix(time_string):
    now_time = datetime.datetime.now()
    if '分钟前' in time_string:
        minutes = re.search(r'^(\d+)分钟', time_string).group(1)
        created_at = now_time - datetime.timedelta(minutes=int(minutes))
        return created_at.strftime('%Y-%m-%d %H:%M')

    if '小时前' in time_string:
        minutes = re.search(r'^(\d+)小时', time_string).group(1)
        created_at = now_time - datetime.timedelta(hours=int(minutes))
        return created_at.strftime('%Y-%m-%d %H:%M')

    if '今天' in time_string:
        return time_string.replace('今天', now_time.strftime('%Y-%m-%d'))

    if '月' in time_string:
        time_string = time_string.replace('月', '-').replace('日', '')
        time_string = str(now_time.year) + '-' + time_string
        return time_string

    return time_string


keyword_re = re.compile('<span class="kt">|</span>|原图|<!-- 是否进行翻译 -->|')
emoji_re = re.compile('<img alt="|" src="//h5\.sinaimg(.*?)/>')
white_space_re = re.compile('<br />')
div_re = re.compile('</div>|<div>')
image_re = re.compile('<img(.*?)/>')
url_re = re.compile('<a href=(.*?)>|</a>')


def extract_weibo_content(weibo_html):
    s = weibo_html
    if '转发理由' in s:
        s = s.split('转发理由:', maxsplit=1)[1]
    if 'class="ctt">' in s:
        s = s.split('class="ctt">', maxsplit=1)[1]
    s = s.split('赞', maxsplit=1)[0]
    s = keyword_re.sub('', s)
    s = emoji_re.sub('', s)
    s = url_re.sub('', s)
    s = div_re.sub('', s)
    s = image_re.sub('', s)
    if '<span class="ct">' in s:
        s = s.split('<span class="ct">')[0]
    s = white_space_re.sub(' ', s)
    s = s.replace('\xa0', '')
    s = s.strip(':')
    s = s.strip()
    return s


def extract_comment_content(comment_html):
    s = comment_html
    if 'class="ctt">' in s:
        s = s.split('class="ctt">', maxsplit=1)[1]
    s = s.split('举报', maxsplit=1)[0]
    s = emoji_re.sub('', s)
    s = keyword_re.sub('', s)
    s = url_re.sub('', s)
    s = div_re.sub('', s)
    s = image_re.sub('', s)
    s = white_space_re.sub(' ', s)
    s = s.replace('\xa0', '')
    s = s.strip(':')
    s = s.strip()
    return s


class Weibo(object):
    base_url = "https://weibo.cn"
    search_url = 'https://weibo.cn/search/?pos=search'

    def __init__(self, user_name='', topic='', keyword='', like_num=0, comment_num=0, page=1):
        self.account = get_random_acount()
        self.headers = self.account['header']
        self.user_name = user_name
        self.topic = topic
        self.keyword = keyword
        self.like_num = like_num
        self.comment_num = comment_num
        mode = ['0', '0', '0']
        if self.user_name:
            mode[0] = '1'
        if self.topic:
            mode[1] = '1'
        if self.keyword:
            mode[2] = '1'
        self.mode = ''.join(mode)
        self.result = []
        self.page = page
        self.max_page = 100
        self.search()

    def net(self, url, callback, method='GET', data=None, meta=None):
        if not data:
            data = {}
        try:
            if method == 'GET':
                r = requests.get(url, headers=self.headers, timeout=30, params=data)
            else:
                r = requests.post(url, headers=self.headers, timeout=30, data=data)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            if meta is not None:
                return callback(r, meta)
            else:
                return callback(r)
        except requests.exceptions.ConnectionError:
            log.error('ConnectionError -- please wait 3 seconds')
            # time.sleep(3)
        except requests.exceptions.ChunkedEncodingError:
            log.error('ChunkedEncodingError -- please wait 3 seconds')
            # time.sleep(3)
        return ''

    def get(self, url, callback, data=None, meta=None):
        return self.net(url, callback=callback, data=data, meta=meta)

    def post(self, url, callback, data, meta=None):
        return self.net(url, method='POST', callback=callback, data=data, meta=meta)

    # def __iter__(self):
    #     self.page = 1
    #     self.search()
    #     return self
    #
    # def __next__(self):
    #     if self.page > self.max_page:
    #         raise StopIteration
    #     self.page += 1
    #     self.result = []
    #     self.search()
    #     return self.result

    def search(self):
        data = {
            'page': self.page
        }
        if self.mode == '000':  # 什么也不搜
            pass
        if self.mode == '100':  # 只搜用户名
            data['keyword'] = self.user_name
            data['suser'] = '找人'
            self.post(url=self.search_url,
                      callback=self.parse_user_page,
                      data=data)
        elif self.mode == '010':  # 只搜主题
            data['keyword'] = '#' + self.topic + '#'
            data['smblog'] = '搜微博'
            self.post(url=self.search_url,
                      callback=self.parse_tweet_page,
                      data=data)
        elif self.mode == '001':  # 只搜关键词
            data['keyword'] = self.keyword
            data['smblog'] = '搜微博'
            self.post(self.search_url,
                      callback=self.parse_tweet_page,
                      data=data)
        else:  # 高级搜索
            data['advancedfilter'] = '1'
            data['sort'] = 'time'
            data['smblog'] = '搜索'
            if self.user_name:
                data['nick'] = self.user_name
            if self.topic:
                data['keyword'] = '#' + self.topic + '#'
                self.post(self.search_url,
                          callback=self.parse_tweet_page,
                          data=data)
            else:
                data['keyword'] = self.keyword
                self.post(self.search_url,
                          callback=self.parse_tweet_page,
                          data=data)

    def parse_tweet_page(self, response):
        if self.page == 1:
            all_page = re.search(r'/>&nbsp;1/(\d+)页</div>', response.text)
            if all_page:
                all_page = all_page.group(1)
                all_page = int(all_page)
                self.max_page = all_page
        # 解析本页的数据
        tree_node = etree.HTML(response.content)
        tweet_nodes = tree_node.xpath('//div[@class="c" and @id]')
        for index, tweet_node in enumerate(tweet_nodes):
            utils.log_progress(index, len(tweet_nodes))
            try:
                packet = dict()
                # packet['crawl_time'] = int(time.time())
                tweet_repost_url = tweet_node.xpath('.//a[contains(text(),"转发[")]/@href')[0]
                user_tweet_id = re.search(r'/repost/(.*?)\?uid=(\d+)', tweet_repost_url)
                packet['weibo_url'] = 'https://weibo.com/{}/{}'.format(user_tweet_id.group(2), user_tweet_id.group(1))
                # packet['user_id'] = user_tweet_id.group(2)
                # packet['_id'] = '{}_{}'.format(user_tweet_id.group(2), user_tweet_id.group(1))
                # create_time_info_node = tweet_node.xpath('.//span[@class="ct"]')[-1]
                # create_time_info = create_time_info_node.xpath('string(.)')
                # if "来自" in create_time_info:
                #     packet['created_at'] = time_fix(create_time_info.split('来自')[0].strip())
                #     packet['tool'] = create_time_info.split('来自')[1].strip()
                # else:
                #     packet['created_at'] = time_fix(create_time_info.strip())

                like_num = tweet_node.xpath('.//a[contains(text(),"赞[")]/text()')[-1]
                packet['like_num'] = int(re.search('\d+', like_num).group())

                repost_num = tweet_node.xpath('.//a[contains(text(),"转发[")]/text()')[-1]
                packet['repost_num'] = int(re.search('\d+', repost_num).group())

                comment_num = tweet_node.xpath(
                    './/a[contains(text(),"评论[") and not(contains(text(),"原文"))]/text()')[-1]
                packet['comment_num'] = int(re.search('\d+', comment_num).group())

                images = tweet_node.xpath('.//img[@alt="图片"]/@src')
                if images:
                    packet['images'] = [images[0]]
                else:
                    packet['images'] = []
                #
                # videos = tweet_node.xpath('.//a[contains(@href,"https://m.weibo.cn/s/video/show?object_id=")]/@href')
                # if videos:
                #     packet['video_url'] = videos[0]

                # map_node = tweet_node.xpath('.//a[contains(text(),"显示地图")]')
                # if map_node:
                #     map_node = map_node[0]
                #     map_node_url = map_node.xpath('./@href')[0]
                #     map_info = re.search(r'xy=(.*?)&', map_node_url).group(1)
                #     packet['location_map_info'] = map_info
                #     packet['location'] = map_node.xpath('./preceding-sibling::a/text()')[0]

                # repost_node = tweet_node.xpath('.//a[contains(text(),"原文评论[")]/@href')
                # if repost_node:
                #     packet['origin_weibo'] = repost_node[0]

                # 检测有没有阅读全文:
                all_content_link = tweet_node.xpath('.//a[text()="全文" and contains(@href,"ckAll=1")]')
                if all_content_link:
                    all_content_url = self.base_url + all_content_link[0].xpath('./@href')[0]
                    packet['content'] = self.get(url=all_content_url, callback=self.parse_all_content)
                else:
                    tweet_html = etree.tostring(tweet_node, encoding='unicode')
                    packet['content'] = extract_weibo_content(tweet_html)

                # 抓取该微博的评论信息
                comment_url = self.base_url + '/comment/' + packet['weibo_url'].split('/')[-1] + '?page=1'
                all_comment = []
                self.get(comment_url, callback=self.parse_comment, meta=all_comment)
                packet['comments'] = all_comment

            except Exception as e:
                # self.logger.error(e)
                log.error(e)
            finally:
                self.result.append(packet)

    def parse_user_page(self, response):
        # print(response)
        return ''
        pass

    def parse_all_content(self, response):
        tree_node = etree.HTML(response.content)
        content_node = tree_node.xpath('//*[@id="M_"]/div[1]')[0]
        tweet_html = etree.tostring(content_node, encoding='unicode')
        return extract_weibo_content(tweet_html)

    def parse_comment(self, response, meta):
        # 如果是第1页，一次性获取后面的所有页
        all_comment = meta
        tree_node = etree.HTML(response.content)
        comment_nodes = tree_node.xpath('//div[@class="c" and contains(@id,"C_")]')
        for comment_node in comment_nodes:
            comment_user_url = comment_node.xpath('.//a[contains(@href,"/u/")]/@href')
            if not comment_user_url:
                continue
            comment_item = dict()
            # comment_item['crawl_time'] = int(time.time())
            # comment_item['comment_user_id'] = re.search(r'/u/(\d+)', comment_user_url[0]).group(1)
            comment_item['content'] = extract_comment_content(etree.tostring(comment_node, encoding='unicode'))
            # comment_item['_id'] = comment_node.xpath('./@id')[0]
            # created_at_info = comment_node.xpath('.//span[@class="ct"]/text()')[0]
            # like_num = comment_node.xpath('.//a[contains(text(),"赞[")]/text()')[-1]
            # comment_item['like_num'] = int(re.search('\d+', like_num).group())
            # comment_item['created_at'] = time_fix(created_at_info.split('\xa0')[0])
            all_comment.append(comment_item)
        # if response.url.endswith('page=1'):
        #     all_page = re.search(r'/>&nbsp;1/(\d+)页</div>', response.text)
        #     if all_page:
        #         all_page = all_page.group(1)
        #         all_page = int(all_page)
        #         for page_num in range(2, all_page + 1):
        #             page_url = response.url.replace('page=1', 'page={}'.format(page_num))
        #             all_comment.append(self.get(url=page_url, meta=all_comment, callback=self.parse_comment))


if __name__ == '__main__':
    res = Weibo(keyword="英雄联盟").result
    print(json.dumps(res, sort_keys=True, indent=4, separators=(', ', ': '), ensure_ascii=False))







