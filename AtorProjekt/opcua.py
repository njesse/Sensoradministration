from devices.models import Device
from locations.models import Building,Room,Location
from lxml import etree
import xml.etree.ElementTree as Et

def printXML():

    NSMAP ={None: 'http://opcfoundation.org/UA/2011/03/UANodeSet.xsd',
                                  'uax': 'http://opcfoundation.org/UA/2008/02/Types.xsd',
                                 'xsd': 'http://www.w3.org/2001/XMLSchema',
                                  'xsi': 'http://www.w3.org/2001/XMLSchema-instance', }  # the default namespace (no prefix)
    root = etree.Element("UANodeSet", nsmap=NSMAP)  # lxml only!

    etree.SubElement(root, "NamespaceUris")
    aliases = etree.SubElement(root,"Aliases")
    alias = etree.SubElement(aliases,"Aliase",Alias = "Organizes")
    alias.text ="i=35"
    alias = etree.SubElement(aliases, "Aliase", Alias="HasTypeDefinition")
    alias.text = "i=40"

    buildings = Building.objects.all()
    for b in buildings:
        b.getXML(root)
    rooms = Room.objects.all()
    for r in rooms:
        r.getXML(root)
    locations = Location.objects.all()
    for l in locations:
        l.getXML(root)
    devices = Device.objects.all()
    for d in devices:
        d.getXML(root)

    tree = Et.ElementTree(root)

    xml = etree.tostring(root, pretty_print=True, xml_declaration=True)

    f = open("output.xml", "wb")
    f.write(xml)
    f.close()

    #with open("output.xml", 'w', encoding='utf-8') as file:
     #  tree.write(file, encoding='unicode')
