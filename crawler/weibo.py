import sys
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)
    sys.path.append(os.path.join(BASE_DIR, 'crawler'))
import requests
import time
import re
from lxml import etree
import json
import yaml
import datetime
from WebCrawler import settings
import os
from crawler import utils
from WebCrawler import header

log = settings.log
from random import randint

class Weibo(object):
    base_url = "https://weibo.cn"
    search_url = 'https://weibo.cn/search/?pos=search'

    def __init__(self, user_name='', topic='', keyword='', like_num=0, comment_num=0, page=1, cookie='', count=-1, url=''):
        header.set_cookie(cookie)
        self.count = count
        self.headers = header.get_header()
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
            utils.log_progress(index, len(tweet_nodes), '爬取数据')
            if self.count == 0:
                break
            self.count -= 1
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
                like_num = int(re.search('\d+', like_num).group())
                if like_num < self.like_num:
                    continue
                packet['like_num'] = like_num

                repost_num = tweet_node.xpath('.//a[contains(text(),"转发[")]/text()')[-1]
                repost_num = int(re.search('\d+', repost_num).group())
                packet['repost_num'] = repost_num

                comment_num = tweet_node.xpath(
                    './/a[contains(text(),"评论[") and not(contains(text(),"原文"))]/text()')[-1]
                comment_num = int(re.search('\d+', comment_num).group())
                if comment_num < self.comment_num:
                    continue
                packet['comment_num'] = comment_num

                all_image_url = tweet_node.xpath('.//a[contains(text(),"组图")]/@href')
                if all_image_url:
                    images = self.get(all_image_url[0], self.parse_all_image)
                else:
                    images = tweet_node.xpath('.//a[contains(text(),"原图")]/@href')
                    if not images:
                        images = tweet_node.xpath('.//img[@alt="图片"]/@src')
                new_images = []
                if images:
                    packet['imageList'] = [{'img': utils.fix_image_url(self.base_url, image_url)} for image_url in images]
                else:
                    packet['imageList'] = []

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
                    packet['content'] = utils.extract_weibo_content(tweet_html)

                # 抓取该微博的评论信息
                comment_url = self.base_url + '/comment/' + packet['weibo_url'].split('/')[-1] + '?page=1'
                all_comment = []
                self.get(comment_url, callback=self.parse_comment, meta=all_comment)
                packet['commentsList'] = all_comment

            except Exception as e:
                # self.logger.error(e)
                log.error(e)
            finally:
                self.result.append(packet)

    def parse_all_image(self, response):
        image_node = etree.HTML(response.content)
        images = image_node.xpath('.//a[contains(text(),"原图")]/@href')
        return images

    def parse_user_page(self, response):
        # print(response)
        # 解析本页的数据
        tree_node = etree.HTML(response.content)
        urls = tree_node.xpath('.//a[contains(text(),"{0}")]/@href'.format(self.user_name))
        if urls:
            self.get(self.base_url + urls[0], callback=self.parse_tweet_page)

    def parse_all_content(self, response):
        tree_node = etree.HTML(response.content)
        content_node = tree_node.xpath('//*[@id="M_"]/div[1]')[0]
        tweet_html = etree.tostring(content_node, encoding='unicode')
        return utils.extract_weibo_content(tweet_html)

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
            comment_item['commentContent'] = utils.extract_comment_content(etree.tostring(comment_node, encoding='unicode'))
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
    res = Weibo(keyword="9图").result
    print(json.dumps(res, sort_keys=True, indent=4, separators=(', ', ': '), ensure_ascii=False))







