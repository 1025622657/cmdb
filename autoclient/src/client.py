import requests
import json
from src.plugins import PluginManager
from lib.conf.config import settings
from lib.utils.aes_auth_client import encrypt
from lib.utils.api_auth_client import apiAuth

class Base(object):
    def post_asset(self, server_info):
        #数据转成字符再加密发送
        data = encrypt(json.dumps(server_info))#通过json序列化字典成字符类型，再encrypt加密成字节传输
        #向API发送资产信息
        result = requests.post(settings.API,
                               data=data,
                               headers={'OpenKey': apiAuth(), 'Content-Type': 'application/json'},
                               )

        print(json.loads(result.text))



class Agent(Base):
    """
    Agent模式下，找到唯一标识（使用config/cert文件下的主机名做唯一标识）
    第一次采集时，config/cert下的信息为空则以提交信息的hostname为准，
    多次时，则均以cert文件下的主机名为准
    """
    def execute(self):
        #linux上通过命令获取数据
        server_info = PluginManager().exec_plugin()

        # 【status】数据正确时发送，[basic]基本信息，hostname做为唯一标识
        #只有唯一标识数据正确才会发送到后台处理
        if  server_info['basic']['status']:

            hostname = server_info['basic']['data']['hostname']
            certname = open(settings.CERT_PATH,'r',encoding='utf-8').read().strip()#读
            #文件为空时，表示第一次写入，则把hostname写入文件,sserver_info['basic']['data']['hostname']未改变
            if not certname:
                with open(settings.CERT_PATH,'w',encoding='utf-8') as f:#写
                    f.write(hostname)
            #文件不为空时，表示已写入过，即使hostname有变更，则仍以certname为准 ，
            else:
                server_info['basic']['data']['hostname'] = certname

        #【status】数据错误时，打印错误信息
        for key in list(server_info.keys()):

            if not server_info[key]['status']:
                print('>>',server_info[key]['data'])
        #发送资产信息到api,执行基类下的post_asset()方法
        self.post_asset(server_info)


class SSHSALT(Base):
    def get_host(self):
        # 获取未采集的主机列表
        response = requests.get(settings.API)#get请求获取数据
        result = json.loads(response.text) #反序列化 "{"status":'True',data:['c1.com','c2.com']}"
        if not result['status']:
            return
        return result['data']

    def run(self,host):
        server_info = PluginManager(host).exec_plugin()
        self.post_asset(server_info)

    def execute(self):
        """
        线程池完成并发
        :return:
        """
        from concurrent.futures import ThreadPoolExecutor
        #获取未采集的主机列表
        host_list = self.get_host()

        #设置线程池，每次并发10个
        pool = ThreadPoolExecutor(10)
        for host in host_list:
            pool.submit(self.run,host)#传入要执行的函数与参数