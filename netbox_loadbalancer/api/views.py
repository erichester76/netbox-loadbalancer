from django.db.models import Count

from netbox.api.viewsets import NetBoxModelViewSet

from .. import filtersets, models
from .serializers import LBClusterSerializer, LBVirtualServerSerializer, LBPoolSerializer, LBPoolNodeSerializer

class LBClusterViewSet(NetBoxModelViewSet):
    queryset = models.LBCluster.objects.all()
    serializer_class = LBClusterSerializer

class LBVirtualServerViewSet(NetBoxModelViewSet):
    queryset = models.LBVirtualServer.objects.all()
    serializer_class = LBVirtualServerSerializer

class LBPoolViewSet(NetBoxModelViewSet):
    queryset = models.LBPool.objects.all()
    serializer_class = LBPoolSerializer

class LBPoolNodeViewSet(NetBoxModelViewSet):
    queryset = models.LBPoolNode.objects.all()
    serializer_class = LBPoolNodeSerializer
