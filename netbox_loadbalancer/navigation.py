from netbox.plugins import PluginMenuButton, PluginMenuItem
from netbox.plugins import PluginMenu, PluginMenuButton, PluginMenuItem

cluster_items = (
     PluginMenuItem(
        link="plugins:netbox_loadbalancer:LBcluster_list",
        link_text="Cluster",
        buttons=(
            PluginMenuButton(
                link="plugins:netbox_loadbalancer:LBcluster_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                color='green',
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:netbox_loadbalancer:LBvirtualserver_list",
        link_text="Virtual Servers",
        buttons=(
            PluginMenuButton(
                link="plugins:netbox_loadbalancer:LBvirtualserver_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
            ),
        ),
    ),
    PluginMenuItem(
        link='plugins:netbox_loadbalancer:LBpool_list',
        link_text='Pools',
        buttons=(
            PluginMenuButton(
                link="plugins:netbox_loadbalancer:LBpool_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
            ),
        ),
    ),   
    PluginMenuItem(
        link='plugins:netbox_loadbalancer:LBpoolnode_list',
        link_text='Nodes',
        buttons=(
            PluginMenuButton(
                link="plugins:netbox_loadbalancer:LBpoolnode_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
            ),
        ),
    ),

)

menu = PluginMenu(
    label="Load Balancing",
    groups=(("Load Balancing", cluster_items),),
    icon_class="mdi mdi-lan",
)
