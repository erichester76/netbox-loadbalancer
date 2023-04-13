from netbox.filtersets import NetBoxModelFilterSet
from .models import F5Cluster, F5VirtualServer, F5Pool, F5PoolNode

class F5ClusterFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = F5Cluster
        fields = ('name', 'physical_device', 'virtual_device', 'describe')

    def search(self, queryset, name, value):
        return queryset.filter(name__icontains=value)
    
    list_display = ('pk', 'id', 'name', 'physical_device', 'virtual_device', 'describe')

class F5VirtualServerFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = F5VirtualServer
        fields = ('cluster', 'name', 'ip', 'port', 'vip_type', 'owner', 'describe')

    def search(self, queryset, name, value):
        return queryset.filter(name__icontains=value)
    
    list_display = ('pk', 'id', 'name', 'ip', 'port', 'vip_type', 'owner', 'protocol', 'status', 'describe')
    

class F5PoolFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = F5Pool
        fields = ('name', 'uri', 'describe', 'vip')

    def search(self, queryset, name, value):
        return queryset.filter(name__icontains=value)
    
    list_display = ('pk', 'id', 'name', 'uri', 'describe', 'vip', 'cluster', 'status')
    

class F5PoolNodeFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = F5PoolNode
        fields = ('name', 'physical_device', 'virtual_device', 'port', 'pool', 'describe', 'cluster', 'status')

    def search(self, queryset, name, value):
        return queryset.filter(name__icontains=value)
    
    list_display = ('pk', 'id', 'name', 'physical_device', 'virtual_device', 'port', 'pool', 'describe', 'cluster', 'status')

    