import importlib
import traceback #错误的堆栈
from lib.conf.config import settings  #导入配置路径（实现自定义配置+默认配置的整合）
class PluginManager(object):
    def __init__(self,hostname=None):
        self.hostname = hostname #可为空，即根据mode选择是否传参，Agent不传，ssh/salt均传
        self.plugin_dict = settings.PLUGINS_DICT
        self.mode = settings.MODE
        self.debug = settings.DEBUG
        #单独对SSH模式的实例化参数处理
        if self.mode == "SSH":
            self.ssh_user = settings.SSH_USER #用户名
            self.ssh_pwd = settings.SSH_PWD #密码
            self.ssh_port = settings.SSH_PORT #端口
            self.ssh_key = settings.SSH_KEY #私钥

    def exec_plugin(self):
        """
        获取所有的插件，并执行获取插件返回值
        :return:
        """
        response = {}
        for k,v in self.plugin_dict.items():

            ret = {"status":True,"data":None}
            try:
                module_path,class_name = v.rsplit('.',1)#r表示从右往左切，1表示只切一次
                m = importlib.import_module(module_path)
                cls = getattr(m,class_name)#路径下获取类
                if hasattr(cls,'initial'):
                    obj = cls.initial()
                else:
                    obj = cls()#实例化类，创建对象

                #linux上执行的命令
                result = obj.process(self.command,self.debug)#执行类下的process方法,且传参，即命令
                print("====================",result)
                ret['data'] = result

            except Exception as e:
                ret['status'] = False
                #那台主机，那个插件，出现的错误信息,通过traceback错误的堆栈返回错误信息
                #应用场景，后台管理
                ret['data'] = "[%s][%s] 采集数据出现错误：%s"%(self.hostname if self.hostname else "AGENT",k,traceback.format_exc())
            response[k] = ret
        return response

    def command(self,cmd):
        if self.mode == "AGENT":
            return self.__agent(cmd)
        elif self.mode == "SSH":
            return self.__ssh(cmd)
        elif self.mode == "SALT":
            return self.__salt(cmd)
        else:
            raise Exception("模式只能是AGENT/SSH/SALT")

    #私有方法
    def __agent(self,cmd):
        import subprocess
        output = subprocess.getoutput(cmd)
        return output
    def __salt(self,cmd):
        #python2使用，salt只支持到python2,不支持python3
        # import salt.client
        # local = salt.client.LocalClient()
        # result = local.cmd(self.hostname,'cmd.run',[cmd])
        # return result[self.hostname]

        #python3使用
        salt_cmd = "salt '%s' cmd.run '%s'"%(self.hostname,cmd,)
        import subprocess
        output = subprocess.getoutput(salt_cmd)
        return output

    def __ssh(self,cmd):
        import paramiko
        # #私钥连接
        # private_key = paramiko.RSAKey.from_private_key_file(self.ssh_key)
        # ssh = paramiko.SSHClient()
        # # 允许连接不在know_hosts文件中的主机，可不加
        # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # ssh.connect(hostname=self.hostname, port=self.ssh_port, username=self.ssh_user, pkey=private_key)
        # stdin, stdout, stderr = ssh.exec_command(cmd)
        # result = stdout.read()
        # ssh.close()
        # return result

        #用户名密码登录
        ssh = paramiko.SSHClient()
        # 允许连接不在know_hosts文件中的主机，可不加
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.hostname, port=self.ssh_port, username=self.ssh_user, password=self.ssh_pwd)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        result = stdout.read()
        ssh.close()
        return result

