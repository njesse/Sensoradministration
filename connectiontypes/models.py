from django.utils.translation import ugettext as _
from django.db import models
# Create your models here.


#class ConnectionParameter(models.Model):
 #   formatChoices = (
   #     ('int', 'Integer'),
   #     ('txt', 'Text'),
   #     ('bin', 'Binary'),
  #      ('Bit', 'Bits'),
  #      ('Byte', 'Byte'),
  #      ('IP', 'IP Address'),
  #  )
   # parameterName = models.CharField(max_length=20)
  #  format = models.CharField(max_length=10, choices=formatChoices, default='txt')
 #   size = models.IntegerField()

 #   def __str__(self):  # __unicode__ on Python 2
  #
#       return self.parameterName


class ConnectionType(models.Model):
    connectionName = models.CharField(max_length=50)
    topology = models.ForeignKey('Topology')

    def __str__(self):  # __unicode__ on Python 2
        return self.connectionName


class ConnectionHasParameter(models.Model):
    formatChoices = (
        ('int', 'Integer'),
        ('txt', 'Text'),
        ('IP', _('IP Address')),
        ('bool', 'Boolean'),

    )
    connectiontype = models.ForeignKey('ConnectionType')
    parameterName = models.CharField(max_length=20)
    isDeviceSpecific = models.BooleanField(default=False)
    needsToBePreset = models.BooleanField(default=False)
    format = models.CharField(max_length=10, choices=formatChoices, default='txt')
    size = models.IntegerField()

    def __str__(self):  # __unicode__ on Python 2
        return self.parameterName


class Topology(models.Model):
    topologyName = models.CharField(max_length=20)
    # image

    def __str__(self):  # __unicode__ on Python 2
        return self.topologyName

    class Meta:
        verbose_name_plural = "topologies"
