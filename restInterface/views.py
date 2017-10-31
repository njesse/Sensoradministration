from django.shortcuts import render
from rest_framework import viewsets,status
from restInterface.serializers import SensorSerializer, DeviceSerializer, SensortypeSerializer, LocationSerializer, \
    RoomSerializer, MeasurementSerializer, ConnectionTypeSerializer, BuildingSerializer, ConnectionPartnerSerializer, \
    ConnectionPartnerEditParameterIPSerializer, ConnectionPartnerEditParameter
from sensors.models import Sensor, SensorType, SensortypeCanMeasure, Measurement
from connectiontypes.models import ConnectionType
from connections.models import ConnectionPartner, ParameterIP
from devices.models import Device
from locations.models import Location, Room, Building, Address
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser


from rest_framework import generics
# Create your views here.


class SensorViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


class MeasurementViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer


class ConnectionTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ConnectionType.objects.all()
    serializer_class = ConnectionTypeSerializer


class DeviceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


class DeviceViewSetExternalID(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'externalID'
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


class SensorTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SensorType.objects.all()
    serializer_class = SensortypeSerializer


class LocationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class RoomViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class BuildingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer

class ConnectionPartnerParameterViewSet(viewsets.ModelViewSet):
    lookup_field = 'device'
    queryset = ConnectionPartner.objects.all()
    serializer_class = ConnectionPartnerEditParameter

class ConnectionPartnerParameterIPViewSet(viewsets.ModelViewSet):
    lookup_field = 'connectionPartner'
    queryset = ParameterIP.objects.all()
    serializer_class = ConnectionPartnerEditParameterIPSerializer


 #   def create(self, request):
 #       serializer = self.serializer_class(data=request.data)

  #      if serializer.is_valid():
  #          ParameterIP.objects.create_user(**serializer.validated_data)

  #          return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

   #     return Response({
   #         'status': 'Bad request',
   #         'message': 'Account could not be created with received data.'
   #     }, status=status.HTTP_400_BAD_REQUEST)


# class SensorsAtLocationViewSet(viewsets.ReadOnlyModelViewSet):
    #   print(id)

#   queryset = Sensor.objects.filter(device__location="5")
#   serializer_class = SensorSerializer

def SensorsAtLocation(request, id):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        location = Location.objects.get(id=id)
    except Location.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        queryset = Sensor.objects.filter(device__location=location.id)
        serializer = SensorSerializer(queryset, many=True)
        return JSONResponse(serializer.data)


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)
