from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import newSensorChooseTypeForm
from devices.models import Device
from devices.forms import deviceform
from sensors.models import Sensor
from sensors.forms import SensorForm
from locations.models import Location
from django.template import Context
from django.template.loader import get_template
from django.contrib.auth import logout
from django.shortcuts import render
from locations.models import Location
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.utils.encoding import force_text
import re
import paho.mqtt.publish as publish
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
from django.utils.translation import ugettext as _


def location(request, locationid):

    try:
        loc = Location.objects.get(id=locationid)
    except:
        raise Http404(_('Sensor not found'))

    variables = Context({
            'location': loc
         })

    return render(request, 'locations/location.html', variables)


def device(request, deviceID):
    try:
        main_instance = Sensor.objects.get(id=deviceID)
        return sensor(request, main_instance.id)
    except:
        raise Http404(_('Device not found'))


def main_page(request):
    return render(request, 'main_page.html')


def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')


def sensor(request, sensorID):
    refererName = "refererEditSensor"

    try:
        main_instance = Sensor.objects.get(id=sensorID)

    except:
        raise Http404(_('Sensor not found'))

    if request.method == 'POST':
        if 'cancel' in request.POST:
            return redirect(request.session[refererName])

        subformset = SensorForm(request.POST, instance=main_instance)
        subformsetDevice = deviceform(request.POST, instance=main_instance.device)
        if subformset.is_valid() and subformsetDevice.is_valid():
            subformset.save()
            subformsetDevice.save()

            try:
                deviceID= subformsetDevice.cleaned_data.get('externalID')
                publish.single("device/"+deviceID, "sensor", hostname="localhost")

            except ConnectionRefusedError:
                print(_("MQTT nicht erreichbar"))

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
            # print('keine Weiterleitung')
            request.session[refererName] = ""

        else:
            referer = re.sub('^https?:\/\/', '', referer).split('/')
            referer = u'/' + u'/'.join(referer[1:])
            print(referer)
            if "/devices/sensors/sensortype/" not in referer:
                request.session[refererName] = referer

    subformset = SensorForm(instance=main_instance)
    subformsetDevice = deviceform(instance=main_instance.device)
    variables = Context({
        'sensor': main_instance,
        'sensorProperties': subformset,
        'deviceProperties':subformsetDevice,
        'requestref': request.session[refererName],
    })

    return render(request, 'sensors/sensor_details.html', variables)


def sensor_add(request):
    if request.method == 'POST':
        form = newSensorChooseTypeForm(request.POST)
        if form.is_valid():
            # Device
            device = Device()
            device.description = form.cleaned_data['description']
            device.location_id = form.data['location']
            device.save()
            sensor = Sensor()
            sensor.device = device
            sensor.sensortype_id = form.data['sensortype']
            sensor.save()
            return HttpResponseRedirect('/devices/sensors/')
    else:
        form = newSensorChooseTypeForm()
        variables = Context({
            'form': form,
        })
    return render(request, 'sensors/sensor_new.html', variables)