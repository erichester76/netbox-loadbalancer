from dcim.models.devices import Device
from dcim.tables.devices import DeviceTable
from django.contrib import messages
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _
from netbox.views import generic
from utilities.views import ViewTab, register_model_view
from virtualization.models.virtualmachines import VirtualMachine
from virtualization.tables.virtualmachines import VirtualMachineTable

from . import filtersets, forms, models, tables

#
# LBClusterviews
#

@register_model_view(models.LBCluster, 'devices')
class LBClusterDevicesView(generic.ObjectChildrenView):
    queryset = models.LBCluster.objects.all()
    child_model = Device
    table = DeviceTable
    template_name = 'netbox_loadbalancer_tab_view/cluster_devices.html'
    tab = ViewTab(
        label=_('Devices'),
        badge=lambda obj: obj.physical_device.count(),
        weight=100
    )

    def get_children(self, request, parent):
        device_list = parent.physical_device.all()
        return Device.objects.restrict(request.user, 'view').filter(
            pk__in=[device.pk for device in device_list]
        )


@register_model_view(models.LBCluster, 'virtualdevices')
class LBClusterVirtualDevicesView(generic.ObjectChildrenView):
    queryset = models.LBCluster.objects.all()
    child_model = VirtualMachine
    table = VirtualMachineTable
    template_name = 'netbox_loadbalancer_tab_view/cluster_virtualdevices.html'
    tab = ViewTab(
        label=_('Virtual Device'),
        badge=lambda obj: obj.virtual_device.count(),
        weight=200
    )

    def get_children(self, request, parent):
        vdevice_list = parent.virtual_device.all()
        return VirtualMachine.objects.restrict(request.user, 'view').filter(
            pk__in=[device.pk for device in vdevice_list]
        )


@register_model_view(models.LBCluster, 'vips')
class LBClusterVipsView(generic.ObjectChildrenView):
    queryset = models.LBCluster.objects.all()
    child_model = models.LBVirtualServer
    table = tables.LBVirtualServerTable
    template_name = 'netbox_loadbalancer_tab_view/cluster_pools.html'
    tab = ViewTab(
        label=_('Virtual Endpoint (Vip)'),
        badge=lambda obj: obj.LB_vips.count(),
        weight=300
    )

    def get_children(self, request, parent):
        vip_list = parent.LB_vips.all()
        return models.LBVirtualServer.objects.restrict(request.user, 'view').filter(
            pk__in=[vip.pk for vip in vip_list]
        )


@register_model_view(models.LBCluster, 'pools')
class LBClusterPoolsView(generic.ObjectChildrenView):
    queryset = models.LBCluster.objects.all()
    child_model = models.LBPool
    table = tables.LBPoolTable
    template_name = 'netbox_loadbalancer_tab_view/cluster_pools.html'
    tab = ViewTab(
        label=_('Pools'),
        badge=lambda obj: obj.LB_pools.count(),
        weight=400
    )

    def get_children(self, request, parent):
        pool_list = parent.LB_pools.all()
        return models.LBPool.objects.restrict(request.user, 'view').filter(
            pk__in=[pool.pk for pool in pool_list]
        )
        

@register_model_view(models.LBCluster, 'nodes')
class LBClusterNodesView(generic.ObjectChildrenView):
    queryset = models.LBCluster.objects.all()
    child_model = models.LBPoolNode
    table = tables.LBPoolNodeTable
    template_name = 'netbox_loadbalancer_tab_view/cluster_nodes.html'
    tab = ViewTab(
        label=_('Nodes'),
        badge=lambda obj: obj.LB_nodes.count(),
        weight=500
    )

    def get_children(self, request, parent):
        node_list = parent.LB_nodes.all()
        return models.LBPoolNode.objects.restrict(request.user, 'view').filter(
            pk__in=[node.pk for node in node_list]
        )


