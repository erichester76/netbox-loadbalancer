from django.db import models
from netbox.models import NetBoxModel
from ipam.models.ip import IPAddress
from utilities.choices import ChoiceSet
from tenancy.models.contacts import Contact
from django.urls import reverse
from django.utils.html import format_html

class F5VirtualServerType(ChoiceSet):    
    CHOICES = [
       ('l4', 'LoadBalance Layer 4', 'indigo'),
       ('l7', 'LoadBalance Layer 7', 'green'),
    ]

class F5VirtualProtocol(ChoiceSet):    
    CHOICES = [
       ('http', 'http', 'green'),
       ('fastl4', 'fastl4', 'indigo'),
       ('tcp', 'tcp', 'blue'),
       ('udp', 'udp', 'teal'),
       ('other', 'other', 'gray'),
    ]

class F5VipStatus(ChoiceSet):
    CHOICES = [
       ('up', 'up', 'green'),
       ('down', 'down', 'red'),
       ('disable', 'disable', 'gray'),
    ]
    
class F5PoolStatus(ChoiceSet):
    CHOICES = [
       ('up', 'up', 'green'),
       ('down', 'down', 'red'),
       ('disable', 'disable', 'gray'),
    ]

class F5PoolNodeStatus(ChoiceSet):
    CHOICES = [
       ('up', 'up', 'green'),
       ('down', 'down', 'red'),
       ('disable', 'disable', 'gray'),
    ]
    
    
class F5Cluster(NetBoxModel):
    name = models.CharField(
        max_length=200,
        blank=False,
        unique=True
    )
    
    physical_device = models.ManyToManyField(
        to='dcim.Device', 
        related_name='f5_cluster_physical_devices',
        blank=True,
        default=None
    )
        
    virtual_device = models.ManyToManyField(
        to='virtualization.VirtualMachine', 
        related_name='f5_cluster_virtual_devices',
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
        # unique_together = ('name', 'ip')

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('plugins:netbox_loadbalancer:f5cluster', args=[self.pk])

    # @property
    # def cluster_device(self):
    #     return self.physical_device.count + self.virtual_device.count ## Not work ??

class F5VirtualServer(NetBoxModel):
    cluster = models.ForeignKey(
        to=F5Cluster,
        on_delete=models.PROTECT,
        related_name='f5_vips' 
    )
    
    name = models.CharField(
        max_length=200,
        unique=True,
        blank=False,
    )
    
    ip = models.ForeignKey(
        to=IPAddress,
        on_delete=models.PROTECT,
        related_name='f5_vips'
    )
    
    port = models.IntegerField(
        blank=False
    )
    
    vip_type = models.CharField(
        max_length=20,
        blank=True,
        choices=F5VirtualServerType
    )
    
    protocol = models.CharField(
        max_length=20,
        blank=False,
        choices=F5VirtualProtocol
    )
        
    owner = models.ForeignKey(
        to=Contact,
        on_delete=models.PROTECT,
        related_name='f5_owner'
    )
    
    status = models.CharField(
        max_length=20,
        blank=False,
        choices=F5VipStatus
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

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('plugins:netbox_loadbalancer:f5virtualserver', args=[self.pk])
    
    def get_vip_type_color(self):
        return F5VirtualServerType.colors.get(self.vip_type)
    
    def get_status_color(self):
        return F5VipStatus.colors.get(self.status)
    
    def get_protocol_color(self):
        return F5VirtualProtocol.colors.get(self.protocol)


class F5Pool(NetBoxModel):
    cluster = models.ForeignKey(
        to=F5Cluster,
        on_delete=models.PROTECT,
        related_name='f5_pools' 
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
        to=F5VirtualServer, 
        related_name='pools',
        blank=True,
        default=None
    )
    
    # vip = models.ForeignKey(
    #     to=F5VirtualServer,
    #     blank=True, 
    #     null=True,
    #     related_name='pools',
    #     on_delete=models.SET_NULL
    # )   
    
    status = models.CharField(
        max_length=20,
        blank=False,
        choices=F5PoolStatus
    )
    
    describe = models.TextField(
        blank=True
    )
    
    comments = models.TextField(
        blank=True
    )
    
    class Meta:
        ordering = ('-pk',)

    def __str__(self):
        return f'{self.name} ({self.uri})'
    
    def get_absolute_url(self):
        return reverse('plugins:netbox_loadbalancer:f5pool', args=[self.pk])
    
    def get_status_color(self):
        return F5PoolStatus.colors.get(self.status)
    
    @property
    def full_url(self):
        html_content = ''
        if self.vip.all():
            for vip in self.vip.all():
                html_content += f'<a href="/plugins/f5-manager/vips/{vip.pk}/">{vip.ip.address.ip}:{vip.port}{self.uri}</a><br/>'
        return format_html(html_content)
    
    @property
    def related_node(self):
        return self.f5_pool_node.all()
    
    @property
    def related_vip(self):
        return self.vip.all()
    

class F5PoolNode(NetBoxModel):
    cluster = models.ForeignKey(
        to=F5Cluster,
        on_delete=models.PROTECT,
        related_name='f5_nodes' 
    )
    
    name = models.CharField(
        max_length=200,
        blank=False,
        unique=True
    )
                
    physical_device = models.ForeignKey(
        to='dcim.Device', 
        on_delete=models.PROTECT,
        related_name='f5_pool_node_physical_devices',
        blank=True,
        null=True
    )
    
    virtual_device = models.ForeignKey(
        to='virtualization.VirtualMachine', 
        on_delete=models.PROTECT,
        related_name='f5_pool_node_virtual_devices',
        blank=True,
        null=True
    )
    
    port = models.IntegerField(
        blank=False
    )
    
    pool = models.ForeignKey(
        to=F5Pool,
        related_name='f5_pool_node',
        blank=True, 
        on_delete=models.PROTECT,
        null=True
    )
    
    status = models.CharField(
        max_length=20,
        blank=False,
        choices=F5PoolNodeStatus
    )
    
    describe = models.TextField(
        blank=True
    )
    
    comments = models.TextField(
        blank=True
    )
    
    class Meta:
        ordering = ('-pk',)
        # unique_together = ('name', 'ip')

    def __str__(self):
        ip = ''
        if self.physical_device:
            ip = self.physical_device.primary_ip4.address.ip
        if self.virtual_device:
            ip = self.virtual_device.primary_ip4.address.ip
        
        return f'{self.name} ({ip}:{self.port})'
    
    def get_absolute_url(self):
        return reverse('plugins:netbox_loadbalancer:f5poolnode', args=[self.pk])

    def get_status_color(self):
        return F5PoolNodeStatus.colors.get(self.status)
    
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