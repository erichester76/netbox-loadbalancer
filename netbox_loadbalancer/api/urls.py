from netbox.api.routers import NetBoxRouter
from . import views


app_name = 'netbox_loadbalancer'

router = NetBoxRouter()
router.register('clusters', views.LBClusterViewSet)
router.register('vips', views.LBVirtualServerViewSet)
router.register('pools', views.LBPoolViewSet)
router.register('nodes', views.LBPoolNodeViewSet)

urlpatterns = router.urls
