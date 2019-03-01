from .base import BasePlugin
#继承方式实现
# class Basic(BasePlugin):
#     def process(self):
#         self.command('xxx')
#         return '123'

class Basic(object):
    """
    获取主机基本信息
    """
    def __init__(self):
        pass

    #执行构造方法之前，可以加点其他操作，可有可无
    #类似预留的钩子
    @classmethod
    def initial(cls):
        return cls()

    def process(self,command_func,debug):
        if debug:
            output = {
                'os_platform':"linux",
                'os_version':"CentOS release 6",
                # 'os_version': "CentOS ii",
                'hostname':'c1.com',
                'sn':'SN01',
                'manufacturer':'你11呀',
                'model':'zzs001',
                'manage_ip':'192.167.1.1',
                'cpu_count':'4',
                'cpu_physical_count':'2',
                'cpu_model':'cpu01',
            }
        else:
            pass
        return output
        # return self.parse(output)

    def parse(self, content):
        pass