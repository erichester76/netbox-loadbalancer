from netbox.plugins import PluginTemplateExtension
from .models import F5PoolNode, F5Cluster

class F5PoolNodeExtension(PluginTemplateExtension):
    def left_page(self):
        object = self.context.get('object')
        f5poolnode = F5PoolNode.objects.filter(**{self.kind:object})
        return self.render('netbox_loadbalancer/inc/f5poolnode_info.html', extra_context={
            'f5poolnode': f5poolnode,
        })
        
class F5DeviceClusterExtension(PluginTemplateExtension):
    def left_page(self):
        object = self.context.get('object')
        f5cluster = F5Cluster.objects.filter(**{self.kind:object})
        return self.render('netbox_loadbalancer/f5devicecluster.html', extra_context={
            'f5cluster': f5cluster,
        })
        
class DeviceF5PoolNodeInfo(F5PoolNodeExtension):
    model = 'dcim.device'
    kind = 'physical_device'

class DeviceF5ClusterInfo(F5DeviceClusterExtension):
    model = 'dcim.device'
    kind = 'physical_device'

template_extensions = (
    DeviceF5PoolNodeInfo,
    DeviceF5ClusterInfo
)
