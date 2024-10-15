from django.db import models
from netbox.models import NetBoxModel
from ipam.models.ip import IPAddress
from utilities.choices import ChoiceSet
from tenancy.models.contacts import Contact
from django.urls import reverse
from django.utils.html import format_html

class LBVirtualServerType(ChoiceSet):    
    CHOICES = [
       ('l4', 'LoadBalance Layer 4', 'indigo'),
       ('l7', 'LoadBalance Layer 7', 'green'),
    ]

class LBVirtualProtocol(ChoiceSet):    
    CHOICES = [
       ('http', 'http', 'green'),
       ('fastl4', 'fastl4', 'indigo'),
       ('tcp', 'tcp', 'blue'),
       ('udp', 'udp', 'teal'),
       ('other', 'other', 'gray'),
    ]

class LBVipStatus(ChoiceSet):
    CHOICES = [
       ('up', 'up', 'green'),
       ('down', 'down', 'red'),
       ('disable', 'disable', 'gray'),
    ]
    
class LBPoolStatus(ChoiceSet):
    CHOICES = [
       ('up', 'up', 'green'),
       ('down', 'down', 'red'),
       ('disable', 'disable', 'gray'),
    ]

class LBPoolNodeStatus(ChoiceSet):
    CHOICES = [
       ('up', 'up', 'green'),
       ('down', 'down', 'red'),
       ('disable', 'disable', 'gray'),
    ]
    
    
class LBCluster(NetBoxModel):
    name = models.CharField(
        max_length=200,
        blank=False,
        unique=True
    )
    
    physical_device = models.ManyToManyField(
        to='dcim.Device', 
        related_name='LB_cluster_physical_devices',
        blank=True,
        default=None
    )
        
    virtual_device = models.ManyToManyField(
        to='virtualization.VirtualMachine', 
        related_name='LB_cluster_virtual_devices',
        blank=True,
        default=None
    )
    
    describe = models.TextField(
        blank=True
    )
    
    comments = models.TextField(
        blank=True
    )
    
    class Meta:
        ordering = ('-pk',)
        verbose_name = ('Load Balancer Cluster')
        verbose_name_plural = ('Load Balancer Clusters')

        # unique_together = ('name', 'ip')

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('plugins:netbox_loadbalancer:LBcluster', args=[self.pk])

    # @property
    # def cluster_device(self):
    #     return self.physical_device.count + self.virtual_device.count ## Not work ??

class LBVirtualServer(NetBoxModel):
    cluster = models.ForeignKey(
        to=LBCluster,
        on_delete=models.PROTECT,
        related_name='LB_vips' 
    )
    
    name = models.CharField(
        max_length=200,
        unique=True,
        blank=False,
    )
    
    ip = models.ForeignKey(
        to=IPAddress,
        on_delete=models.PROTECT,
        related_name='LB_vips'
    )
    
    port = models.IntegerField(
        blank=False
    )
    
    vip_type = models.CharField(
        max_length=20,
        blank=True,
        choices=LBVirtualServerType
    )
    
    protocol = models.CharField(
        max_length=20,
        blank=False,
        choices=LBVirtualProtocol
    )
        
    owner = models.ForeignKey(
        to=Contact,
        on_delete=models.PROTECT,
        related_name='LB_owner'
    )
    
    status = models.CharField(
        max_length=20,
        blank=False,
        choices=LBVipStatus
    )
    
    describe = models.TextField(
        blank=True
    )
    
    comments = models.TextField(
        blank=True
    )
    
    class Meta:
        ordering = ('-pk',)
        unique_together = ('name', 'ip')
        verbose_name = ('Load Balancer Virtual Server')
        verbose_name_plural = ('Load Balancer Virtual Servers')

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('plugins:netbox_loadbalancer:LBvirtualserver', args=[self.pk])
    
    def get_vip_type_color(self):
        return LBVirtualServerType.colors.get(self.vip_type)
    
    def get_status_color(self):
        return LBVipStatus.colors.get(self.status)
    
    def get_protocol_color(self):
        return LBVirtualProtocol.colors.get(self.protocol)


