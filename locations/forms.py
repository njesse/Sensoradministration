from django import forms
from django.forms import ModelForm,inlineformset_factory
from .models import Location, Building,Address,Room
from django.utils.translation import ugettext_lazy as _


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('description', 'number',)


class BuildingForm(ModelForm):
        class Meta:
            model = Building
            fields = ('description',)


class AddressForm(ModelForm):
    class Meta:
        model = Address
        fields = ('addressLine1', 'addressLine2', 'city', 'country', 'zip')


class LocationForm(ModelForm):
    class Meta:
        model = Location
        fields = ('description',)

RoomsFormSet = inlineformset_factory(Building, Room, extra=5, form=RoomForm)
BuildingFormSet = inlineformset_factory(Address, Building, extra=1, form=BuildingForm)
LocationFormSet = inlineformset_factory(Room, Location, extra=5, form=LocationForm)
