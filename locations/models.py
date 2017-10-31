from django.db import models
from devices.models import Device
from sensors.models import Sensor, SensorType

from lxml import etree

# Create your models here.

# Location
# official address
# building
# room nr.
# location description


class Address(models.Model):
    addressLine1 = models.CharField(max_length=100)
    addressLine2 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    zip = models.CharField(max_length=10, blank=True)
    country = models.CharField(max_length=30, blank=True)

    def __str__(self):  # __unicode__ on Python 2
        return self.addressLine1 + " " + self.addressLine2 + " " + self.zip + " " + self.city


class Building(models.Model):
    address = models.ForeignKey(Address)
    description = models.CharField(max_length=100)

    def __str__(self):  # __unicode__ on Python 2
        return self.description + " (" + self.address.__str__() + ")"

    def getNodeID(self):
        return self.description + "_"+self.address.addressLine1

    def getXML(self,root1):
       root = etree.SubElement(root1,"UAObject", BrowseName="0:" +self.description, NodeId="s="+self.getNodeID(), ParentNodeId="i=85")
       #root = etree.Element("UAObject", BrowseName="0:" +self.description, NodeId="s="+self.description, ParentNodeId="i=85")
       DisplayName = etree.SubElement(root, "DisplayName")
       DisplayName.text = self.description
       Description = etree.SubElement(root,"Description")
       Description.text=self.description
       References = etree.SubElement(root, "References")
       ref = etree.SubElement(References, "Reference",IsForward="false", ReferenceType="Organizes" )
       ref.text="i=85"
       ref = etree.SubElement(References, "Reference",  ReferenceType="HasTypeDefinition")
       ref.text = "i=61"

       for room in self.room_set.all():
           ref = etree.SubElement(References, "Reference", ReferenceType="Organizes")
           ref.text = "s="+room.getNodeID()

       return


#  <UAObject BrowseName="0:HauptgebÃ¤ude" NodeId="s=HauptgebÃ¤ude" ParentNodeId="i=85">
#    <DisplayName>HauptgebÃ¤ude</DisplayName>
#    <Description>HauptgebÃ¤ude</Description>
#    <References>
#      <Reference IsForward="false" ReferenceType="Organizes">i=85</Reference>
#      <Reference ReferenceType="HasTypeDefinition">i=61</Reference>
#      <Reference ReferenceType="Organizes">s=H313</Reference>
#      <Reference ReferenceType="Organizes">s=Aula</Reference>
#    </References>
#  </UAObject>

class Room(models.Model):
    building = models.ForeignKey(Building)
    number = models.CharField("Number or Name", max_length=30)
    description = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.number + " " + self.description + " (" + self.building.description + ")"

    def getNodeID(self):
        return self.number+"_"+self.building.getNodeID()

    def getXML(self,root1):
       root = etree.SubElement(root1,"UAObject", BrowseName="0:" +self.number, NodeId="s="+self.getNodeID(), ParentNodeId="s="+self.building.getNodeID())
       DisplayName = etree.SubElement(root, "DisplayName")
       DisplayName.text = self.number
       Description = etree.SubElement(root,"Description")
       Description.text=self.number
       References = etree.SubElement(root, "References")
       ref = etree.SubElement(References, "Reference",IsForward="false", ReferenceType="Organizes" )
       ref.text="s="+self.building.getNodeID()
       ref = etree.SubElement(References, "Reference",  ReferenceType="HasTypeDefinition")
       ref.text = "i=61"

       for location in self.location_set.all():
           ref = etree.SubElement(References, "Reference", ReferenceType="Organizes")
           ref.text = "s="+location.getNodeID()
       return

 #   < UAObject  BrowseName = "0:H313"  NodeId = "s=H313"
 #   ParentNodeId = "s=Hauptgeb&#228;ude" >
 #   < DisplayName > H313 < / DisplayName >
#    < Description > H313 < / Description >
#    < References >
 #   < Reference
 #   IsForward = "false"
#    ReferenceType = "Organizes" > s = Hauptgebäude < / Reference >
 #   < Reference
 #   ReferenceType = "HasTypeDefinition" > i = 61 < / Reference >
#    < Reference
 #   ReferenceType = "Organizes" > s = Tisch am
 #   Fenster < / Reference >
  #  < Reference
 #   ReferenceType = "Organizes" > s = Schreibtisch < / Reference >
#< / References >
#< / UAObject >


class Location(models.Model):
    room = models.ForeignKey(Room, blank=True, null=True)
    description = models.CharField(max_length=100)
    lat = models.FloatField("Latitude", blank=True, null=True)
    lon = models.FloatField("Longitude", blank=True, null=True)

    def __str__(self):
        if self.room:
            return self.description  + " @ " + self.room.number
        else:
            return self.description

    def get_sensors(self):
        devices = Device.objects.filter(location=self)
        print(devices)
        sensors = Sensor.objects.filter(device__in=devices)
        print(sensors)

        return sensors

    def getNodeID(self):
        if self.room:
            return self.description+ "_"+ self.room.getNodeID();
        else:
            return self.description


    def getXML(self, root1):
        if self.room:
            root = etree.SubElement(root1, "UAObject", BrowseName="0:" + self.description,
                                    NodeId="s=" + self.getNodeID(),
                                    ParentNodeId="s=" + self.room.getNodeID())
        else:
            root = etree.SubElement(root1, "UAObject", BrowseName="0:" + self.description,
                                    NodeId="s=" + self.getNodeID(),
                                    ParentNodeId = "i=85" )

        DisplayName = etree.SubElement(root, "DisplayName")
        DisplayName.text = self.description
        Description = etree.SubElement(root, "Description")
        Description.text = self.description
        References = etree.SubElement(root, "References")
        ref = etree.SubElement(References, "Reference", IsForward="false", ReferenceType="Organizes")
        if self.room:
            ref.text = "s=" + self.room.getNodeID()
        else:
            ref.text = "i=85"
        ref = etree.SubElement(References, "Reference", ReferenceType="HasTypeDefinition")
        ref.text = "i=61"


        for dev in Device.objects.filter(location=self):
            ref = etree.SubElement(References, "Reference", ReferenceType="Organizes")
            ref.text = "s=" + dev.externalID
        return


 # <UAObject BrowseName="0:Schreibtisch" NodeId="s=Schreibtisch" ParentNodeId="s=H313">
 #   <DisplayName>Schreibtisch</DisplayName>
 #   <Description>Schreibtisch</Description>
 #   <References>
 #     <Reference IsForward="false" ReferenceType="Organizes">s=H313</Reference>
  #    <Reference ReferenceType="HasTypeDefinition">i=61</Reference>
  #      < Reference ReferenceType = "Organizes" > s = Prototyp < / Reference >

        #  </References>
#  </UAObject>
