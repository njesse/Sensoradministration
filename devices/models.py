from django.db import models
import paho.mqtt.publish as publish
import datetime as dt
from django.utils.translation import ugettext as _
from lxml import etree
from django.conf import settings


tls = settings.TLS


class Device(models.Model):
    description = models.CharField(max_length=100)
    location = models.ForeignKey('locations.Location')
    externalID = models.CharField(max_length=100, blank=True)  # Inventarnummer o.ä.
    lastPing_send = models.DateTimeField(null=True, blank=True)
    lastPing_received = models.DateTimeField(null=True, blank=True)

    def __str__(self):  # __unicode__ on Python 2
        return self.description

    def sendPingViaMQTT(self):
        publish.single("device/" + self.externalID, "ping", hostname=settings.MQTT_HOST, tls=tls, port=8883)
        self.lastPing_send=dt.datetime.now()
        self.save()


    def getXML(self,root1):
        root = etree.SubElement(root1,"UAObject", BrowseName="0:" + self.description, NodeId="s=" + self.externalID,
                             ParentNodeId="s=" + self.location.getNodeID())
        DisplayName = etree.SubElement(root, "DisplayName")
        DisplayName.text = "BaseObjectType"
        Description = etree.SubElement(root, "Description")
        Description.text = "The base type for all object nodes."
        References = etree.SubElement(root, "References")
        ref = etree.SubElement(References, "Reference", IsForward="false", ReferenceType="Organizes")
        ref.text = "s=" +self.location.getNodeID()
        ref = etree.SubElement(References, "Reference", ReferenceType="HasTypeDefinition")
        ref.text = "i=58"

        return
       # return etree.tostring(root, pretty_print=True)

#  <UAObject BrowseName="0:AstroPi" NodeId="s=Prototyp" ParentNodeId="s=Tisch am Fenster">
 #   <DisplayName>BaseObjectType</DisplayName>
#    <Description>The base type for all object nodes.</Description>
#    <References>
#      <Reference IsForward="false" ReferenceType="Organizes">s=Tisch am Fenster</Reference>
#      <Reference ReferenceType="HasTypeDefinition">i=58</Reference>
 #   </References>
#  </UAObject>


class DeviceHasDevices(models.Model):
    parentDevice = models.ForeignKey(Device, related_name='parentDevice')
    childDevice = models.OneToOneField(Device, related_name='childDevice')
# if device gets internal connected and locations differ: ask for location and reset them

    def __str__(self):  # __unicode__ on Python 2
        return self.parentDevice.description + " / " + self.childDevice.description


class NonSensorDevice(models.Model):
    device = models.OneToOneField('Device')  # ForeignKey(Device, unique=True)
    interfaces = models.ManyToManyField('connectiontypes.ConnectionType', through='NonSensorDeviceHasInterfaces')

    def __str__(self):  # __unicode__ on Python 2
        return self.device.description + " "+ _("no Sensor")


class NonSensorDeviceHasInterfaces(models.Model):
    nonSensorDevice = models.ForeignKey(NonSensorDevice)
    connectionType = models.ForeignKey('connectiontypes.ConnectionType')
    quantity = models.IntegerField()

    def __str__(self):  # __unicode__ on Python 2
        return self.nonSensorDevice.device.description + " " + self.connectionType.connectionName
