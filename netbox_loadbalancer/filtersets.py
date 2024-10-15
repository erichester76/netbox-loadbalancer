from netbox.filtersets import NetBoxModelFilterSet
from .models import LBCluster, LBVirtualServer, LBPool, LBPoolNode

class LBClusterFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = LBCluster
        fields = ('name', 'physical_device', 'virtual_device', 'describe')

    def search(self, queryset, name, value):
        return queryset.filter(name__icontains=value)
    
    list_display = ('pk', 'id', 'name', 'physical_device', 'virtual_device', 'describe')

class LBVirtualServerFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = LBVirtualServer
        fields = ('cluster', 'name', 'ip', 'port', 'vip_type', 'owner', 'describe')

    def search(self, queryset, name, value):
        return queryset.filter(name__icontains=value)
    
    list_display = ('pk', 'id', 'name', 'ip', 'port', 'vip_type', 'owner', 'protocol', 'status', 'describe')
    

class LBPoolFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = LBPool
        fields = ('name', 'uri', 'describe', 'vip')

    def search(self, queryset, name, value):
        return queryset.filter(name__icontains=value)
    
    list_display = ('pk', 'id', 'name', 'uri', 'describe', 'vip', 'cluster', 'status')
    

class LBPoolNodeFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = LBPoolNode
        fields = ('name', 'physical_device', 'virtual_device', 'port', 'pool', 'describe', 'cluster', 'status')

    def search(self, queryset, name, value):
        return queryset.filter(name__icontains=value)
    
    list_display = ('pk', 'id', 'name', 'physical_device', 'virtual_device', 'port', 'pool', 'describe', 'cluster', 'status')

    