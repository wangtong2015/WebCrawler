from django.db import models

# Create your models here.
# class Tweets(models.Model):
#     """微博信息"""
#     _id = models.CharField(max_length=128, primary_key=True)
#     weibo_url = models.CharField(max_length=128)
#     like_num = models.IntegerField(default=0)
#     repost_num = models.IntegerField(default=0)
#     comment_num = models.IntegerField(default=0)
#     content = models.CharField(max_length=2048)
#     user_id = models.CharField(max_length=128)
#     tool = models.CharField(max_length=128, blank=True)
#     image_url = models.CharField(max_length=2048)  # JSON
#     video_url = models.CharField(max_length=128)
#     location = models.CharField(max_length=128)
#     location_map_info = models.CharField(max_length=128)
#     origin_weibo = models.CharField(max_length=2048)  # 原始微博，只有转发的微博才有这个字段
#     create_time = models.DateTimeField(auto_now_add=True, null=True)
#     update_time = models.DateTimeField(auto_now=True, null=True)
#
#
# class Comment(models.Model):
#     """微博评论信息"""
#     # comment_user_id = models.CharField(max_length=128)
#     tweet = models.ForeignKey(Tweets, to_field='_id')
#     content = models.CharField(max_length=1024)
#     like_num = models.IntegerField()
#     create_time = models.DateTimeField(auto_now_add=True)
#     update_time = models.DateTimeField(auto_now=True)
#


