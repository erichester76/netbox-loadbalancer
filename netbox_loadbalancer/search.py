from netbox.search import SearchIndex, register_search
from .models import F5Cluster, F5VirtualServer, F5Pool, F5PoolNode


@register_search
class F5ClusterIndex(SearchIndex):
    model = F5Cluster
    fields = (
        ('name', 100),
        ('physical_device', 200),
        ('virtual_device', 200),
        ('describe', 200),
    )


@register_search
class F5VirtualServerIndex(SearchIndex):
    model = F5VirtualServer
    fields = (
        ('name', 100),
        ('cluster', 200),
        ('protocol', 200),
        ('status', 200),
        ('ip', 200),
        ('port', 200),
        ('vip_type', 200),
        ('owner', 200),
        ('describe', 5000)
    )


@register_search
class F5PoolIndex(SearchIndex):
    model = F5Pool
    fields = (
        ('name', 100),
        ('vip', 100),
        ('uri', 200),
        ('describe', 5000),
        ('cluster', 200),
        ('status', 200)
    )

@register_search
class F5PoolNodeIndex(SearchIndex):
    model = F5PoolNode
    fields = (
        ('name', 100),
        ('pool', 100),
        ('physical_device', 200),
        ('virtual_device', 200),
        ('port', 200),
        ('describe', 5000),
        ('cluster', 200),
        ('status', 200)
    )

    