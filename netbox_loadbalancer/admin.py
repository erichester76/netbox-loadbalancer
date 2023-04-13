from django.contrib import admin
from .models import F5Cluster, F5VirtualServer, F5Pool


# @admin.register(F5Cluster)
# class F5ClusterAdmin(admin.ModelAdmin):
#     list_display = ('pk', 'id', 'name', 'physical_device', 'virtual_device', 'describe')

# @admin.register(F5VirtualServer)
# class F5VirtualServerAdmin(admin.ModelAdmin):
#     list_display = ('pk', 'id', 'cluster', 'name', 'ip', 'port', 'vip_type', 'owner', 'protocol', 'status', 'describe')
    
# @admin.register(F5Pool)
# class F5VirtualServerAdmin(admin.ModelAdmin):
#     list_display = ('pk', 'id', 'name', 'uri', 'describe', 'vip')

