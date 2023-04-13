from django.db.models import Count

from netbox.api.viewsets import NetBoxModelViewSet

from .. import filtersets, models
from .serializers import F5ClusterSerializer, F5VirtualServerSerializer, F5PoolSerializer, F5PoolNodeSerializer

class F5ClusterViewSet(NetBoxModelViewSet):
    queryset = models.F5Cluster.objects.all()
    serializer_class = F5ClusterSerializer

class F5VirtualServerViewSet(NetBoxModelViewSet):
    queryset = models.F5VirtualServer.objects.all()
    serializer_class = F5VirtualServerSerializer

class F5PoolViewSet(NetBoxModelViewSet):
    queryset = models.F5Pool.objects.all()
    serializer_class = F5PoolSerializer

class F5PoolNodeViewSet(NetBoxModelViewSet):
    queryset = models.F5PoolNode.objects.all()
    serializer_class = F5PoolNodeSerializer
