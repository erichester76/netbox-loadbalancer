from django.urls import path

from netbox.views.generic import ObjectChangeLogView
from . import models, views

urlpatterns = [
    
    #F5Cluster
    path('clusters/', views.F5ClusterListView.as_view(), name='f5cluster_list'),
    path('clusters/add/', views.F5ClusterEditView.as_view(), name='f5cluster_add'),
    path('clusters/<int:pk>/', views.F5ClusterView.as_view(), name='f5cluster'),
    path('clusters/<int:pk>/edit/', views.F5ClusterEditView.as_view(), name='f5cluster_edit'),
    path('clusters/<int:pk>/delete/', views.F5ClusterDeleteView.as_view(), name='f5cluster_delete'),
    path('clusters/delete/', views.F5ClusterBulkDeleteView.as_view(), name='f5cluster_bulk_delete'),
    path('clusters/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='f5cluster_changelog', kwargs={
        'model': models.F5Cluster
    }),
    
    path('clusters/<int:pk>/devices/', views.F5ClusterDevicesView.as_view(), name='f5cluster_devices'),
    path('clusters/<int:pk>/virtualdevices/', views.F5ClusterVirtualDevicesView.as_view(), name='f5cluster_virtualdevices'),
    path('clusters/<int:pk>/vips/', views.F5ClusterVipsView.as_view(), name='f5cluster_vips'),
    path('clusters/<int:pk>/pools/', views.F5ClusterPoolsView.as_view(), name='f5cluster_pools'),
    path('clusters/<int:pk>/nodes/', views.F5ClusterNodesView.as_view(), name='f5cluster_nodes'),
    
    # F5VirtualServer
    path('vips/', views.F5VirtualServerListView.as_view(), name='f5virtualserver_list'),
    path('vips/add/', views.F5VirtualServerEditView.as_view(), name='f5virtualserver_add'),
    path('vips/<int:pk>/', views.F5VirtualServerView.as_view(), name='f5virtualserver'),
    path('vips/<int:pk>/edit/', views.F5VirtualServerEditView.as_view(), name='f5virtualserver_edit'),
    path('vips/<int:pk>/delete/', views.F5VirtualServerDeleteView.as_view(), name='f5virtualserver_delete'),
    path('vips/delete/', views.F5VirtualServerBulkDeleteView.as_view(), name='f5virtualserver_bulk_delete'),
    path('vips/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='f5virtualserver_changelog', kwargs={
        'model': models.F5VirtualServer
    }),
    
    path('vips/<int:pk>/pools/', views.F5VirtualServerPoolsView.as_view(), name='f5virtualserver_pools'),
    path('vips/<int:pk>/pools/add/', views.F5VirtualServerAddPoolsView.as_view(), name='f5virtualserver_add_pools'),
    path('vips/<int:pk>/pools/delete/', views.F5VirtualServerDeletePoolsView.as_view(), name='f5virtualserver_delete_pools'),

    # F5Pool
    path('pools/', views.F5PoolListView.as_view(), name='f5pool_list'),
    path('pools/add/', views.F5PoolEditView.as_view(), name='f5pool_add'),
    path('pools/<int:pk>/', views.F5PoolView.as_view(), name='f5pool'),
    path('pools/<int:pk>/edit/', views.F5PoolEditView.as_view(), name='f5pool_edit'),
    path('pools/<int:pk>/delete/', views.F5PoolDeleteView.as_view(), name='f5pool_delete'),
    path('pools/delete/', views.F5PoolBulkDeleteView.as_view(), name='f5pool_bulk_delete'),
    path('pools/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='f5pool_changelog', kwargs={
        'model': models.F5Pool
    }),
    
    path('pools/<int:pk>/nodes/', views.F5PoolNodesView.as_view(), name='f5pool_nodes'),
    path('pools/<int:pk>/nodes/add/', views.F5PoolAddNodesView.as_view(), name='f5pool_add_nodes'),
    path('pools/<int:pk>/nodes/delete/', views.F5PoolDeleteNodesView.as_view(), name='f5pool_delete_nodes'),
    
    # F5PoolNode
    path('nodes/', views.F5PoolNodeListView.as_view(), name='f5poolnode_list'),
    path('nodes/add/', views.F5PoolNodeEditView.as_view(), name='f5poolnode_add'),
    path('nodes/<int:pk>/', views.F5PoolNodeView.as_view(), name='f5poolnode'),
    path('nodes/<int:pk>/edit/', views.F5PoolNodeEditView.as_view(), name='f5poolnode_edit'),
    path('nodes/<int:pk>/delete/', views.F5PoolNodeDeleteView.as_view(), name='f5poolnode_delete'),
    path('nodes/delete/', views.F5PoolNodeBulkDeleteView.as_view(), name='f5poolnode_bulk_delete'),
    path('nodes/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='f5poolnode_changelog', kwargs={
        'model': models.F5PoolNode
    }),

]