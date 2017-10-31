"""AtorProjekt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import os.path

from django.conf.urls import url, include
from django.conf import settings
from django.contrib import admin
from Ator.views import *
from django.conf.urls import url
from django.contrib import admin
from Ator.views import *
from sensors.views import *
from devices.views import *
from locations.views import *
from connectiontypes.views import *
from connections.views import *
from django.contrib.auth.views import login
from django.views.static import serve
from django.conf.urls.static import static
from rest_framework import routers
from restInterface import views

router = routers.DefaultRouter()
router.register(r'rest/sensors', views.SensorViewSet)
router.register(r'rest/devices', views.DeviceViewSet)
router.register(r'rest/device', views.DeviceViewSetExternalID)
router.register(r'rest/sensortypes', views.SensorTypeViewSet)
router.register(r'rest/locations', views.LocationViewSet)
router.register(r'rest/measurements', views.MeasurementViewSet)
router.register(r'rest/connectiontypes', views.ConnectionTypeViewSet)
router.register(r'rest/rooms', views.RoomViewSet)
router.register(r'rest/buildings', views.BuildingViewSet)
router.register(r'rest/connectionpartnerIP',views.ConnectionPartnerParameterIPViewSet)
router.register(r'rest/connectionpartner',views.ConnectionPartnerParameterViewSet)
#router.register(r'rest/sensorsat/(?P<id>\d+)', views.SensorsAtLocation)



site_media = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'site_media')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', main_page),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #url(r'^devices/sensors/sensortype/(\d+)/$',sensortypes_page),
    url(r'^devices/sensors/sensortype/(\d+)/$', sensortype_edit),
    url(r'^devices/sensors/sensortype/add$', sensortype_new),
    url(r'^devices/sensors/add/$', sensor_add, name="url_addSensor"),
    url(r'^login/$', login),
    url(r'^logout/$', logout_page),
    url(r'^site_media/(?P<path>.*)$', serve, {'document_root': site_media}),
    url(r'^devices/sensors/$', sensors_overview, name="url_sensors"),
    url(r'^devices/$', devices_overview, name="url_devices"),
    url(r'^device/(\d+)/$', device, name="url_device"),
    url(r'^device/ping/(\d+)/$', device_pingMQTT, name="url_device_ping"),
    url(r'^devices/sensors/sensortypes/$', sensortypes_overview, name="url_sensortypes"),
    url(r'^devices/sensor/(\d+)/$', sensor, name="url_sensor"),
    url(r'^location/(\d+)/$', location, name="url_location"),
    url(r'^locations/$', locations_overview, name="url_locations"),
    url(r'^locations/add/$', location_add, name="url_addlocation"),
    url(r'^locations/buildings/add/$', location_Addresses, name="url_addresses"),
    url(r'^locations/room/(\d+)/$', location_EditRoom, name="url_editRoom"),
    url(r'^locations/building/(\d+)/$', location_EditBuilding, name="url_editBuilding"),
    url(r'^locations/address/(\d+)/$', location_EditAddress, name="url_editAddress"),
    url(r'^locations/management', location_management, name="url_managelocations"),
    url(r'^connections/connectiontypes/$', connectiontype_overview, name="url_connectiontypes"),
    url(r'^connections/connectiontypes/add/$', connectiontype_add, name="url_addconnectiontype"),
    url(r'^connections/connectiontype/(\d+)/$', connectiontype_edit, name="url_editConnectionType"),
    url(r'^connections/toplogy/add/$', topology_add, name="url_addTopology"),
    url(r'^connections/$', connections_overview, name="url_connections"),
    url(r'^connection/add/$', connection_add, name="url_addconnection"),
    url(r'^connection/(\d+)/$', connection, name="url_connection"),
    url(r'^rest/sensorsat/(\d+)/$', views.SensorsAtLocation, name="url_sensorsAtLocation"),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


from . import mqtt
mqtt.client.loop_start()

from . import opcua
opcua.printXML()
