import os
from lib.conf.config import settings  #导入配置路径（实现自定义配置+默认配置的整合）

class Nic(object):
    """获取主机网卡信息"""
    def __init__(self):
        pass
    #执行构造方法之前，可以加点其他操作，可有可无
    #类似预留的钩子
    @classmethod
    def initial(cls):
        return cls()

    def process(self,command_func,debug):
        # if debug:
        #     output = open(os.path.join(settings.BASEDIR,'files/nic.out'),'r',encoding='utf-8').read()
        #     interfaces_info = self._interfaces_ip(output)
        # else:
        #     interfaces_info = self.linux_interfaces(command_func)

        # self.standard(interfaces_info)
        return "nic11"