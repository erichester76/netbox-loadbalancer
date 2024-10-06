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
)

vips_pool_items = (
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
    label="F5 Manager",
    groups=(("Cluster", cluster_items), ("LoadBalance", vips_pool_items),),
    icon_class="mdi mdi-lan",
)

# menu_items = (
#     PluginMenuItem(
#         link='plugins:huytm:huytm_list',
#         link_text='Storage Lists'
#     ),
#     PluginMenuItem(
#         link='plugins:huytm:huytm_add',
#         link_text='Storage Add'
#     ),
# )

# PluginMenuItem(
#         link="plugins:huytm:huytm_list",
#         link_text="Storage Lists",
#         buttons=(
#             PluginMenuButton(
#                 link="plugins:huytm:huytm_add",
#                 title="Add",
#                 icon_class="mdi mdi-plus-thick",
#                 color='green',
#             ),
#         ),
# )
