from django.utils.translation import ugettext as _
from django.shortcuts import render,redirect
from django.template import Context
from .models import Connection,ConnectionPartner,ParameterInt,ParameterIP,ParameterBoolean,ParameterText100
from connectiontypes.models import ConnectionType
from .forms import ConnectionForm,ParameterIntForm
from django.http import HttpResponse,Http404
from django import forms
from django.utils.encoding import force_text
from django.forms import modelformset_factory,formset_factory
import re
# Create your views here.
import paho.mqtt.publish as publish

def connections_overview(request):
    connections = Connection.objects.all()
    variables = Context({
        'Connections': connections
    })
    return render(request, 'connections/connections.html', variables)


def connection_add(request):
    refererName = 'refererAddConnection'
    if request.method == 'POST':
      form = ConnectionForm(request.POST)

      if form.is_valid():
          newType = form.save()
          return redirect('/connection/%i' % newType.id)
    else:
        referer = force_text(
            request.META.get('HTTP_REFERER'),
            strings_only=True,
            errors='replace'
        )
        print(referer)
        if referer is None:
           # print('keine Weiterleitung')
            request.session[refererName] = ""
        else:
            referer = re.sub('^https?:\/\/', '', referer).split('/')
            referer = u'/' + u'/'.join(referer[1:])
         #   print(referer)
            request.session[refererName] = referer
        form = ConnectionForm()



    variables = Context({
        'requestref': request.session[refererName],
        'form': form, })
    return render(request, 'connections/connection_new.html', variables)


def connection(request, connID):
    refererName = "refererEditConnection"

    formsetPartner = forms.models.inlineformset_factory(Connection,
                                                    ConnectionPartner,
                                                    fields=('connection',
                                                            'device',
                                                            'master',),
                                                    extra=2,
                                                    )
  #  formsetParInt =formset_factory(form=ParameterIntForm)
    formsetParInt = forms.models.inlineformset_factory(Connection,ParameterInt,
                                                       fields=('connection',
                                                               'name','value'),
                                                       extra=2,
                                                       )
    formsetParText100 = forms.models.inlineformset_factory(Connection, ParameterText100,
                                                       fields=('connection',
                                                               'name', 'value'),
                                                       extra=2,
                                                       )
    formsetParBoolan = forms.models.inlineformset_factory(Connection, ParameterBoolean,
                                                       fields=('connection',
                                                               'name', 'value'),
                                                       extra=2,
                                                       )
    formsetParIP = forms.models.inlineformset_factory(Connection, ParameterIP,
                                                       fields=('connection',
                                                               'name', 'value'),
                                                       extra=2,
                                                       )
    try:
        main_instance = Connection.objects.get(id=connID)

    except:
        raise Http404(_('Connection not found'))



    if request.method == 'POST':
        if 'cancel' in request.POST:
            return redirect(request.session[refererName])

        subformset = ConnectionForm(request.POST, instance=main_instance)
        subformsetPartner = formsetPartner(request.POST, instance=main_instance)
        subformsetInt = formsetParInt(request.POST,instance=main_instance)
        subformsetText100=formsetParText100(request.POST,instance=main_instance)
        subformsetBoolean = formsetParBoolan(request.POST, instance=main_instance)
        subformsetIP = formsetParIP(request.POST, instance=main_instance)
        if subformset.is_valid() and subformsetPartner.is_valid() and subformsetInt.is_valid() and subformsetText100.is_valid() and subformsetBoolean.is_valid() and subformsetIP.is_valid():
            subformset.save()
            subformsetPartner.save()
            subformsetInt.save()
            subformsetText100.save()
            subformsetBoolean.save()
            subformsetIP.save()

            for deviceForm in subformsetPartner:

                try:
                    device = deviceForm.cleaned_data.get('device')
                    if device:
                        publish.single("device/" + device.externalID, "connection", hostname="localhost")
                        print("device/" + device.externalID)
                except ConnectionRefusedError:
                    print("MQTT nicht erreichbar")
                    break

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
            if "/connection/add/" not in referer:
               # if "/devices/sensors/sensortype/" not in referer:
                    request.session[refererName] = referer
            else:
                request.session[refererName] = request.session['refererAddConnection']

        subformset = ConnectionForm(instance=main_instance)
        subformsetPartner = formsetPartner(instance=main_instance)
        subformsetInt = formsetParInt(instance=main_instance)
        subformsetText100 = formsetParText100(instance=main_instance)
        subformsetBoolean = formsetParBoolan(instance=main_instance)
        subformsetIP = formsetParIP(instance=main_instance)

    variables = Context({
        'connection': main_instance,
        'connectionProperties': subformset,
        'partnerProperties': subformsetPartner,
        'ParameterInt': subformsetInt,
        'ParameterText100':subformsetText100,
        'ParameterBoolean':subformsetBoolean,
        'ParameterIP':subformsetIP,
        'requestref': request.session[refererName],
    })

    return render(request, 'connections/connection_details.html', variables)