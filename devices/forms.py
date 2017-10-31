from django.forms import ModelForm
from .models import Device


class deviceform(ModelForm):

    class Meta:
        model = Device
        fields = ('externalID','description', 'location')
