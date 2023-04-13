from netbox.api.routers import NetBoxRouter
from . import views


app_name = 'netbox_loadbalancer'

router = NetBoxRouter()
router.register('clusters', views.F5ClusterViewSet)
router.register('vips', views.F5VirtualServerViewSet)
router.register('pools', views.F5PoolViewSet)
router.register('nodes', views.F5PoolNodeViewSet)

urlpatterns = router.urls
