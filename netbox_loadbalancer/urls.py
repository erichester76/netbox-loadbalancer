from django.urls import path

from netbox.views.generic import ObjectChangeLogView
from . import models, views

urlpatterns = [
    
    #LBCluster
    path('clusters/', views.LBClusterListView.as_view(), name='LBcluster_list'),
    path('clusters/add/', views.LBClusterEditView.as_view(), name='LBcluster_add'),
    path('clusters/<int:pk>/', views.LBClusterView.as_view(), name='LBcluster'),
    path('clusters/<int:pk>/edit/', views.LBClusterEditView.as_view(), name='LBcluster_edit'),
    path('clusters/<int:pk>/delete/', views.LBClusterDeleteView.as_view(), name='LBcluster_delete'),
    path('clusters/delete/', views.LBClusterBulkDeleteView.as_view(), name='LBcluster_bulk_delete'),
    path('clusters/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='LBcluster_changelog', kwargs={
        'model': models.LBCluster
    }),
    
    path('clusters/<int:pk>/devices/', views.LBClusterDevicesView.as_view(), name='LBcluster_devices'),
    path('clusters/<int:pk>/virtualdevices/', views.LBClusterVirtualDevicesView.as_view(), name='LBcluster_virtualdevices'),
    path('clusters/<int:pk>/vips/', views.LBClusterVipsView.as_view(), name='LBcluster_vips'),
    path('clusters/<int:pk>/pools/', views.LBClusterPoolsView.as_view(), name='LBcluster_pools'),
    path('clusters/<int:pk>/nodes/', views.LBClusterNodesView.as_view(), name='LBcluster_nodes'),
    
    # LBVirtualServer
    path('vips/', views.LBVirtualServerListView.as_view(), name='LBvirtualserver_list'),
    path('vips/add/', views.LBVirtualServerEditView.as_view(), name='LBvirtualserver_add'),
    path('vips/<int:pk>/', views.LBVirtualServerView.as_view(), name='LBvirtualserver'),
    path('vips/<int:pk>/edit/', views.LBVirtualServerEditView.as_view(), name='LBvirtualserver_edit'),
    path('vips/<int:pk>/delete/', views.LBVirtualServerDeleteView.as_view(), name='LBvirtualserver_delete'),
    path('vips/delete/', views.LBVirtualServerBulkDeleteView.as_view(), name='LBvirtualserver_bulk_delete'),
    path('vips/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='LBvirtualserver_changelog', kwargs={
        'model': models.LBVirtualServer
    }),
    
    path('vips/<int:pk>/pools/', views.LBVirtualServerPoolsView.as_view(), name='LBvirtualserver_pools'),
    path('vips/<int:pk>/pools/add/', views.LBVirtualServerAddPoolsView.as_view(), name='LBvirtualserver_add_pools'),
    path('vips/<int:pk>/pools/delete/', views.LBVirtualServerDeletePoolsView.as_view(), name='LBvirtualserver_delete_pools'),

    # LBPool
    path('pools/', views.LBPoolListView.as_view(), name='LBpool_list'),
    path('pools/add/', views.LBPoolEditView.as_view(), name='LBpool_add'),
    path('pools/<int:pk>/', views.LBPoolView.as_view(), name='LBpool'),
    path('pools/<int:pk>/edit/', views.LBPoolEditView.as_view(), name='LBpool_edit'),
    path('pools/<int:pk>/delete/', views.LBPoolDeleteView.as_view(), name='LBpool_delete'),
    path('pools/delete/', views.LBPoolBulkDeleteView.as_view(), name='LBpool_bulk_delete'),
    path('pools/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='LBpool_changelog', kwargs={
        'model': models.LBPool
    }),
    
    path('pools/<int:pk>/nodes/', views.LBPoolNodesView.as_view(), name='LBpool_nodes'),
    path('pools/<int:pk>/nodes/add/', views.LBPoolAddNodesView.as_view(), name='LBpool_add_nodes'),
    path('pools/<int:pk>/nodes/delete/', views.LBPoolDeleteNodesView.as_view(), name='LBpool_delete_nodes'),
    
    # LBPoolNode
    path('nodes/', views.LBPoolNodeListView.as_view(), name='LBpoolnode_list'),
    path('nodes/add/', views.LBPoolNodeEditView.as_view(), name='LBpoolnode_add'),
    path('nodes/<int:pk>/', views.LBPoolNodeView.as_view(), name='LBpoolnode'),
    path('nodes/<int:pk>/edit/', views.LBPoolNodeEditView.as_view(), name='LBpoolnode_edit'),
    path('nodes/<int:pk>/delete/', views.LBPoolNodeDeleteView.as_view(), name='LBpoolnode_delete'),
    path('nodes/delete/', views.LBPoolNodeBulkDeleteView.as_view(), name='LBpoolnode_bulk_delete'),
    path('nodes/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='LBpoolnode_changelog', kwargs={
        'model': models.LBPoolNode
    }),

]