from django.urls import path
from WebCrawler import settings
from spider import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('search/', views.search),
    path('confirm/', views.confirm),
    path('user/fetchUser/', views.fetch_user),
    path('user/addUser/', views.add_user),
    path('groups/', views.groups),
    path('upload/image/avatar/', views.upload_avatar),
    path('upload/image/', views.upload_image),
    path('test/', views.test)
]
