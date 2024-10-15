from rest_framework import serializers

from ipam.api.serializers import PrefixSerializer
from netbox.api.serializers import NetBoxModelSerializer, WritableNestedSerializer
from ..models import LBVirtualServer, LBPool, LBCluster, LBPoolNode

class LBClusterSerializer(NetBoxModelSerializer):
    class Meta:
        model = LBCluster
        fields = [
            'id', 'name', 'physical_device', 'virtual_device', 'describe', 'display', 'comments'
        ]

class LBVirtualServerSerializer(NetBoxModelSerializer):
    class Meta:
        model = LBVirtualServer
        fields = [
            'id', 'cluster', 'name', 'ip', 'port', 'vip_type', 'protocol', 'status', 'owner', 'describe', 'pools', 'display', 'comments'
        ]

class LBPoolSerializer(NetBoxModelSerializer):
    class Meta:
        model = LBPool
        fields = [
            'id', 'cluster', 'name', 'uri', 'describe', 'display', 'vip', 'status', 'LB_pool_node', 'comments'
        ]


class LBPoolNodeSerializer(NetBoxModelSerializer):
    class Meta:
        model = LBPoolNode
        fields = [
            'id', 'cluster', 'name', 'physical_device', 'virtual_device', 'port', 'pool', 'describe', 'display', 'status', 'comments'
        ]
