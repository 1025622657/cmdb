from repository import models
from django.shortcuts import HttpResponse,redirect,render
import json
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

    def process(self,server_info,hostname,k):
        server_obj = models.Server.objects.filter(hostname=hostname).first()

        # ###############处理服务器信息###############
        if not server_info['basic']['status']:
            temp = '[%s]服务器采集[%s]信息错误'%(hostname if hostname else 'AGENT',k)
            models.ErrorLog.objects.create(content=server_info['basic']['data'],
                                           asset_obj=server_obj.asset if server_obj else None,
                                           title=temp)
            return temp

        else:
            info = []
            new_basic_dict = server_info['basic']['data']
            #老资产信息
            # server_obj = models.Server.objects.filter(hostname=hostname).first()
            record_list = []
            if not server_obj:
                #添加，
                asset_obj = models.Asset.objects.filter(device_type_id=1,
                                                        device_status_id=1,
                                                        server__hostname__isnull=True).first()
                new_basic_dict['asset'] = asset_obj
                temp = '服务器[%s],[%s]信息添加成功'%(hostname,k)
                info.append(temp)
                server_obj = models.Server.objects.create(**new_basic_dict)
            else:
                #更新
                for key, v in new_basic_dict.items():
                    value = str(getattr(server_obj, key))
                    if v.strip() != value.strip():
                        setattr(server_obj, key, v)
                        temp = '服务器[%s],[%s]信息，[%s]字段由[%s]变更为[%s]' % (hostname,k,key,value,v)
                        info.append(temp)
                        record_list.append(temp)
                    server_obj.save()
                if record_list:
                    content =  ';'.join(record_list)
                    asset_obj = server_obj.asset
                    models.AssetRecord.objects.create(content=content,asset_obj=asset_obj)
            if info:
                return info

