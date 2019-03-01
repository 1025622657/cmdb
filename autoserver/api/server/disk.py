from repository import models
from django.shortcuts import HttpResponse,redirect,render
import json
class Disk(object):
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


        # ###############处理硬盘信息###############
        server_obj = models.Server.objects.filter(hostname=hostname).first()

        # 添加错误日志
        temp = '[%s]服务器采集[%s]信息错误'%(hostname if hostname else 'AGENT',k)
        if not server_info['disk']['status']:
            models.ErrorLog.objects.create(content=server_info['disk']['data'],
                                           asset_obj=server_obj.asset if server_obj else None,
                                           title=temp)
            print("----disk",temp)
            return temp

        info = []
        new_disk_dict = server_info['disk']['data']
        print("--ndisk", new_disk_dict)
        """
        {
            5:{'slot':5,capacity:452...},
            3:{'slot':3,capacity:452...},
        }
        """
        old_disk_list = models.Disk.objects.filter(server_obj=server_obj)
        """
        [
            Disk('slot':5,capacity:465...),
            Disk('slot':4,capacity:465...),
        ]
        #槽位是唯一的
        """
        # 交集：5，创建：3，删除：4
        new_slot_list = list(new_disk_dict.keys())
        old_slot_list = []
        for item in old_disk_list:
            old_slot_list.append(item.slot)

        # 交集：更新[5,]
        update_list = set(new_slot_list).intersection(old_slot_list)
        # 差集：创建[3]
        create_list = set(new_slot_list).difference(old_slot_list)
        # 差集：删除[4]
        del_list = set(old_slot_list).difference(new_slot_list)
        if del_list:
            # 删除
            models.Disk.objects.filter(server_obj=server_obj, slot__in=del_list).delete()
            temp = '服务器[%s],删除[%s]里的[%s]'%(hostname,k,del_list)
            info.append(temp)
            # 记录日志
            models.AssetRecord.objects.create(asset_obj=server_obj.asset, content="移除硬盘:%s" % ('、'.join(del_list),))

        # 增加
        record_list = []
        for slot in create_list:
            disk_dict = new_disk_dict[slot]
            disk_dict['server_obj'] = server_obj
            models.Disk.objects.create(**disk_dict)
            temp = "服务器{server},{disk}新增硬盘:槽位:{slot}，容量:{capacity}，型号:{model},类型:{pd_type}".format(server=hostname,disk=k,**disk_dict)
            info.append(temp)
            record_list.append(temp)
        if record_list:
            content = ";".join(record_list)
            models.AssetRecord.objects.create(asset_obj=server_obj.asset, content=content)
        # ###########更新##########
        record_list = []
        row_map = {'capacity': '容量', 'pd_type': '类型', 'model': '型号'}
        for slot in update_list:
            new_disk_row = new_disk_dict[slot]
            ol_disk_row = models.Disk.objects.filter(slot=slot, server_obj=server_obj).first()
            for key, v in new_disk_row.items():
                value = getattr(ol_disk_row, key)
                if v != value:
                    temp = "服务器[%s],[%s]里的槽位为[%s]的,[%s]由[%s]变更为[%s]" % (hostname,k,slot, key, value, v)
                    record_list.append(temp)
                    info.append(temp)
                    setattr(ol_disk_row, key, v)
            ol_disk_row.save()
        if record_list:
            content = ";".join(record_list)
            models.AssetRecord.objects.create(asset_obj=server_obj.asset, content=content)
        if info:
            return info
