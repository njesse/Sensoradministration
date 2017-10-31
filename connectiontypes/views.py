from django.shortcuts import render,redirect
from django.template import Context
from .models import ConnectionType,ConnectionHasParameter
from .forms import ConnectionTypeForm,TopologyForm
from django.http import HttpResponse,Http404
from django import forms
from django.utils.encoding import force_text
# Create your views here.
from django.utils.translation import ugettext as _
def connectiontype_overview(request):
    connectiontypes = ConnectionType.objects.all()
    variables = Context({
        'ConnectionTypes': connectiontypes
    })
    return render(request, 'connectiontypes/connectiontypes.html', variables)





def connectiontype_edit(request, typid):
    refererName = 'refererEditConnectionType'
    try:
        typ = ConnectionType.objects.get(id=typid)
    except:
        raise Http404(_('Sensor not found'))

    formsetdef = forms.models.inlineformset_factory(ConnectionType,
                                                      ConnectionHasParameter,
                                                      fields=('parameterName',
                                                               'isDeviceSpecific',
                                                              'format','size','needsToBePreset',),
                                                      extra=2,
                                                      )
    if request.method == 'POST':

        if 'cancel' in request.POST:
            return redirect(request.session[refererName])

        msFormset = formsetdef(request.POST, instance=typ)

        form = ConnectionTypeForm(request.POST, request.FILES, instance=typ)
        print(request.FILES)

        if msFormset.is_valid() and form.is_valid():
            print(msFormset.cleaned_data)

            print(form.cleaned_data)
            # Update Bezeichnung und Datei
            form.save()
            msFormset.save()
            form = ConnectionTypeForm(instance=typ, )
            msFormset = formsetdef(instance=typ, )
            variables = Context({
                'Connectiontype': typ,
                'form': form,
                'msFormset': msFormset,
                'requestref': request.session[refererName],

            })
        else:
            variables = Context({
                'Connectiontype': typ,
                'form': form,
                'msFormset': msFormset,
                'requestref': request.session[refererName],
            })

        if request.session[refererName]!="" and 'saveChangesBack' in request.POST:
             return redirect(request.session[refererName])

        return render(request, 'connectiontypes/connectiontype_details.html', variables)
    else:

        referer = force_text(
            request.META.get('HTTP_REFERER'),
            strings_only=True,
            errors='replace'
        )
        if "/connectiontypes/add" not in referer:
            if "connections/toplogy/add" not in referer:
                request.session[refererName] = referer
        else:
            request.session[refererName] = request.session['refererAddConnectiontype']
        form = ConnectionTypeForm(instance=typ, )
        msFormset = formsetdef(instance=typ,)
        variables = Context({
               'Connectiontype': typ,
               'form': form,
               'msFormset': msFormset,
                'requestref': request.session[refererName],
            })

        return render(request, 'connectiontypes/connectiontype_details.html', variables)


def connectiontype_add(request):
    refererName = 'refererAddConnectiontype'
    if request.method == 'POST':
      form = ConnectionTypeForm(request.POST)

      if form.is_valid():
          newType = form.save()
          return redirect('/connections/connectiontype/%i' % newType.id)

    else:
        referer = force_text(
            request.META.get('HTTP_REFERER'),
            strings_only=True,
            errors='replace'
        )
        if referer != request.build_absolute_uri('/connections/toplogy/add'):
            request.session[refererName] = referer
        form = ConnectionTypeForm()

    variables = Context({
        'requestref': request.session[refererName],
        'form': form, })
    return render(request, 'connectiontypes/connectiontype_new.html', variables)

def topology_add(request):
    refererName = 'refererAddTopology'
    if request.method == 'POST':
        form = TopologyForm(request.POST)
        if form.is_valid():
            form.save()
            if request.session[refererName] != "":
                return redirect(request.session[refererName])

    else:
        referer = force_text(
            request.META.get('HTTP_REFERER'),
            strings_only=True,
            errors='replace'
        )
        request.session[refererName] = referer
        form = TopologyForm()

    variables = Context({

        'requestref': request.session[refererName],
        'form': form, })
    return render(request, 'connectiontypes/topology_new.html', variables)