class LBPool(NetBoxModel):
    cluster = models.ForeignKey(
        to=LBCluster,
        on_delete=models.PROTECT,
        related_name='LB_pools' 
    )
    
    name = models.CharField(
        max_length=200,
        blank=False,
        unique=True
    )
    
    uri = models.CharField(
        max_length=100,
        blank=False,
        help_text="Eg: '/', '/api/v1', 'heathz'..."
    )
    
    vip = models.ManyToManyField(
        to=LBVirtualServer, 
        related_name='pools',
        blank=True,
        default=None
    )
    
    # vip = models.ForeignKey(
    #     to=LBVirtualServer,
    #     blank=True, 
    #     null=True,
    #     related_name='pools',
    #     on_delete=models.SET_NULL
    # )   
    
    status = models.CharField(
        max_length=20,
        blank=False,
        choices=LBPoolStatus
    )
    
    describe = models.TextField(
        blank=True
    )
    
    comments = models.TextField(
        blank=True
    )
    
    class Meta:
        ordering = ('-pk',)
        verbose_name = ('Load Balancer Pool')
        verbose_name_plural = ('Load Balancer Pools')

    def __str__(self):
        return f'{self.name} ({self.uri})'
    
    def get_absolute_url(self):
        return reverse('plugins:netbox_loadbalancer:LBpool', args=[self.pk])
    
    def get_status_color(self):
        return LBPoolStatus.colors.get(self.status)
    
    @property
    def full_url(self):
        html_content = ''
        if self.vip.all():
            for vip in self.vip.all():
                html_content += f'<a href="/plugins/LB-manager/vips/{vip.pk}/">{vip.ip.address.ip}:{vip.port}{self.uri}</a><br/>'
        return format_html(html_content)
    
    @property
    def related_node(self):
        return self.LB_pool_node.all()
    
    @property
    def related_vip(self):
        return self.vip.all()
    

class LBPoolNode(NetBoxModel):
    cluster = models.ForeignKey(
        to=LBCluster,
        on_delete=models.PROTECT,
        related_name='LB_nodes' 
    )
    
    name = models.CharField(
        max_length=200,
        blank=False,
        unique=True
    )
                
    physical_device = models.ForeignKey(
        to='dcim.Device', 
        on_delete=models.PROTECT,
        related_name='LB_pool_node_physical_devices',
        blank=True,
        null=True
    )
    
    virtual_device = models.ForeignKey(
        to='virtualization.VirtualMachine', 
        on_delete=models.PROTECT,
        related_name='LB_pool_node_virtual_devices',
        blank=True,
        null=True
    )
    
    port = models.IntegerField(
        blank=False
    )
    
    pool = models.ForeignKey(
        to=LBPool,
        related_name='LB_pool_node',
        blank=True, 
        on_delete=models.PROTECT,
        null=True
    )
    
    status = models.CharField(
        max_length=20,
        blank=False,
        choices=LBPoolNodeStatus
    )
    
    describe = models.TextField(
        blank=True
    )
    
    comments = models.TextField(
        blank=True
    )
    
    class Meta:
        ordering = ('-pk',)
        verbose_name = ('Load Balancer Pool Node')
        verbose_name_plural = ('Load Balancer Pool Nodes')
        # unique_together = ('name', 'ip')

    def __str__(self):
        ip = ''
        if self.physical_device:
            ip = self.physical_device.primary_ip4.address.ip
        if self.virtual_device:
            ip = self.virtual_device.primary_ip4.address.ip
        
        return f'{self.name} ({ip}:{self.port})'
    
    def get_absolute_url(self):
        return reverse('plugins:netbox_loadbalancer:LBpoolnode', args=[self.pk])

    def get_status_color(self):
        return LBPoolNodeStatus.colors.get(self.status)
    
    @property
    def ip(self):
        if self.physical_device:
            return format_html(f'<a href="/ipam/ip-addresses/{self.physical_device.primary_ip4_id}/">{self.physical_device.primary_ip4}</a>')
        if self.virtual_device:
            return format_html(f'<a href="/ipam/ip-addresses/{self.virtual_device.primary_ip4_id}/">{self.virtual_device.primary_ip4}</a>')
        
    @property
    def related_device(self):
        if self.physical_device:
            return format_html(f'<a href="/dcim/devices/{self.physical_device.pk}/">{self.physical_device.name}</a>')
        if self.virtual_device:
            return format_html(f'<a href="/virtualization/virtual-machines/{self.virtual_device.pk}/">{self.virtual_device.name}</a>')