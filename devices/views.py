from django.shortcuts import render
from .models import Device
from django.template import Context
from django.http import Http404,HttpResponseRedirect
from django.utils.translation import ugettext as _

def devices_overview(request):
    devices = Device.objects.all()
    variables = Context({
        'Devices': devices
    })
    return render(request, 'devices/devices.html', variables)


def device_pingMQTT(request, devID):
    try:
        device = Device.objects.get(id=devID)
    except:
        raise Http404(_('Device not found'))

    device.sendPingViaMQTT()
    return HttpResponseRedirect("/devices/")
