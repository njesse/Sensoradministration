from django import forms
from django.forms import ModelForm
from .models import SensorType,Sensor
from connectiontypes.models import ConnectionType
from django.utils.translation import ugettext_lazy as _
from django.forms import inlineformset_factory,modelformset_factory


class SensorTypeForm(ModelForm):
    required_css_class = 'editDetails'

    def __init__(self, *args, **kwargs):
        super(SensorTypeForm, self).__init__(*args, **kwargs)
        # Making name required

        self.fields['typeName'].label = _("Typ Bezeichnung")
        self.fields['datasheet'].label = _("Datenblatt")

    class Meta:
        model = SensorType
        fields = ('typeName', 'datasheet')


class SensorForm(ModelForm):
    class Meta:
        model = Sensor
        fields = ( 'sensortype',)



# SensortypeFormSet = inlineformset_factory(model=SensorType,  fields=('typeName','datasheet','interfaces', 'measurements'))
# SensortypeFormSet = inlineformset_factory(SensorType,Sensor,  fields=('id','sensortype',))
# SensortypeFormSet = modelformset_factory(SensorType, extra=0, fields=('typeName', 'datasheet', 'interfaces', 'measurements'))
