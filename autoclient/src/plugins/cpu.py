import os
from lib.conf.config import settings
class Cpu(object):
    """CPU信息"""
    def __init__(self):
        pass
    #执行构造方法之前，可以加点其他操作，可有可无
    #类似预留的钩子
    @classmethod
    def initial(cls):
        return cls()

    def process(self,command_func,debug):
        #settings下默认设置为True
        # if debug:
        #     output = open(os.path.join(settings.BASEDIR,'files/cpuinfo.out'),'r',encoding='utf-8').read()
        # else:
        #     output = command_func("cat /proc/cpuinfo")
        output = {
            "霍普":{"cpu_count":'4',"cpu_physical_count":'3',"cpu_model":'霍普'},
            "喜龙": {"cpu_count": '1', "cpu_physical_count":'2', "cpu_model": '喜龙'},
        }

        return output
        # return self.parse(output)

    def parse(self,content):
        pass