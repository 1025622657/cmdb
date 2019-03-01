import importlib
import json
import traceback #错误的堆栈
from django.conf import settings  #导入配置路径（实现自定义配置+默认配置的整合）
from repository import models
from django.shortcuts import HttpResponse
class PluginManager(object):
    def __init__(self,server_info):
        self.plugin_dict = settings.PLUGINS_DICT
        self.server_info = server_info
        self.hostname = self.server_info['basic']['data']['hostname'] if self.server_info['basic']['status'] else None

        #老资产信息，信息未输入时，查询结果为空
        # self.server_obj = models.Server.objects.filter(hostname=self.hostname).first() if self.hostname else None
        # print('--s1',self.server_obj)
        print("--s2",self.hostname)


    def exec_plugin(self):
        """
        获取所有的插件，并执行获取插件返回值
        :return:
        """
        result = []
        print('sele',self.server_info)
        #settings.plugin_dict数据按列表形式存放，首先输入basic的资料
        #防止basic资料没有输入，因basic下的hostname作为唯一标识
        for row in self.plugin_dict:
            for k in row.keys():
                v = row[k][k]
                module_path,class_name = v.rsplit('.',1)#r表示从右往左切，1表示只切一次
                m = importlib.import_module(module_path)
                cls = getattr(m,class_name)#路径下获取类
                if hasattr(cls,'initial'):
                    obj = cls.initial()
                else:
                    obj = cls()#实例化类，创建对象
                print('-->1',obj)
                temp =  obj.process(self.server_info,self.hostname,k)#执行类下的process方法,且传参，即命令
                if temp:
                    result.append(temp)

        #linux上执行的命令
        result = result if result else '没有改变'
        print('-->>',result)
        return result







