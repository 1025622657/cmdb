from repository import models
from django.shortcuts import HttpResponse,redirect,render
import json
class Cpu(object):
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
        print('---0',hostname,k,server_info)
        server_obj = models.Server.objects.filter(hostname=hostname).first()
        temp = '[%s]服务器，采集[%s]信息错误'%(hostname if hostname else 'AGENT',k)
        if not server_info['cpu']['status']:
            models.ErrorLog.objects.create(content=server_info['cpu']['data'],
                                           asset_obj=server_obj.asset if server_obj else None,
                                           title=temp)
            return temp

        #如果server_obj不为真，则重新查询，因basic会先执行，即已经添加了该数据
        info = []
        new_cpu_dict = server_info['cpu']['data']
        ol_cpu_list = models.Cpu.objects.filter(server_obj=server_obj)
        new_cpu_model_list =  list(new_cpu_dict.keys())
        ol_cpu_model_list = [item.cpu_model for item in ol_cpu_list ]

        #修改
        record_list = []
        update_cpu_list = set(new_cpu_model_list).intersection(ol_cpu_model_list)
        print("--交集update",update_cpu_list)

        for row in update_cpu_list:
            new_cpu_row = new_cpu_dict[row]
            old_cpu_row = models.Cpu.objects.filter(cpu_model=row,server_obj=server_obj).first()
            for key,v in new_cpu_row.items():
                value = getattr(old_cpu_row,key)
                if v != value:
                    setattr(old_cpu_row,key,v)
                    temp = '服务器[%s],变更[%s]下的信息，[%s]内容，由[%s]变更为[%s]'%(hostname,k,key,value,v)
                    info.append(temp)
                    record_list.append(temp)
                old_cpu_row.save()
        if record_list:
            content = ';'.join(record_list)
            asset_obj = server_obj.asset
            models.AssetRecord.objects.create(content=content,asset_obj=asset_obj)
            print("--rec",record_list)

        #增加
        record_list = []
        create_cpu_list = set(new_cpu_model_list).difference(ol_cpu_model_list)
        print("---差集add",create_cpu_list)
        for model in create_cpu_list:
            cpu_disk = new_cpu_dict[model]
            cpu_disk['server_obj'] = server_obj

            models.Cpu.objects.create(**cpu_disk)
            temp = '服务器{hostname},新增{cpu}信息，cpu数量:{cpu_count},物理核心数:{cpu_physical_count},型号:{cpu_model}'.format(hostname=hostname,cpu=k,**cpu_disk)
            info.append(temp)
            record_list.append(temp)

        if record_list:
            content = ';'.join(record_list)
            asset_obj = server_obj.asset
            models.AssetRecord.objects.create(content=content,asset_obj=asset_obj)
            print("--re",record_list)

        #删除
        del_cpu_list = set(ol_cpu_model_list).difference(new_cpu_model_list)
        if del_cpu_list:
            temp = '服务器[%s],删除[%s]里的[%s]'%(hostname,k,del_cpu_list)
            info.append(temp)
        print("---差集del", del_cpu_list)
        models.Cpu.objects.filter(cpu_model__in=del_cpu_list).delete()


        if info:
            return info
