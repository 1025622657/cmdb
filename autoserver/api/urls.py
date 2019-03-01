from django.conf.urls import url,include
from api import views


urlpatterns = [
    url(r'^asset.html$',views.asset),#三种模式的数据存储
    url(r'^servers.html$',views.servers),#获取未采集的服务器主机信息
    url(r'^servers/(\d+).html$',views.servers_detail),

]