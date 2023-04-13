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
# F5Clusterviews
#

@register_model_view(models.F5Cluster, 'devices')
class F5ClusterDevicesView(generic.ObjectChildrenView):
    queryset = models.F5Cluster.objects.all()
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


@register_model_view(models.F5Cluster, 'virtualdevices')
class F5ClusterVirtualDevicesView(generic.ObjectChildrenView):
    queryset = models.F5Cluster.objects.all()
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


@register_model_view(models.F5Cluster, 'vips')
class F5ClusterVipsView(generic.ObjectChildrenView):
    queryset = models.F5Cluster.objects.all()
    child_model = models.F5VirtualServer
    table = tables.F5VirtualServerTable
    template_name = 'netbox_loadbalancer_tab_view/cluster_pools.html'
    tab = ViewTab(
        label=_('Virtual Endpoint (Vip)'),
        badge=lambda obj: obj.f5_vips.count(),
        weight=300
    )

    def get_children(self, request, parent):
        vip_list = parent.f5_vips.all()
        return models.F5VirtualServer.objects.restrict(request.user, 'view').filter(
            pk__in=[vip.pk for vip in vip_list]
        )


@register_model_view(models.F5Cluster, 'pools')
class F5ClusterPoolsView(generic.ObjectChildrenView):
    queryset = models.F5Cluster.objects.all()
    child_model = models.F5Pool
    table = tables.F5PoolTable
    template_name = 'netbox_loadbalancer_tab_view/cluster_pools.html'
    tab = ViewTab(
        label=_('Pools'),
        badge=lambda obj: obj.f5_pools.count(),
        weight=400
    )

    def get_children(self, request, parent):
        pool_list = parent.f5_pools.all()
        return models.F5Pool.objects.restrict(request.user, 'view').filter(
            pk__in=[pool.pk for pool in pool_list]
        )
        

@register_model_view(models.F5Cluster, 'nodes')
class F5ClusterNodesView(generic.ObjectChildrenView):
    queryset = models.F5Cluster.objects.all()
    child_model = models.F5PoolNode
    table = tables.F5PoolNodeTable
    template_name = 'netbox_loadbalancer_tab_view/cluster_nodes.html'
    tab = ViewTab(
        label=_('Nodes'),
        badge=lambda obj: obj.f5_nodes.count(),
        weight=500
    )

    def get_children(self, request, parent):
        node_list = parent.f5_nodes.all()
        return models.F5PoolNode.objects.restrict(request.user, 'view').filter(
            pk__in=[node.pk for node in node_list]
        )


class F5ClusterView(generic.ObjectView):
    queryset = models.F5Cluster.objects.all()
    
    # def get_extra_context(self, request, instance):
    #     physical_devices_table = DeviceTable(instance.physical_device.all())
    #     physical_devices_table.configure(request)
        
    #     virtual_devices_table = VirtualMachineTable(instance.virtual_device.all())
    #     virtual_devices_table.configure(request)
                
    #     vip_table = tables.F5VirtualServerTable(instance.f5_vips.all())
    #     vip_table.configure(request)
        
    #     pool_table = tables.F5PoolTable(instance.f5_pools.all())
    #     pool_table.configure(request)
        
    #     node_table = tables.F5PoolNodeTable(instance.f5_nodes.all())
    #     node_table.configure(request)
        
    #     return {
    #         'physical_devices_table': physical_devices_table,
    #         'virtual_devices_table': virtual_devices_table,
    #         'vip_table': vip_table,
    #         'pool_table': pool_table,
    #         'node_table': node_table,
    #     }


class F5ClusterListView(generic.ObjectListView):
    queryset = models.F5Cluster.objects.annotate(
        physical_device_count=Count('physical_device', distinct=True),
    ).annotate(
        virtual_device_count=Count('virtual_device', distinct=True)
    )

    table = tables.F5ClusterTable
    filterset = filtersets.F5ClusterFilterSet
    filterset_form = forms.F5ClusterFilterForm


class F5ClusterEditView(generic.ObjectEditView):
    queryset = models.F5Cluster.objects.all()
    form = forms.F5ClusterForm


class F5ClusterDeleteView(generic.ObjectDeleteView):
    queryset = models.F5Cluster.objects.all()


class F5ClusterBulkDeleteView(generic.BulkDeleteView):
    queryset = models.F5Cluster.objects.all()
    filterset = filtersets.F5ClusterFilterSet
    table = tables.F5ClusterTable


#
# F5VirtualServer views
#

class F5VirtualServerView(generic.ObjectView):
    queryset = models.F5VirtualServer.objects.all()
    def get_extra_context(self, request, instance):
        table = tables.F5PoolTable(instance.pools.all())
        table.configure(request)

        return {
            'pools_table': table,
        }