class LBClusterView(generic.ObjectView):
    queryset = models.LBCluster.objects.all()
    
    # def get_extra_context(self, request, instance):
    #     physical_devices_table = DeviceTable(instance.physical_device.all())
    #     physical_devices_table.configure(request)
        
    #     virtual_devices_table = VirtualMachineTable(instance.virtual_device.all())
    #     virtual_devices_table.configure(request)
                
    #     vip_table = tables.LBVirtualServerTable(instance.LB_vips.all())
    #     vip_table.configure(request)
        
    #     pool_table = tables.LBPoolTable(instance.LB_pools.all())
    #     pool_table.configure(request)
        
    #     node_table = tables.LBPoolNodeTable(instance.LB_nodes.all())
    #     node_table.configure(request)
        
    #     return {
    #         'physical_devices_table': physical_devices_table,
    #         'virtual_devices_table': virtual_devices_table,
    #         'vip_table': vip_table,
    #         'pool_table': pool_table,
    #         'node_table': node_table,
    #     }


class LBClusterListView(generic.ObjectListView):
    queryset = models.LBCluster.objects.annotate(
        physical_device_count=Count('physical_device', distinct=True),
    ).annotate(
        virtual_device_count=Count('virtual_device', distinct=True)
    )

    table = tables.LBClusterTable
    filterset = filtersets.LBClusterFilterSet
    filterset_form = forms.LBClusterFilterForm


class LBClusterEditView(generic.ObjectEditView):
    queryset = models.LBCluster.objects.all()
    form = forms.LBClusterForm


class LBClusterDeleteView(generic.ObjectDeleteView):
    queryset = models.LBCluster.objects.all()


class LBClusterBulkDeleteView(generic.BulkDeleteView):
    queryset = models.LBCluster.objects.all()
    filterset = filtersets.LBClusterFilterSet
    table = tables.LBClusterTable


#
# LBVirtualServer views
#

class LBVirtualServerView(generic.ObjectView):
    queryset = models.LBVirtualServer.objects.all()
    def get_extra_context(self, request, instance):
        table = tables.LBPoolTable(instance.pools.all())
        table.configure(request)

        return {
            'pools_table': table,
        }


class LBVirtualServerListView(generic.ObjectListView):
    queryset = models.LBVirtualServer.objects.annotate(
        pool_count=Count('pools')
    )
    queryset = models.LBVirtualServer.objects.all()
    table = tables.LBVirtualServerTable
    filterset = filtersets.LBVirtualServerFilterSet
    filterset_form = forms.LBVirtualServerFilterForm


class LBVirtualServerEditView(generic.ObjectEditView):
    queryset = models.LBVirtualServer.objects.all()
    form = forms.LBVirtualServerForm


class LBVirtualServerDeleteView(generic.ObjectDeleteView):
    queryset = models.LBVirtualServer.objects.all()


class LBVirtualServerBulkDeleteView(generic.BulkDeleteView):
    queryset = models.LBVirtualServer.objects.all()
    filterset = filtersets.LBVirtualServerFilterSet
    table = tables.LBVirtualServerTable


@register_model_view(models.LBVirtualServer, 'pools')
class LBVirtualServerPoolsView(generic.ObjectChildrenView):
    queryset = models.LBVirtualServer.objects.all()
    child_model = models.LBPool
    table = tables.LBPoolTable
    template_name = 'netbox_loadbalancer_tab_view/vip_pools.html'
    tab = ViewTab(
        label=_('Pool List'),
        badge=lambda obj: obj.pools.count(),
        weight=100
    )

    def get_children(self, request, parent):
        pool_list = parent.pools.all()
        return models.LBPool.objects.restrict(request.user, 'view').filter(
            pk__in=[pool.pk for pool in pool_list]
        )


@register_model_view(models.LBVirtualServer, 'add_pools', path='pools/add')
class LBVirtualServerAddPoolsView(generic.ObjectEditView):
    queryset = models.LBVirtualServer.objects.all()
    form = forms.LBVirtualServerAddPoolsForm
    template_name = 'netbox_loadbalancer/LBvirtualserver_update_pools.html'

    def get(self, request, pk):
        queryset = self.queryset.filter(pk=pk)
        vip = get_object_or_404(queryset)
        pools = vip.pools.all()
        current_pools = []
        if pools:
            for pool in pools:
                current_pools.append(pool)
        
        initial_data = {
            'cluster': vip.cluster,
            'virtual_server': vip.name,
            'ip': vip.ip.address.ip,
            'port': vip.port,
            'protocol': vip.protocol,
            'vip_type': vip.vip_type,
            'pools': current_pools,
            
        }
        
        form = self.form(initial=initial_data)
                
        return render(request, self.template_name, {
            'vip': vip,
            'form': form,
            'return_url': reverse('plugins:netbox_loadbalancer:LBvirtualserver', kwargs={'pk': pk}),
        })

    def post(self, request, pk):
        queryset = self.queryset.filter(pk=pk)
        vip = get_object_or_404(queryset)
        form = self.form(request.POST)

        if form.is_valid():
            current_pools = vip.pools.all()
            # Remove current pools 
            if current_pools:
                for pool in current_pools:
                    vip.pools.remove(pool)
                    
            # Add pool 
            new_data_pool = form.cleaned_data['pools']
            for newpool in new_data_pool:
                vip.pools.add(newpool)
                
            messages.success(request, f"Success update pools for {vip.name}")
            return redirect(vip.get_absolute_url())

        return render(request, self.template_name, {
            'vip': vip,
            'form': form,
            'return_url': vip.get_absolute_url(),
        })


