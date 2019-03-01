from Crypto.Cipher import AES
from django.conf import settings
import time
import json
import hashlib
import requests
# ######################加密################
#chr(32) ord(' ')
def encrypt(message):
    """
    数据加密，按16个字节的倍数进行加密
    :param message:字符类型
    :return:字节类型
    """
    # 加密时数据长度需为16的倍数,如:DATA_KEY = b'dfdsdfsasdfdsdfs'
    key = settings.DATA_KEY

    #创建一个对象
    cipher = AES.new(key, AES.MODE_CBC, key)

    # bytearray为可变字节数组，只能加数字
    #加密时数据长度需为16的倍数,如:DATA_KEY = b'dfdsdfsasdfdsdfs'
    bmessage = bytearray(message, encoding='utf-8')#bytearray为可变字节数组,
    v1 = len(bytes(message, encoding='utf-8'))#字符转字节
    v2 = v1 % 16 #（v2为余数）

    #或刚好16个字节，则也加16个16，这样方便后面解密
    #组合成16的倍数
    if v2 == 0:
        v3 = 16
    else:
        v3 = 16 - v2
    for i in range(v3):

        #通过添加空格或添加几个几数字，解决16的倍数的位数问题
        # bmessage.append(32)#32表示空格，一个空格一个字节，
        #注：添加n个数字较好，便于解密处理，
        # 加空格则有可以数据本身就有空格，则造成数据不一致

        bmessage.append(v3)#后面添加加几个几，

    #data表示要加密的字符串，需是16个字节或16个字节的倍数
    msg = cipher.encrypt(bmessage)
    return msg


# ######################解密################
def decrypt(message):
    """
    数据解密，按16个字节的倍数进行解密
    :param message:字节
    :return:字符
    """
    from Crypto.Cipher import AES
    key = settings.DATA_KEY
    cipher = AES.new(key, AES.MODE_CBC, key)
    result = cipher.decrypt(message)#解密字节
    #result[-1]表示最后一个字节，即几个几，如5个5
    #result[0:-5]即表示只获取有效的字节

    result = result[0:-result[-1]]#字节类型
    return result.decode('utf-8')

    #strip()方式可以不准确，有可以数据里原来有空格
    # return result.decode('utf-8').strip()



#json会序列化再发过去
# response = requests.post(url="http://127.0.0.1:8000/api/asset.html",headers={'OpenKey':auth()},json={'v1':'k1'})


#字符串unicode,至少16位表示一个字符，传输的时候会把字符串压缩成字节（requests会帮助转换），再进行传输
#也可以转成字节再进行传输，
# v1 = json.dumps({'v1':'k1'})
# v1 = bytes(json.dumps({'v1':'k1'}),encoding='utf-8')

#加密传输
# v1 = encrypt(json.dumps({'k1':'v1','k2':'abcdef'}))
# print(v1)
#
# response = requests.post(url="http://127.0.0.1:8000/api/asset.html",
#                          headers={'OpenKey':auth(),'Content-Type':'application/json'},
#                          data=v1)
# print(response.text)


