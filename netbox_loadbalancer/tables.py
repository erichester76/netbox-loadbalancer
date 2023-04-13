import django_tables2 as tables
from netbox.tables import ChoiceFieldColumn, NetBoxTable, columns
from django_tables2.utils import Accessor
from .models import F5Cluster, F5Pool, F5PoolNode, F5VirtualServer

# from dcim.models.devices import Device
#


class F5ClusterTable(NetBoxTable):
    name = tables.Column(
        linkify=True
    )
    physical_device_count = tables.Column()
    virtual_device_count = tables.Column()

    class Meta(NetBoxTable.Meta):
        model = F5Cluster
        fields =  ('pk', 'id', 'name', 'physical_device_count', 'virtual_device_count', 'describe')
        default_columns = ('name', 'physical_device_count', 'virtual_device_count', 'describe')


class F5VirtualServerTable(NetBoxTable):
    name = tables.Column(
        linkify=True
    )
    
    ip = tables.Column(
        linkify=True
    )
    
    vip_type = ChoiceFieldColumn()
    
    protocol = ChoiceFieldColumn()
    status = ChoiceFieldColumn()
    
    cluster = tables.Column(
        linkify=True
    )
    
    owner = tables.Column(
        linkify=True
    )
    
    class Meta(NetBoxTable.Meta):
        model = F5VirtualServer
        fields = ('pk', 'id', 'name', 'ip', 'port', 'protocol', 'vip_type', 'cluster', 'owner', 'status', 'describe')
        default_columns = ('name', 'ip', 'port', 'protocol', 'vip_type', 'cluster', 'owner', 'status', 'describe')
        

POOL_LINK = """
{% if record.pk %}
    {% if record.related_node %}
        <table>
            <tr>
                <td><a href="{{ record.get_absolute_url }}">{{ record.name }}</a></td>
                <td></td>
            </tr>
            <tr>
                <td></td>
                <td> 
                    <ul>
                        {% for node in record.related_node %}
                            <li><small><a href="{% url 'plugins:netbox_loadbalancer:f5poolnode' node.pk %}">{{ node }}</a></small></li>
                        {% endfor %}
                    </ul>
                </td>
            </tr>
        </table>
    {% else %}
        <a href="{{ record.get_absolute_url }}">{{ record.name }}</a>
    {% endif %}
{% endif %}
"""

VIP_RELATED_POOL = """
{% if record.pk %}
    {% if record.related_vip %}
        {% for vip in record.related_vip %} 
            <a href="{% url 'plugins:netbox_loadbalancer:f5virtualserver' vip.pk %}">{{ vip.name }} - {{ vip.ip.address.ip }}:{{ vip.port }}</a><br/>
        {% endfor %}
    {% else %}
        <span></span>
    {% endif %}
{% endif %}
"""

class F5PoolTable(NetBoxTable):
    name = columns.TemplateColumn(
        template_code=POOL_LINK,
        export_raw=True,
        attrs={'td': {'class': 'text-nowrap'}}
    )

    vip = columns.TemplateColumn(
        template_code=VIP_RELATED_POOL,
        export_raw=True,
        attrs={'td': {'class': 'text-nowrap'}}
    )
    cluster = tables.Column(
        linkify=True
    )
    status = ChoiceFieldColumn()
    
    full_url = tables.Column(
        verbose_name="Vip Full URL"
    )
    
    class Meta(NetBoxTable.Meta):
        model = F5Pool
        fields = ('pk', 'id', 'name', 'full_url', 'describe', 'vip', 'cluster', 'status')
        default_columns = ('name', 'full_url', 'vip', 'cluster', 'describe', 'status')
        
    
class F5PoolNodeTable(NetBoxTable):
    name = tables.Column(
        linkify=True
    )
    # ip = tables.Column(
    #     linkify=True
    # )
    pool = tables.Column(
        linkify=True
    )
    status = ChoiceFieldColumn()
    class Meta(NetBoxTable.Meta):
        model = F5PoolNode
        fields = ('pk', 'id', 'name', 'cluster', 'status','related_device', 'port', 'pool', 'describe', 'ip')
        default_columns = ('name', 'related_device', 'ip', 'port', 'pool', 'describe', 'cluster', 'status')
