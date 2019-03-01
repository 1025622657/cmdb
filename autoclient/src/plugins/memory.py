import os
from lib.conf.config import settings  #导入配置路径（实现自定义配置+默认配置的整合）

class Memory(object):
    """
    获取主机内存信息
    """
    def __init__(self):
        pass

    # 执行构造方法之前，可以加点其他操作，可有可无
    # 类似预留的钩子
    @classmethod
    def initial(cls):
        return cls()

    def process(self, command_func, debug):
        #调试模式
        # if debug:
        #     output = open(os.path.join(settings.BASEDIR, 'files/memory.out'), 'r', encoding='utf-8').read()
        # #linux上执行命令
        # else:
        #     output = command_func("sudo dmidecode -p -t 17 2>/dev/null")
        return "memory11"
        # return self.parse(output)

    #正则过滤，获取匹配信息
    def parse(self, content):
        pass