from django.contrib import admin
from .models import SensorType, Measurement, SensortypeCanMeasure, PhysicalQuantity, Unit, Sensor, SensorTypeHasInterfaces
# Register your models here.

admin.site.register(Sensor)
admin.site.register(SensorType)
admin.site.register(Measurement)
admin.site.register(PhysicalQuantity)
admin.site.register(Unit)
admin.site.register(SensortypeCanMeasure)
admin.site.register(SensorTypeHasInterfaces)
