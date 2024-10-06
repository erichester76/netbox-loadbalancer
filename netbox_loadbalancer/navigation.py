from netbox.plugins import PluginMenuButton, PluginMenuItem
from netbox.plugins import PluginMenu, PluginMenuButton, PluginMenuItem

cluster_items = (
     PluginMenuItem(
        link="plugins:netbox_loadbalancer:f5cluster_list",
        link_text="Cluster",
        buttons=(
            PluginMenuButton(
                link="plugins:netbox_loadbalancer:f5cluster_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                color='green',
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:netbox_loadbalancer:f5virtualserver_list",
        link_text="Virtual Servers",
        buttons=(
            PluginMenuButton(
                link="plugins:netbox_loadbalancer:f5virtualserver_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
            ),
        ),
    ),
    PluginMenuItem(
        link='plugins:netbox_loadbalancer:f5pool_list',
        link_text='Pools',
        buttons=(
            PluginMenuButton(
                link="plugins:netbox_loadbalancer:f5pool_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
            ),
        ),
    ),   
    PluginMenuItem(
        link='plugins:netbox_loadbalancer:f5poolnode_list',
        link_text='Nodes',
        buttons=(
            PluginMenuButton(
                link="plugins:netbox_loadbalancer:f5poolnode_add",
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
