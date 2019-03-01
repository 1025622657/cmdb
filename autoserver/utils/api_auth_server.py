import time
import hashlib
from django.shortcuts import HttpResponse
from django.conf import settings
import json

api_key_record = {
    # "61d81a820af928e88c137763f544ccd6|1527240537.548074":1527240537.548074
}

def api_auth(func):
    def wrap(request,*args,**kwargs):
        # print(request.META)
        #客户端：传参方式：response = requests.get("http://127.0.0.1:8000/api/asset.html?OPENKEY=%s"%(md5_time_key))
        # client_md5_time_key = request.GET.get('OPENKEY')


        # 客户端：传参方式：response = requests.get("http://127.0.0.1:8000/api/asset.html",headers={'OpenKey':md5_time_key})
        client_md5_time_key = request.META.get('HTTP_OPENKEY')

        if not client_md5_time_key:
            return HttpResponse('请传入API验证令牌')
        client_md5_key,client_ctime = client_md5_time_key.split('|')
        client_ctime = float(client_ctime)
        server_time = time.time()
        print("服务器API验证",server_time-client_ctime)

        #时间，第一关，一般2s内到达的就可以访问
        if server_time-client_ctime > 10:#10s
            return HttpResponse(json.dumps('【第一关】时间过期了'))

        #加密，第二关，定义的令牌+客户端的时间做md5哈希认证
        temp = "%s|%s"%(settings.AUTH_KEY,client_ctime)
        m = hashlib.md5()

        #temp转成字节两种方式均可
        # m.update(bytes(temp,encoding='utf-8'))
        m.update(temp.encode('utf-8'))

        server_md5_key = m.hexdigest()

        if server_md5_key != client_md5_key:
            return HttpResponse(json.dumps('【第二关】认证失败'))


        #第三关：与已访问的记录列表对比
        #判断数据key是否在字典里，使用in方式，在字典里，in比较的是key
        if client_md5_time_key in api_key_record:
            return HttpResponse(json.dumps('【第三关】有人已经来过了'))
        else:
            #把第一次来的的用户，以字典的形式添加到api_key_record里，value为超过时间
            api_key_record[client_md5_time_key] = client_ctime + 10


        #删除api_key_record里过时的数据，只存在规定时间内到来的用户
        for k in list(api_key_record.keys()):
            v = api_key_record[k]
            if server_time > v:
                del api_key_record[k]

        return func(request)

    return wrap