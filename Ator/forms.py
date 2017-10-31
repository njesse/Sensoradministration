from django import forms
from django.forms import ModelForm
from sensors.models import SensorType,Sensor
from locations.models import Location

from connectiontypes.models import ConnectionType
from django.utils.translation import ugettext_lazy as _
from django.forms import inlineformset_factory,modelformset_factory


class newSensorChooseTypeForm(ModelForm):
    description = forms.CharField(max_length=100)
    sensortypeF = forms.modelform_factory(SensorType,  fields=('typeName', 'datasheet', 'interfaces', 'measurements'))
    location = forms.ModelChoiceField(Location.objects.all(),)

    def __init__(self, *args, **kwargs):
        super(newSensorChooseTypeForm, self).__init__(*args, **kwargs)


    class Meta:
        model = Sensor
        fields = ('sensortype',)

