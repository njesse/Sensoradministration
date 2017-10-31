from django.forms import ModelForm
from .models import ConnectionType, Topology

from django.utils.translation import ugettext_lazy as _

class ConnectionTypeForm(ModelForm):
    required_css_class = 'editDetails'

    def __init__(self, *args, **kwargs):
        super(ConnectionTypeForm, self).__init__(*args, **kwargs)
        # Making name required

    class Meta:
        model = ConnectionType
        fields = ('connectionName', 'topology')


class TopologyForm(ModelForm):

    class Meta:
        model = Topology
        fields = ('topologyName',)
