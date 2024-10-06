from netbox.plugins import PluginConfig

class NetboxLoadBalancerConfig(PluginConfig):
    name = 'netbox_loadbalancer'
    verbose_name = 'Netbox LoadBalancer'
    description = 'Manager LoadBalancer with Netbox'
    version = '1.0.0'
    author = 'HuyTM'
    min_version = '4.0.0'
    author_email = 'huytm@hocchudong.com'
    base_url = 'netbox_loadbalancer'


config = NetboxLoadBalancerConfig
