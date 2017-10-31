from django.shortcuts import render,redirect
from .models import Location, Room, Building, Address

from django.forms import formset_factory, inlineformset_factory, modelformset_factory
from django.template import Context
from django.http import Http404
from django import forms
from .forms import RoomsFormSet,BuildingForm,RoomForm,LocationFormSet,AddressForm, BuildingFormSet
from django.utils.encoding import force_text
import re
# Create your views here.
from django.utils.translation import ugettext as _

def locations_overview(request):
    locations = Location.objects.all()

    variables = Context({
        'Locations': locations,
    })
    return render(request, 'locations/locations.html', variables)


def location_Addresses(request):
    refererName='addAddress'

    if request.method == 'POST':
        form=AddressForm(request.POST)

        if form.is_valid():
            form.save()


    else:
        form = AddressForm()

        referer = force_text(
            request.META.get('HTTP_REFERER'),
            strings_only=True,
            errors='replace'
        )
        if referer is None:
            print('keine Weiterleitung')
            request.session[refererName] = ""
        else:
            referer = re.sub('^https?:\/\/', '', referer).split('/')
            referer = u'/' + u'/'.join(referer[1:])
            print(referer)
            request.session[refererName] = referer



    addresses= Address.objects.all()


    variables = Context({
        'addresses_all': addresses,
        'form': form,
    })


    return render(request, 'locations/building_new.html', variables)

def location_EditBuilding(request, buildingID):
    refererName='refererAddBuilding'
    try:
        main_instance = Building.objects.get(id=buildingID)
    except:
        raise Http404(_('Building not found'))

    if request.method == 'POST':

        if 'cancel' in request.POST:
            return redirect(request.session[refererName])

        subformset = RoomsFormSet(request.POST, instance=main_instance)

        if subformset.is_valid():
            subformset.save()
            if request.session[refererName] != "" and 'saveChangesBack' in request.POST:
                return redirect(request.session[refererName])


    else:

        referer = force_text(
            request.META.get('HTTP_REFERER'),
            strings_only=True,
            errors='replace'
        )
        if referer is None:
            print('keine Weiterleitung')
            request.session[refererName] = ""
        else:
            referer = re.sub('^https?:\/\/', '', referer).split('/')
            referer = u'/' + u'/'.join(referer[1:])
            print(referer)
            request.session[refererName] = referer

    subformset = RoomsFormSet(instance=main_instance)
    variables = Context({
        'building': main_instance,
        'rooms': subformset,
        'requestref': request.session[refererName],
    })
    return render(request, 'locations/building.html', variables)

def location_add(request):
    refererName = 'refererAddLocation'

    referer = force_text(
        request.META.get('HTTP_REFERER'),
        strings_only=True,
        errors='replace'
    )
    if referer is None:
        print('keine Weiterleitung')
        request.session[refererName] = ""
    else:
        referer = re.sub('^https?:\/\/', '', referer).split('/')
        referer = u'/' + u'/'.join(referer[1:])
        print(referer)
        if "/locations/room/" not in referer:
            if "/locations/building/" not in referer:
                if "/devices/sensors/add/" in referer:
                    request.session[refererName] = referer
                else:
                    request.session[refererName] = ""


    buildings_all = Building.objects.all()
    print(buildings_all.count())
    variables = Context({
        'buildings_all': buildings_all,
        'requestref': request.session[refererName],
    })
    return render(request, 'locations/location_new.html', variables)

def location_management(request):
    address_all = Address.objects.all()
    buildings_all= Building.objects.all()
    rooms_all= Room.objects.all()
    locations_all= Location.objects.all()

    variables = Context({
        'address_all': address_all,
        'buildings_all': buildings_all,
        'rooms_all': rooms_all,
        'locations_all': locations_all
    })

    return render(request, 'locations/locations_management.html', variables)

def location_EditRoom(request, roomID):
    refererName = "refererAddRoom"

    try:
        main_instance = Room.objects.get(id=roomID)
    except:
        raise Http404(_('Room not found'))

    if request.method == 'POST':

        if 'cancel' in request.POST:
            return redirect(request.session[refererName])

        subformset = LocationFormSet(request.POST, instance=main_instance)

        if subformset.is_valid():
            subformset.save()
            if request.session[refererName] != "" and 'saveChangesBack' in request.POST:
                return redirect(request.session[refererName])
        else:
            print(subformset.errors)

    else:


        referer = force_text(
            request.META.get('HTTP_REFERER'),
            strings_only=True,
            errors='replace'
        )
        if referer is None:
            print('keine Weiterleitung')
            request.session[refererName] = ""
        else:
            referer = re.sub('^https?:\/\/', '', referer).split('/')
            referer = u'/' + u'/'.join(referer[1:])
            print(referer)
            request.session[refererName] = referer

    subformset = LocationFormSet(instance=main_instance)
    variables = Context({
        'room': main_instance,
        'locations': subformset,
        'requestref': request.session[refererName],
    })
    return render(request, 'locations/room.html', variables)

def location_EditAddress(request,addressID):
    refererName = "refererEditAddress"

    try:
        main_instance = Address.objects.get(id=addressID)
    except:
        raise Http404(_('Room not found'))

    if request.method == 'POST':

        if 'cancel' in request.POST:
            return redirect(request.session[refererName])

        subformset = BuildingFormSet(request.POST, instance=main_instance)

        if subformset.is_valid():
            subformset.save()
            if request.session[refererName] != "" and 'saveChangesBack' in request.POST:
                return redirect(request.session[refererName])
        else:
            print(subformset.errors)

    else:
        referer = force_text(
            request.META.get('HTTP_REFERER'),
            strings_only=True,
            errors='replace'
        )
        if referer is None:
            print('keine Weiterleitung')
            request.session[refererName] = ""
        else:
            referer = re.sub('^https?:\/\/', '', referer).split('/')
            referer = u'/' + u'/'.join(referer[1:])
            print(referer)
            request.session[refererName] = referer

    subformset = BuildingFormSet(instance=main_instance)
    variables = Context({
        'address': main_instance,
        'buildings': subformset,
        'requestref': request.session[refererName],
    })
    return render(request, 'locations/address.html', variables)
