from rest_framework import serializers

from ipam.api.serializers import NestedPrefixSerializer
from netbox.api.serializers import NetBoxModelSerializer, WritableNestedSerializer
from ..models import F5VirtualServer, F5Pool, F5Cluster, F5PoolNode

class F5ClusterSerializer(NetBoxModelSerializer):
    class Meta:
        model = F5Cluster
        fields = [
            'id', 'name', 'physical_device', 'virtual_device', 'describe', 'display', 'comments'
        ]

class F5VirtualServerSerializer(NetBoxModelSerializer):
    class Meta:
        model = F5VirtualServer
        fields = [
            'id', 'cluster', 'name', 'ip', 'port', 'vip_type', 'protocol', 'status', 'owner', 'describe', 'pools', 'display', 'comments'
        ]

class F5PoolSerializer(NetBoxModelSerializer):
    class Meta:
        model = F5Pool
        fields = [
            'id', 'cluster', 'name', 'uri', 'describe', 'display', 'vip', 'status', 'f5_pool_node', 'comments'
        ]


class F5PoolNodeSerializer(NetBoxModelSerializer):
    class Meta:
        model = F5PoolNode
        fields = [
            'id', 'cluster', 'name', 'physical_device', 'virtual_device', 'port', 'pool', 'describe', 'display', 'status', 'comments'
        ]
