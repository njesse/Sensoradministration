from django.db import models
from django.utils.translation import ugettext as _

class Sensor(models.Model):
    device = models.OneToOneField('devices.Device')  # ForeignKey(Device, unique=True)
    sensortype = models.ForeignKey('SensorType')

    # measurement=models.ForeignKey('Measurement')

    def __str__(self):  # __unicode__ on Python 2
        return self.device.description + " " +_("Type:")+" " + self.sensortype.typeName







def user_directory_path(instance, filename):
    return 'datasheets/{1}'.format(instance.id, filename)

class SensorType(models.Model):
    typeName = models.CharField(max_length=100)
    measurements = models.ManyToManyField('Measurement', through='SensortypeCanMeasure')
    interfaces = models.ManyToManyField('connectiontypes.ConnectionType', through='SensorTypeHasInterfaces')
    datasheet = models.FileField(upload_to=user_directory_path, blank=True)
    description = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):  # __unicode__ on Python 2
        return self.typeName

class Unit(models.Model):
    description = models.CharField(max_length=30, unique=True)

    def __str__(self):  # __unicode__ on Python 2
        return self.description

class SensortypeCanMeasure(models.Model):
    sensorType = models.ForeignKey(SensorType)
    measurement = models.ForeignKey('Measurement')
    rangeMin = models.CharField("Measuring range lower limit", max_length=20, blank=True)
    rangeMax = models.CharField("Measuring range upper limit", max_length=20, blank=True)
    accuracy =models.FloatField(blank=True, null=True)
    accuracyUnit = models.ForeignKey(Unit, blank=True, null=True)

    def __str__(self):  # __unicode__ on Python 2
        return self.sensorType.typeName + " "+_("can measure") +" " + self.measurement.__str__()


class SensorMeasures(models.Model):
    sensor = models.ForeignKey(Sensor)
    measurement = models.ForeignKey('SensortypeCanMeasure')
    process = models.CharField(max_length=100, blank=True)
    outputFormat = models.CharField(max_length=100, blank=True)


class SensorTypeHasInterfaces(models.Model):
    sensorType = models.ForeignKey(SensorType)
    connectionType = models.ForeignKey('connectiontypes.ConnectionType')
    quantity = models.IntegerField()

    def __str__(self):  # __unicode__ on Python 2
        return self.sensorType.typeName + " "+_("has") + " " + self.connectionType.connectionName

    class Meta:
        unique_together = ("sensorType", "connectionType")


class PhysicalQuantity(models.Model):
    description = models.CharField(max_length=30)

    def __str__(self):  # __unicode__ on Python 2
        return self.description





class Measurement(models.Model):
    physicalQuantity = models.ForeignKey(PhysicalQuantity)
    unit = models.ForeignKey(Unit)
    description = models.CharField(max_length=100, blank=True)

    def __str__(self):  # __unicode__ on Python 2
        return self.physicalQuantity.description + " in " + self.unit.description

