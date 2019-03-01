import os
from lib.conf.config import settings  #导入配置路径（实现自定义配置+默认配置的整合）
class Disk(object):
    """
    获取主机磁盘信息
    """
    def __init__(self):
        pass
    
    #执行构造方法之前，可以加点其他操作，可有可无
    #类似预留的钩子
    @classmethod
    def initial(cls):
        return cls()
    
    def process(self,command_func,debug):
        #调试模式
        # if debug:
        #     output = open(os.path.join(settings.BASEDIR,'files/cpuinfo.out'),'r',encoding='utf-8').read()
        # #linux上的命令
        # else:
        #     output = command_func("sudo MegaCli -PDList -aAll")

        output = {
            "2":{"slot":'2','capacity':'245.365','pd_type':'SAS','model':'SAEG ST0001 SDDD'},
            "3": {"slot": '3', 'capacity': '245.363', 'pd_type': 'SSSS', 'model': 'SAEG STGGG'},
            "4": {"slot": '4', 'capacity': '245.364', 'pd_type': 'SASj', 'model': 'SAEG ST0003'},
        }

        return output
        # return self.parse(output)

    #正则过滤，获取匹配信息
    def parse(self,content):
        """
        解析shell命令返回结果
        :param content:shell 命令结果
        :return:解析后的结果
        """
        response = {}
        result = []
        for row_line in content.split("\n\n\n\n"):
            result.append(row_line)
        for item in result:
            temp_dict = {}
            for row in item.split('\n'):
                if not row.strip():
                    continue
