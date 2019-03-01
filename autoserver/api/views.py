import json
import hashlib
from django.shortcuts import render,HttpResponse
from django.http import JsonResponse

from django.shortcuts import render
from repository import models
import datetime
import time
from utils.api_auth_server import api_auth
from utils.aes_auth_server import decrypt
from django.conf import settings

# Create your views here.

#redis/Memcache到期后，数据会没有

api_key_record = {
    # "61d81a820af928e88c137763f544ccd6|1527240537.548074":1527240537.548074
}



@api_auth
def asset(request):
    if request.method == "GET":
        ys = '重要的不能看的数据'
        return HttpResponse(json.dumps(ys))

    elif request.method == "POST":
        #解密
        server_info = decrypt(request.body)#字节解密成字符串
        server_info = json.loads(server_info)#字符串反序列化成字典

        #数据增删改操作
        from api.server import PluginManager
        result = PluginManager(server_info).exec_plugin()
        return HttpResponse(json.dumps(result))


#http://127.0.0.1:8000/api/servers.html GET:获取服务器列表
#http://127.0.0.1:8000/api/servers.html POST:创建服务器
#http://127.0.0.1:8000/api/servers/1.html GET:获取单条信息，如id为1的信息
#http://127.0.0.1:8000/api/servers/1.html DELETE:删除单条信息，如id为1的信息
#http://127.0.0.1:8000/api/servers/1.html PUT:更新单条信息，如id为1的信息

def servers(request):
    if request.method == 'GET':
        v = models.Server.objects.values('id','hostname')
        server_list = list(v)
        #JsonResponse默认只返回字典格式
        #返回列表时，需加safe=False
        return JsonResponse(server_list,safe=False)

    elif request.method == "POST":
        print(request.body,request.POST)
        return JsonResponse({"status":200})

def servers_detail(request,nid):
    if request.method == "GET":
        obj = models.Server.objects.filter(id=nid).first()
        return HttpResponse('get')
    elif request.method == "DELETE":
        models.Server.objects.filter(id=nid).delete()
        return HttpResponse('delete')
    elif request.method == "PUT":
        # 获取数据 request.body
        models.Server.objects.filter(id=nid).update()