class F5VirtualServerListView(generic.ObjectListView):
    queryset = models.F5VirtualServer.objects.annotate(
        pool_count=Count('pools')
    )
    queryset = models.F5VirtualServer.objects.all()
    table = tables.F5VirtualServerTable
    filterset = filtersets.F5VirtualServerFilterSet
    filterset_form = forms.F5VirtualServerFilterForm


class F5VirtualServerEditView(generic.ObjectEditView):
    queryset = models.F5VirtualServer.objects.all()
    form = forms.F5VirtualServerForm


class F5VirtualServerDeleteView(generic.ObjectDeleteView):
    queryset = models.F5VirtualServer.objects.all()


class F5VirtualServerBulkDeleteView(generic.BulkDeleteView):
    queryset = models.F5VirtualServer.objects.all()
    filterset = filtersets.F5VirtualServerFilterSet
    table = tables.F5VirtualServerTable


@register_model_view(models.F5VirtualServer, 'pools')
class F5VirtualServerPoolsView(generic.ObjectChildrenView):
    queryset = models.F5VirtualServer.objects.all()
    child_model = models.F5Pool
    table = tables.F5PoolTable
    template_name = 'netbox_loadbalancer_tab_view/vip_pools.html'
    tab = ViewTab(
        label=_('Pool List'),
        badge=lambda obj: obj.pools.count(),
        weight=100
    )

    def get_children(self, request, parent):
        pool_list = parent.pools.all()
        return models.F5Pool.objects.restrict(request.user, 'view').filter(
            pk__in=[pool.pk for pool in pool_list]
        )


@register_model_view(models.F5VirtualServer, 'add_pools', path='pools/add')
class F5VirtualServerAddPoolsView(generic.ObjectEditView):
    queryset = models.F5VirtualServer.objects.all()
    form = forms.F5VirtualServerAddPoolsForm
    template_name = 'netbox_loadbalancer/f5virtualserver_update_pools.html'

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
            'return_url': reverse('plugins:netbox_loadbalancer:f5virtualserver', kwargs={'pk': pk}),
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


@register_model_view(models.F5VirtualServer, 'delete_pools', path='pools/delete')
class F5VirtualServerDeletePoolsView(generic.ObjectEditView):
    queryset = models.F5VirtualServer.objects.all()
    form = forms.F5VirtualServerDeletePoolsForm
    template_name = 'netbox_loadbalancer/f5virtualserver_delete_pools.html'

    def post(self, request, pk):

        vip = get_object_or_404(self.queryset, pk=pk)
        
        if '_confirm' in request.POST:
            form = self.form(request.POST)
            pool_pks = request.POST.getlist('pk')
            with transaction.atomic():
                for pool in models.F5Pool.objects.filter(pk__in=pool_pks):
                    vip.pools.remove(pool)
                    vip.save()

            messages.success(request, "Removed {} pools from {}".format(
                len(pool_pks), vip
            ))
            return redirect(reverse('plugins:netbox_loadbalancer:f5virtualserver_pools', kwargs={'pk': pk}))
        else:
            form = self.form(request.POST, initial={'pk': request.POST.getlist('pk')})
        pk_values = form.initial.get('pk', [])
        selected_objects = models.F5Pool.objects.filter(pk__in=pk_values)
        pool_table = tables.F5PoolTable(list(selected_objects), orderable=False)

        return render(request, self.template_name, {
            'form': form,
            'parent_obj': vip,
            'table': pool_table,
            'obj_type_plural': 'pools',
            'return_url': reverse('plugins:netbox_loadbalancer:f5virtualserver_pools', kwargs={'pk': pk})
        })
        

#
# F5Pool views
#

class F5PoolView(generic.ObjectView):
    queryset = models.F5Pool.objects.all()
    def get_extra_context(self, request, instance):
        table = tables.F5PoolNodeTable(instance.f5_pool_node.all())
        table.configure(request)

        return {
            'nodes_table': table,
        }   


class F5PoolListView(generic.ObjectListView):
    # queryset = models.F5Pool.objects.annotate(
    #     node_count=Count('f5_pool_node')
    # )
    queryset = models.F5Pool.objects.all()
    table = tables.F5PoolTable
    filterset = filtersets.F5PoolFilterSet
    filterset_form = forms.F5PoolFilterForm


class F5PoolEditView(generic.ObjectEditView):
    queryset = models.F5Pool.objects.all()
    form = forms.F5PoolForm


class F5PoolDeleteView(generic.ObjectDeleteView):
    queryset = models.F5Pool.objects.all()


class F5PoolBulkDeleteView(generic.BulkDeleteView):
    queryset = models.F5Pool.objects.all()
    filterset = filtersets.F5PoolFilterSet
    table = tables.F5PoolTable

