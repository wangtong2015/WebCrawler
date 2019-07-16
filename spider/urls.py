from django.urls import path
from WebCrawler import settings
from spider import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('search/', views.search),
    path('confirm/', views.confirm),
    path('robots/', views.robots),
    path('groups/', views.groups)
]
