import os
import sys
BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASEDIR)

#只在当前运行程序的环境变量添加，在配置自定义配置时获取到路径
os.environ['USER_SETTINGS'] = "config.settings"
# print(os.environ)#公共的值

from lib.conf.config import settings
# print(settings.USER,settings.EMAIL)
from src import script
from src.plugins import PluginManager

if __name__ == '__main__':
    script.run()

