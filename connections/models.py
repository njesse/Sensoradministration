from django.db import models
from django.core.exceptions import ValidationError


class Connection(models.Model):
    description = models.CharField(max_length=100)
    externalID = models.CharField(max_length=100, blank=True)
    type = models.ForeignKey('connectiontypes.ConnectionType')
    devices = models.ManyToManyField('devices.Device', through='ConnectionPartner')

    def __str__(self):  # __unicode__ on Python 2
        return self.description


class ConnectionPartner(models.Model):
    connection = models.ForeignKey(Connection)
    device = models.ForeignKey('devices.Device')
    master = models.BooleanField()

    def __str__(self):  # __unicode__ on Python 2
        return self.device.description + " @ " + self.connection.description


# class Parameter(models.Model):
    # Type_Choices = (
    #     ("Int", "Integer"),                       would cause redundancy but might be necessary in the future
    #     ("bool", "Boolean"),
    #     ("char100", "Character, Size 100"),
    # )
    # parameterType = models.CharField(max_length=10, choices=Type_Choices)

    #parameterName = models.CharField(max_length=100)
    #connectionPartner = models.ForeignKey(ConnectionPartner, null=True, blank=True)
    #connection = models.ForeignKey(Connection, null=True, blank=True)

    #def __str__(self):  # __unicode__ on Python 2
     #   return self.parameterName


class ParameterIP(models.Model):
    name = models.CharField(max_length=100)
    connectionPartner = models.ForeignKey(ConnectionPartner, null=True, blank=True)
    connection = models.ForeignKey(Connection, null=True, blank=True)
    value = models.GenericIPAddressField()

    def __str__(self):
        return self.name + " = " + self.value


class ParameterInt(models.Model):
    name = models.CharField(max_length=100)
    connectionPartner = models.ForeignKey(ConnectionPartner, null=True, blank=True)
    connection = models.ForeignKey(Connection, null=True, blank=True)
    value = models.IntegerField()

    def __str__(self):
        return self.name + " = %i" % self.value


class ParameterText100(models.Model):
    name = models.CharField(max_length=100)
    connectionPartner = models.ForeignKey(ConnectionPartner, null=True, blank=True)
    connection = models.ForeignKey(Connection, null=True, blank=True)
    value = models.CharField(max_length=100)

    def __str__(self):
        return self.name + " = " + self.value


class ParameterBoolean(models.Model):
    name = models.CharField(max_length=100)
    connectionPartner = models.ForeignKey(ConnectionPartner, null=True, blank=True)
    connection = models.ForeignKey(Connection, null=True, blank=True)
    value = models.BooleanField()

    def __str__(self):
        return self.name + " = %s" % self.value