@register_model_view(models.LBVirtualServer, 'delete_pools', path='pools/delete')
class LBVirtualServerDeletePoolsView(generic.ObjectEditView):
    queryset = models.LBVirtualServer.objects.all()
    form = forms.LBVirtualServerDeletePoolsForm
    template_name = 'netbox_loadbalancer/LBvirtualserver_delete_pools.html'

    def post(self, request, pk):

        vip = get_object_or_404(self.queryset, pk=pk)
        
        if '_confirm' in request.POST:
            form = self.form(request.POST)
            pool_pks = request.POST.getlist('pk')
            with transaction.atomic():
                for pool in models.LBPool.objects.filter(pk__in=pool_pks):
                    vip.pools.remove(pool)
                    vip.save()

            messages.success(request, "Removed {} pools from {}".format(
                len(pool_pks), vip
            ))
            return redirect(reverse('plugins:netbox_loadbalancer:LBvirtualserver_pools', kwargs={'pk': pk}))
        else:
            form = self.form(request.POST, initial={'pk': request.POST.getlist('pk')})
        pk_values = form.initial.get('pk', [])
        selected_objects = models.LBPool.objects.filter(pk__in=pk_values)
        pool_table = tables.LBPoolTable(list(selected_objects), orderable=False)

        return render(request, self.template_name, {
            'form': form,
            'parent_obj': vip,
            'table': pool_table,
            'obj_type_plural': 'pools',
            'return_url': reverse('plugins:netbox_loadbalancer:LBvirtualserver_pools', kwargs={'pk': pk})
        })
        

#
# LBPool views
#

class LBPoolView(generic.ObjectView):
    queryset = models.LBPool.objects.all()
    def get_extra_context(self, request, instance):
        table = tables.LBPoolNodeTable(instance.LB_pool_node.all())
        table.configure(request)

        return {
            'nodes_table': table,
        }   


class LBPoolListView(generic.ObjectListView):
    # queryset = models.LBPool.objects.annotate(
    #     node_count=Count('LB_pool_node')
    # )
    queryset = models.LBPool.objects.all()
    table = tables.LBPoolTable
    filterset = filtersets.LBPoolFilterSet
    filterset_form = forms.LBPoolFilterForm


class LBPoolEditView(generic.ObjectEditView):
    queryset = models.LBPool.objects.all()
    form = forms.LBPoolForm


class LBPoolDeleteView(generic.ObjectDeleteView):
    queryset = models.LBPool.objects.all()


class LBPoolBulkDeleteView(generic.BulkDeleteView):
    queryset = models.LBPool.objects.all()
    filterset = filtersets.LBPoolFilterSet
    table = tables.LBPoolTable

@register_model_view(models.LBPool, 'nodes')
class LBPoolNodesView(generic.ObjectChildrenView):
    queryset = models.LBPool.objects.all()
    child_model = models.LBPoolNode
    table = tables.LBPoolNodeTable
    template_name = 'netbox_loadbalancer_tab_view/pool_nodes.html'
    tab = ViewTab(
        label=_('Nodes List'),
        badge=lambda obj: obj.LB_pool_node.count(),
        weight=100
    )

    def get_children(self, request, parent):
        node_list = parent.LB_pool_node.all()
        return models.LBPoolNode.objects.restrict(request.user, 'view').filter(
            pk__in=[node.pk for node in node_list]
        )


