from django.contrib import admin


from .models import ConnectionType, ConnectionHasParameter,  Topology


#class HavingParameters(admin.TabularInline):
#    model = ConnectionHasParameter
 #   extra = 1


#class ConnectionTypesAdmin(admin.ModelAdmin):
 #   inlines = (HavingParameters,)
  #   model = ConnectionType
    # filter_horizontal = ('parameters',)  # If you don't specify this, you will get a multiple select widget.


admin.site.register(ConnectionType) #, ConnectionTypesAdmin)
admin.site.register(ConnectionHasParameter)
#admin.site.register(ConnectionParameter)
admin.site.register(Topology)
