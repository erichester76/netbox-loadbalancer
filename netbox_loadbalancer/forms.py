from django import forms
from ipam.models.ip import IPAddress
from dcim.models.devices import Device
from virtualization.models.virtualmachines import VirtualMachine
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from utilities.forms.fields import CommentField, DynamicModelChoiceField, DynamicModelMultipleChoiceField
from .models import F5Cluster, F5VirtualServer, F5Pool, F5PoolNode
from utilities.forms import ConfirmationForm, BootstrapMixin

class F5ClusterForm(NetBoxModelForm):
    physical_device = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required=False
    )
    
    virtual_device = DynamicModelMultipleChoiceField(
        queryset=VirtualMachine.objects.all(),
        required=False
    )
    
    describe = forms.CharField(
        required=False
    )
    
    comments = CommentField()
    
    class Meta:
        model = F5VirtualServer
        fields = ('name', 'physical_device', 'virtual_device', 'tags', 'describe', 'comments')


class F5VirtualServerForm(NetBoxModelForm):
    ip = DynamicModelChoiceField(
        queryset=IPAddress.objects.all()
    )
    
    cluster = DynamicModelChoiceField(
        queryset=F5Cluster.objects.all()
    )
    
    describe = forms.CharField(
        required=False
    )
    
    comments = CommentField()
    
    class Meta:
        model = F5VirtualServer
        fields = ('cluster', 'name', 'ip', 'port', 'protocol', 'status','owner', 'vip_type', 'tags', 'describe', 'comments')

class F5VirtualServerAddPoolsForm(forms.Form):
    cluster = forms.CharField(
        disabled=True,
        required=False
    )
    
    virtual_server = forms.CharField(
        disabled=True,
        required=False
    )
    
    ip = forms.CharField(
        disabled=True,
        required=False
    )
    
    port = forms.CharField(
        disabled=True,
        required=False
    )
    
    protocol = forms.CharField(
        disabled=True,
        required=False
    )
    
    vip_type = forms.CharField(
        disabled=True,
        required=False
    )
    
    pools = DynamicModelMultipleChoiceField(
        queryset=F5Pool.objects.all(),
        help_text="Select pools here"
    )
    
    class Meta:
        fields = [
            'virtual_server', 'pools'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class F5VirtualServerDeletePoolsForm(ConfirmationForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=F5Pool.objects.all(),
        widget=forms.MultipleHiddenInput()
    )


class F5PoolForm(NetBoxModelForm):
    cluster = DynamicModelChoiceField(
        queryset=F5Cluster.objects.all()
    )
    
    vip = DynamicModelMultipleChoiceField(
        queryset=F5VirtualServer.objects.all(),
        required=False
    )
    
    describe = forms.CharField(
        required=False
    )
    
    comments = CommentField()
    
    class Meta:
        model = F5Pool
        fields = ('cluster', 'name', 'vip', 'uri', 'status', 'tags', 'describe', 'comments')


class F5PoolAddNodesForm(forms.Form):
    cluster = forms.CharField(
        disabled=True,
        required=False
    )
    
    name = forms.CharField(
        disabled=True,
        required=False
    )
    
    uri = forms.CharField(
        disabled=True,
        required=False
    )
    
    nodes = DynamicModelMultipleChoiceField(
        queryset=F5PoolNode.objects.all(),
        help_text="Select nodes here"
    )
    
    class Meta:
        fields = [
            'nodes'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class F5PoolDeleteNodesForm(ConfirmationForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=F5PoolNode.objects.all(),
        widget=forms.MultipleHiddenInput()
    )


class F5PoolNodeForm(NetBoxModelForm):
    cluster = DynamicModelChoiceField(
        queryset=F5Cluster.objects.all()
    )
    
    physical_device = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        required=False
    )
    
    virtual_device = DynamicModelChoiceField(
        queryset=VirtualMachine.objects.all(),
        required=False
    )
  
    describe = forms.CharField(
        required=False
    )
    
    pool = DynamicModelChoiceField(
        queryset=F5Pool.objects.all(),
        required=False
    )
    
    comments = CommentField()
    
    class Meta:
        model = F5PoolNode
        fields = ('cluster', 'name', 'physical_device', 'virtual_device', 'port', 'pool', 'status', 'tags', 'describe', 'comments')

## Filter
class F5ClusterFilterForm(NetBoxModelFilterSetForm):
    model = F5Cluster
    name = forms.CharField(
        required=False
    )
    physical_device = forms.CharField(
        required=False
    )
    virtual_device = forms.CharField(
        required=False
    )
    describe = forms.CharField(
        required=False
    )

class F5VirtualServerFilterForm(NetBoxModelFilterSetForm):
    model = F5VirtualServer
    name = forms.CharField(
        required=False
    )
    ip = forms.CharField(
        required=False
    )
    port = forms.CharField(
        required=False
    )
    vip_type = forms.CharField(
        required=False
    )
    protocol = forms.CharField(
        required=False
    )
    status = forms.CharField(
        required=False
    )
    
    owner = forms.CharField(
        required=False
    )
    describe = forms.CharField(
        required=False
    )

class F5PoolFilterForm(NetBoxModelFilterSetForm):
    model = F5Pool
    name = forms.CharField(
        required=False
    )
    uri = forms.CharField(
        required=False
    )
    describe = forms.CharField(
        required=False
    )
    vip = forms.CharField(
        required=False
    )
    
class F5PoolNodeFilterForm(NetBoxModelFilterSetForm):
    model = F5PoolNode
    name = forms.CharField(
        required=False
    )
    physical_device = forms.CharField(
        required=False
    )
    virtual_device = forms.CharField(
        required=False
    )
    port = forms.CharField(
        required=False
    )
    pool = forms.CharField(
        required=False
    )
    describe = forms.CharField(
        required=False
    )
