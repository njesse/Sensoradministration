from django.contrib import admin
from .models import Connection, ConnectionPartner, ParameterBoolean, ParameterInt, ParameterText100, ParameterIP
# Register your models here.


class ParIntInline(admin.StackedInline):
    model = ParameterInt


class ParBooleanInline(admin.StackedInline):
    model = ParameterBoolean


class ParIPInline(admin.StackedInline):
    model = ParameterIP


class ParTxt100Inline(admin.StackedInline):
    model = ParameterText100


class ExtendedParameterAdmin(admin.ModelAdmin):
    inlines = (ParIntInline,) + (ParBooleanInline,) + (ParIPInline,) + (ParTxt100Inline,)


class DevicesInline(admin.TabularInline):
    model = ConnectionPartner
    extra = 2


class ConnectionAdmin(admin.ModelAdmin):
    inlines = (DevicesInline,)


admin.site.register(Connection, ConnectionAdmin)
admin.site.register(ConnectionPartner)
admin.site.register(ParameterBoolean)
admin.site.register(ParameterInt)
admin.site.register(ParameterText100)
admin.site.register(ParameterIP)
#admin.site.register(Parameter, ExtendedParameterAdmin)


