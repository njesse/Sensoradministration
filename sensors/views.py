from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404,HttpResponseRedirect
from .models import Sensor, SensorType,SensortypeCanMeasure,SensorTypeHasInterfaces
from .forms import SensorTypeForm #,SensortypeFormSet

import re
from django.template import Context
from django.template.loader import get_template
from django.template import RequestContext
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django import forms
from django.utils.encoding import force_text
from django.utils.translation import ugettext as _
def sensortypes_page(request, sensortypid):
    try:
        typ = SensorType.objects.get(id=sensortypid)
    except:
        raise Http404(_('Sensor not found'))
    measurements = typ.measurements.all()
    variables = Context({
        'Sensortype': typ.typeName,
        'Measurements': measurements,
    })
    return render(request, 'sensortypes/sensortype_details.html', variables)


def sensortypes_overview(request):
    sensortypes = SensorType.objects.all()
    variables = Context({
        'Sensortypes': sensortypes
    })
    return render(request, 'sensortypes/sensortypes.html', variables)

def sensors_overview(request):
    sensors = Sensor.objects.all()

    variables = Context({
        'Sensors': sensors,
    })
    return render(request, 'sensors/sensors.html', variables)


def sensortype_new(request):

    if request.method == 'POST':
        form = SensorTypeForm(request.POST, request.FILES)

        if form.is_valid():
            newType = form.save()

            return redirect('/devices/sensors/sensortype/%i' % newType.id)

    else:
        form = SensorTypeForm()

        referer = force_text(
            request.META.get('HTTP_REFERER'),
            strings_only=True,
            errors='replace'
        )
        if referer is None:
            print('keine Weiterleitung')
            request.session['refererAddType'] = ""
        else:
            referer = re.sub('^https?:\/\/', '', referer).split('/')
            referer = u'/' + u'/'.join(referer[1:])
            print(referer)
            request.session['refererAddType'] = referer



    variables = Context({
            'form': form
         })
    return render(request, 'sensortypes/sensortype_new.html', variables)





def sensortype_edit(request, sensortypid):

    try:
        typ = SensorType.objects.get(id=sensortypid)
    except:
        raise Http404(_('Sensor not found'))

    msformsetdef = forms.models.inlineformset_factory(SensorType,
                                                      SensortypeCanMeasure,
                                                      fields=('sensorType',
                                                              'measurement', 'rangeMin', 'rangeMax',),
                                                      extra=2,
                                                      widgets={'rangeMin': forms.TextInput(attrs={'size': '5'}),
                                                               'rangeMax': forms.TextInput(attrs={'size': '5'})})
    intformsetdef = forms.models.inlineformset_factory(SensorType,
                                                       SensorTypeHasInterfaces,
                                                       fields=('sensorType', 'connectionType', 'quantity',),
                                                       extra=2,
                                                       widgets={'quantity': forms.TextInput(attrs={'size': '5'})})


    if request.method == 'POST':

        if 'cancel' in request.POST:
            return redirect(request.session['refererAddType'])

        msFormset = msformsetdef(request.POST, instance=typ)
        intFormset = intformsetdef(request.POST, instance=typ)
        form = SensorTypeForm(request.POST, request.FILES, instance=typ)
        print(request.FILES)

        if msFormset.is_valid() and intFormset.is_valid() and form.is_valid():
            print(msFormset.cleaned_data)
            print(intFormset.cleaned_data)
            print(form.cleaned_data)
            # Update Bezeichnung und Datei
            form.save()

            intFormset.save()


            msFormset.save()

            form = SensorTypeForm(instance=typ, )
            msFormset = msformsetdef(instance=typ, )
            intFormset = intformsetdef(instance=typ, )
            variables = Context({
                'Sensortype': typ,
                'form': form,
                'msFormset': msFormset,
                'intFormset': intFormset,
                'requestref': request.session['refererAddType'],

            })
        else:
            variables = Context({
                'Sensortype': typ,
                'form': form,
                'msFormset': msFormset,
                'intFormset': intFormset,
                'requestref': request.session['refererAddType'],
            })

        if request.session['refererAddType']!="" and 'saveChangesBack' in request.POST:
             return redirect(request.session['refererAddType'])

        return render(request, 'sensortypes/sensortype_details.html', variables)
    else:

        referer = force_text(
            request.META.get('HTTP_REFERER'),
            strings_only=True,
            errors='replace'
        )
        if referer != request.build_absolute_uri('/devices/sensors/sensortype/add') and  referer != request.build_absolute_uri('/connections/connectiontypes/add/') and not '/connections/connectiontype' in referer :
            request.session['refererAddType'] = referer

        form = SensorTypeForm(instance=typ, )
        msFormset = msformsetdef(instance=typ,)
        intFormset=intformsetdef(instance=typ,)
        variables = Context({
               'Sensortype': typ,
               'form': form,
               'msFormset': msFormset,
               'intFormset': intFormset,
                'requestref': request.session['refererAddType'],
            })

        return render(request, 'sensortypes/sensortype_details.html', variables)



