from netbox.search import SearchIndex, register_search
from .models import LBCluster, LBVirtualServer, LBPool, LBPoolNode


@register_search
class LBClusterIndex(SearchIndex):
    model = LBCluster
    fields = (
        ('name', 100),
        ('physical_device', 200),
        ('virtual_device', 200),
        ('describe', 200),
    )


@register_search
class LBVirtualServerIndex(SearchIndex):
    model = LBVirtualServer
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
class LBPoolIndex(SearchIndex):
    model = LBPool
    fields = (
        ('name', 100),
        ('vip', 100),
        ('uri', 200),
        ('describe', 5000),
        ('cluster', 200),
        ('status', 200)
    )

@register_search
class LBPoolNodeIndex(SearchIndex):
    model = LBPoolNode
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

    