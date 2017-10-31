import paho.mqtt.client as mqtt
from devices.models import Device
from django.utils import timezone
import ssl
from django.conf import settings

def on_connect(client, userdata, rc):
 #  client.subscribe("$SYS/#")
   client.subscribe("device/#")
   client.subscribe("location/#")

def on_message(client, userdata, msg):
  # print("Received message '" + str(msg.payload) + "' on topic '"
  #    + msg.topic + "' with QoS " + str(msg.qos))

   topic = str(msg.topic)
   message = str(msg.payload)
   if "device/" in topic and "pong" in message:
       device = topic.replace("device/","")
       devices = Device.objects.filter(externalID = device)

       for dev1 in devices:
           dev1.lastPing_received= timezone.now()
           dev1.save()

client = mqtt.Client()
client.tls_set(ca_certs=settings.MQTT_CERT, tls_version=ssl.PROTOCOL_TLSv1_1)

client.on_connect = on_connect
client.on_message = on_message

try:
    client.connect(settings.MQTT_HOST, 8883, 60)
except ConnectionRefusedError:
    print("MQTT not available: Connection refused")
except TimeoutError:
    print("MQTT not available: Timeout")