@register_model_view(models.LBPool, 'add_nodes', path='nodes/add')
class LBPoolAddNodesView(generic.ObjectEditView):
    queryset = models.LBPool.objects.all()
    form = forms.LBPoolAddNodesForm
    template_name = 'netbox_loadbalancer/LBpool_update_nodes.html'

    def get(self, request, pk):
        queryset = self.queryset.filter(pk=pk)
        pool = get_object_or_404(queryset)
        nodes = pool.LB_pool_node.all()
        current_nodes = []
        if nodes:
            for node in nodes:
                current_nodes.append(node)
        
        initial_data = {
            'cluster': pool.cluster,
            'name': pool.name,
            'uri': pool.uri,
            'nodes': nodes,
        }
        
        form = self.form(initial=initial_data)
                
        return render(request, self.template_name, {
            'pool': pool,
            'form': form,
            'return_url': reverse('plugins:netbox_loadbalancer:LBpool', kwargs={'pk': pk}),
        })

    def post(self, request, pk):
        queryset = self.queryset.filter(pk=pk)
        pool = get_object_or_404(queryset)
        form = self.form(request.POST)

        if form.is_valid():
            current_nodes = pool.LB_pool_node.all()
            # Remove current pools 
            if current_nodes:
                for node in current_nodes:
                    pool.LB_pool_node.remove(node)
                    
            # Add pool 
            new_data_node = form.cleaned_data['nodes']
            for newnode in new_data_node:
                pool.LB_pool_node.add(newnode)
                
            messages.success(request, f"Success update nodes for {pool.name}")
            return redirect(pool.get_absolute_url())

        return render(request, self.template_name, {
            'vip': pool,
            'form': form,
            'return_url': pool.get_absolute_url(),
        })


@register_model_view(models.LBPool, 'delete_nodes', path='nodes/delete')
class LBPoolDeleteNodesView(generic.ObjectEditView):
    queryset = models.LBPool.objects.all()
    form = forms.LBPoolDeleteNodesForm
    template_name = 'netbox_loadbalancer/LBpool_delete_nodes.html'

    def post(self, request, pk):

        pool = get_object_or_404(self.queryset, pk=pk)
        
        if '_confirm' in request.POST:
            form = self.form(request.POST)
            node_pks = request.POST.getlist('pk')
            with transaction.atomic():
                for node in models.LBPoolNode.objects.filter(pk__in=node_pks):
                    pool.LB_pool_node.remove(node)
                    pool.save()

            messages.success(request, "Removed {} nodes from {}".format(
                len(node_pks), pool
            ))
            return redirect(reverse('plugins:netbox_loadbalancer:LBpool_nodes', kwargs={'pk': pk}))
        else:
            form = self.form(request.POST, initial={'pk': request.POST.getlist('pk')})
        pk_values = form.initial.get('pk', [])
        selected_objects = models.LBPoolNode.objects.filter(pk__in=pk_values)
        node_table = tables.LBPoolNodeTable(list(selected_objects), orderable=False)

        return render(request, self.template_name, {
            'form': form,
            'parent_obj': pool,
            'table': node_table,
            'obj_type_plural': 'nodes',
            'return_url': reverse('plugins:netbox_loadbalancer:LBpool_nodes', kwargs={'pk': pk})
        })
        


#
# LBPoolNode views
#

class LBPoolNodeView(generic.ObjectView):
    queryset = models.LBPoolNode.objects.all()


class LBPoolNodeListView(generic.ObjectListView):
    queryset = models.LBPoolNode.objects.all()
    table = tables.LBPoolNodeTable
    filterset = filtersets.LBPoolNodeFilterSet
    filterset_form = forms.LBPoolNodeFilterForm


class LBPoolNodeEditView(generic.ObjectEditView):
    queryset = models.LBPoolNode.objects.all()
    form = forms.LBPoolNodeForm
    template_name = 'netbox_loadbalancer/LBpoolnode_edit.html'


class LBPoolNodeDeleteView(generic.ObjectDeleteView):
    queryset = models.LBPoolNode.objects.all()
    
    
class LBPoolNodeBulkDeleteView(generic.BulkDeleteView):
    queryset = models.LBPoolNode.objects.all()
    filterset = filtersets.LBPoolFilterSet
    table = tables.LBPoolNodeTable
