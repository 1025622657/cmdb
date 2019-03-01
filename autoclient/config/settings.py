"""
用户自定义配置文件
"""
import os

#Agent,Salt,SSH三种方式可选
MODE = 'AGENT'#SALT,SSH

#SSH连接时，需要传递的参数，可以以用户名密码连接或私钥连接
SSH_USER = 'root'
SSH_PWD = '123'
SSH_KEY = '/xx/xx/xx'#私钥路径
SSH_PORT = 22

#调试用
DEBUG = True

#当前执行文件路径
BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#可插拔实现的配置，.py文件放在哪都可以，
#只要把路径按如下方式输入即可（路径+类）
PLUGINS_DICT = {
    'basic':"src.plugins.basic.Basic",
    'cpu':"src.plugins.cpu.Cpu",
    'disk':"src.plugins.disk.Disk",
    # 'memory':"src.plugins.memory.Memory",
    # 'board':"src.plugins.board.Board",
    # 'nic':"src.plugins.nic.Nic",
    # 'fff':"src.xx.x1",
}


API = "http://127.0.0.1:8000/api/asset.html"

#Agent验证方式之文件路径，以文件为主，主机名做唯一标识
CERT_PATH = os.path.join(BASEDIR,'config','cert')


#AES加密的key,需为16个字节的倍数
DATA_KEY = b'dfdsdfsasdfdsdfs'

#API验证的key
API_KEY = 'abcdefsge'