@register_model_view(models.F5Pool, 'nodes')
class F5PoolNodesView(generic.ObjectChildrenView):
    queryset = models.F5Pool.objects.all()
    child_model = models.F5PoolNode
    table = tables.F5PoolNodeTable
    template_name = 'netbox_loadbalancer_tab_view/pool_nodes.html'
    tab = ViewTab(
        label=_('Nodes List'),
        badge=lambda obj: obj.f5_pool_node.count(),
        weight=100
    )

    def get_children(self, request, parent):
        node_list = parent.f5_pool_node.all()
        return models.F5PoolNode.objects.restrict(request.user, 'view').filter(
            pk__in=[node.pk for node in node_list]
        )


@register_model_view(models.F5Pool, 'add_nodes', path='nodes/add')
class F5PoolAddNodesView(generic.ObjectEditView):
    queryset = models.F5Pool.objects.all()
    form = forms.F5PoolAddNodesForm
    template_name = 'netbox_loadbalancer/f5pool_update_nodes.html'

    def get(self, request, pk):
        queryset = self.queryset.filter(pk=pk)
        pool = get_object_or_404(queryset)
        nodes = pool.f5_pool_node.all()
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
            'return_url': reverse('plugins:netbox_loadbalancer:f5pool', kwargs={'pk': pk}),
        })

    def post(self, request, pk):
        queryset = self.queryset.filter(pk=pk)
        pool = get_object_or_404(queryset)
        form = self.form(request.POST)

        if form.is_valid():
            current_nodes = pool.f5_pool_node.all()
            # Remove current pools 
            if current_nodes:
                for node in current_nodes:
                    pool.f5_pool_node.remove(node)
                    
            # Add pool 
            new_data_node = form.cleaned_data['nodes']
            for newnode in new_data_node:
                pool.f5_pool_node.add(newnode)
                
            messages.success(request, f"Success update nodes for {pool.name}")
            return redirect(pool.get_absolute_url())

        return render(request, self.template_name, {
            'vip': pool,
            'form': form,
            'return_url': pool.get_absolute_url(),
        })


@register_model_view(models.F5Pool, 'delete_nodes', path='nodes/delete')
class F5PoolDeleteNodesView(generic.ObjectEditView):
    queryset = models.F5Pool.objects.all()
    form = forms.F5PoolDeleteNodesForm
    template_name = 'netbox_loadbalancer/f5pool_delete_nodes.html'

    def post(self, request, pk):

        pool = get_object_or_404(self.queryset, pk=pk)
        
        if '_confirm' in request.POST:
            form = self.form(request.POST)
            node_pks = request.POST.getlist('pk')
            with transaction.atomic():
                for node in models.F5PoolNode.objects.filter(pk__in=node_pks):
                    pool.f5_pool_node.remove(node)
                    pool.save()

            messages.success(request, "Removed {} nodes from {}".format(
                len(node_pks), pool
            ))
            return redirect(reverse('plugins:netbox_loadbalancer:f5pool_nodes', kwargs={'pk': pk}))
        else:
            form = self.form(request.POST, initial={'pk': request.POST.getlist('pk')})
        pk_values = form.initial.get('pk', [])
        selected_objects = models.F5PoolNode.objects.filter(pk__in=pk_values)
        node_table = tables.F5PoolNodeTable(list(selected_objects), orderable=False)

        return render(request, self.template_name, {
            'form': form,
            'parent_obj': pool,
            'table': node_table,
            'obj_type_plural': 'nodes',
            'return_url': reverse('plugins:netbox_loadbalancer:f5pool_nodes', kwargs={'pk': pk})
        })
        


#
# F5PoolNode views
#

class F5PoolNodeView(generic.ObjectView):
    queryset = models.F5PoolNode.objects.all()


class F5PoolNodeListView(generic.ObjectListView):
    queryset = models.F5PoolNode.objects.all()
    table = tables.F5PoolNodeTable
    filterset = filtersets.F5PoolNodeFilterSet
    filterset_form = forms.F5PoolNodeFilterForm


class F5PoolNodeEditView(generic.ObjectEditView):
    queryset = models.F5PoolNode.objects.all()
    form = forms.F5PoolNodeForm
    template_name = 'netbox_loadbalancer/f5poolnode_edit.html'


class F5PoolNodeDeleteView(generic.ObjectDeleteView):
    queryset = models.F5PoolNode.objects.all()
    
    
class F5PoolNodeBulkDeleteView(generic.BulkDeleteView):
    queryset = models.F5PoolNode.objects.all()
    filterset = filtersets.F5PoolFilterSet
    table = tables.F5PoolNodeTable
