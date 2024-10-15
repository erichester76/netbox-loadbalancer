from django.contrib import admin
from .models import LBCluster, LBVirtualServer, LBPool


# @admin.register(LBCluster)
# class LBClusterAdmin(admin.ModelAdmin):
#     list_display = ('pk', 'id', 'name', 'physical_device', 'virtual_device', 'describe')

# @admin.register(LBVirtualServer)
# class LBVirtualServerAdmin(admin.ModelAdmin):
#     list_display = ('pk', 'id', 'cluster', 'name', 'ip', 'port', 'vip_type', 'owner', 'protocol', 'status', 'describe')
    
# @admin.register(LBPool)
# class LBVirtualServerAdmin(admin.ModelAdmin):
#     list_display = ('pk', 'id', 'name', 'uri', 'describe', 'vip')

