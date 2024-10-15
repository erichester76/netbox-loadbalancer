from django import forms
from ipam.models.ip import IPAddress
from dcim.models.devices import Device
from virtualization.models.virtualmachines import VirtualMachine
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from utilities.forms.fields import CommentField, DynamicModelChoiceField, DynamicModelMultipleChoiceField
from .models import LBCluster, LBVirtualServer, LBPool, LBPoolNode
from utilities.forms import ConfirmationForm

class LBClusterForm(NetBoxModelForm):
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
        model = LBVirtualServer
        fields = ('name', 'physical_device', 'virtual_device', 'tags', 'describe', 'comments')


class LBVirtualServerForm(NetBoxModelForm):
    ip = DynamicModelChoiceField(
        queryset=IPAddress.objects.all()
    )
    
    cluster = DynamicModelChoiceField(
        queryset=LBCluster.objects.all()
    )
    
    describe = forms.CharField(
        required=False
    )
    
    comments = CommentField()
    
    class Meta:
        model = LBVirtualServer
        fields = ('cluster', 'name', 'ip', 'port', 'protocol', 'status','owner', 'vip_type', 'tags', 'describe', 'comments')

class LBVirtualServerAddPoolsForm(forms.Form):
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
        queryset=LBPool.objects.all(),
        help_text="Select pools here"
    )
    
    class Meta:
        fields = [
            'virtual_server', 'pools'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class LBVirtualServerDeletePoolsForm(ConfirmationForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=LBPool.objects.all(),
        widget=forms.MultipleHiddenInput()
    )


class LBPoolForm(NetBoxModelForm):
    cluster = DynamicModelChoiceField(
        queryset=LBCluster.objects.all()
    )
    
    vip = DynamicModelMultipleChoiceField(
        queryset=LBVirtualServer.objects.all(),
        required=False
    )
    
    describe = forms.CharField(
        required=False
    )
    
    comments = CommentField()
    
    class Meta:
        model = LBPool
        fields = ('cluster', 'name', 'vip', 'uri', 'status', 'tags', 'describe', 'comments')


class LBPoolAddNodesForm(forms.Form):
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
        queryset=LBPoolNode.objects.all(),
        help_text="Select nodes here"
    )
    
    class Meta:
        fields = [
            'nodes'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class LBPoolDeleteNodesForm(ConfirmationForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=LBPoolNode.objects.all(),
        widget=forms.MultipleHiddenInput()
    )


class LBPoolNodeForm(NetBoxModelForm):
    cluster = DynamicModelChoiceField(
        queryset=LBCluster.objects.all()
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
        queryset=LBPool.objects.all(),
        required=False
    )
    
    comments = CommentField()
    
    class Meta:
        model = LBPoolNode
        fields = ('cluster', 'name', 'physical_device', 'virtual_device', 'port', 'pool', 'status', 'tags', 'describe', 'comments')

## Filter
class LBClusterFilterForm(NetBoxModelFilterSetForm):
    model = LBCluster
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

class LBVirtualServerFilterForm(NetBoxModelFilterSetForm):
    model = LBVirtualServer
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

class LBPoolFilterForm(NetBoxModelFilterSetForm):
    model = LBPool
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
    
class LBPoolNodeFilterForm(NetBoxModelFilterSetForm):
    model = LBPoolNode
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
