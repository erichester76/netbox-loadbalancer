from netbox.plugins import PluginTemplateExtension
from .models import LBPoolNode, LBCluster

class LBPoolNodeExtension(PluginTemplateExtension):
    def left_page(self):
        object = self.context.get('object')
        LBpoolnode = LBPoolNode.objects.filter(**{self.kind:object})
        return self.render('netbox_loadbalancer/inc/LBpoolnode_info.html', extra_context={
            'LBpoolnode': LBpoolnode,
        })
        
class LBDeviceClusterExtension(PluginTemplateExtension):
    def left_page(self):
        object = self.context.get('object')
        LBcluster = LBCluster.objects.filter(**{self.kind:object})
        return self.render('netbox_loadbalancer/inc/LBdevicecluster.html', extra_context={
            'LBcluster': LBcluster,
        })
        
class DeviceLBPoolNodeInfo(LBPoolNodeExtension):
    model = 'dcim.device'
    kind = 'physical_device'

class DeviceLBClusterInfo(LBDeviceClusterExtension):
    model = 'dcim.device'
    kind = 'physical_device'

template_extensions = (
    DeviceLBPoolNodeInfo,
    DeviceLBClusterInfo
)
