from django.forms import ModelForm
from .models import Connection,ConnectionPartner,ParameterBoolean,ParameterInt,ParameterIP,ParameterText100
from django import forms

class ConnectionForm(ModelForm):

    class Meta:
        model = Connection
        fields = ('description','type',)


class ParameterIntForm(ModelForm):
    value = forms.IntegerField()

    def __init__(self,*args, **kwargs):
        super(ParameterIntForm, self).__init__(*args, **kwargs)
        print(self.fields['connection'])

    class Meta:
        model = ParameterInt
        fields = ('name','id',)
