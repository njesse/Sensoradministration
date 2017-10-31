from rest_framework import serializers
from sensors.models import Sensor,SensorType,SensortypeCanMeasure,Measurement,PhysicalQuantity,Unit
from devices.models import Device
from connectiontypes.models import ConnectionType
from locations.models import Location,Building,Address,Room
from connections.models import ConnectionPartner,ParameterIP,Connection
from django.forms.models import model_to_dict


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ('sensortype', 'device')
        depth = 3


class SensorSerializerShort(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ('sensortype',)
        depth = 3


class DeviceSerializerShort(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Device
        fields = ('description', 'sensor')
        depth = 2


class PhysicalQuantitySerializer(serializers.ModelSerializer):

    class Meta:
        model = PhysicalQuantity
        fields = ('description',)


class UnitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Unit
        fields = ('description',)


class MeasurementSerializer(serializers.ModelSerializer):
    physicalQuantity = PhysicalQuantitySerializer()
    unit = UnitSerializer()

    class Meta:
        model = Measurement
        fields = ('physicalQuantity', 'unit', 'description')


class ConnectionTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ConnectionType
        fields = ('connectionName',)


class SensortypeSerializer(serializers.HyperlinkedModelSerializer):
    measurements = MeasurementSerializer(many=True)

    class Meta:
        model = SensorType
        fields = ('datasheet', 'typeName', 'measurements')


class SensortypeLocationSerializer(serializers.ModelSerializer):
    measurements = MeasurementSerializer(many=True)

    class Meta:
        model = SensorType
        fields = ('typeName', 'measurements')
        depth = 1


class SensorAtLocationSerializer(serializers.ModelSerializer):
    sensortype = SensortypeLocationSerializer(read_only=True)
    # desc = DeviceLocationSerializer(read_only=True)

    class Meta:
        model = Sensor
        fields = ('device', 'sensortype')
        depth = 1


class LocationSerializerDeviceView(serializers.ModelSerializer):
    mqttpath = serializers.SerializerMethodField()
#   sensors = serializers.SerializerMethodField()

    class Meta:
        model = Location
        fields = ('id', 'description', 'room', 'mqttpath')
        depth = 5

    def get_mqttpath(self, obj):
        if obj.room:
            return str(obj.room.building.address_id) + "/" + str(obj.room.building_id) + "/" + str(obj.room.id) + "/" + str(obj.id)
        else:
            return str(obj.id)


class LocationSerializer(serializers.ModelSerializer):
    sensors = SensorAtLocationSerializer(source='get_sensors', read_only=True, many=True) # get_sensors steht in model.py

#   sensors = serializers.SerializerMethodField()
    class Meta:
        model = Location
       # fields = ('description','device_set','sensors')
        fields = ('description', 'sensors')
        depth = 2


class ConnectionParametersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connection
        fields = ('id','externalID','type', 'parameterip_set', 'parametertext100_set')
        depth = 1

class ConnectionPartnerSerializer(serializers.ModelSerializer):
    connection = ConnectionParametersSerializer(read_only=True)

    class Meta:
        model = ConnectionPartner
        fields = ('id', 'device','master',  'parameterip_set', 'parametertext100_set','connection')
        depth = 3

class ConnectionPartnerSerializer1(serializers.ModelSerializer):

    class Meta:
        model = ConnectionPartner
        fields = ('id', )
        depth = 1

class ConnectionPartnerEditParameter(serializers.ModelSerializer):

    class Meta:
        model = ConnectionPartner
        fields = ('id','connection','device','master','parameterip_set','parametertext100_set')

class ConnectionPartnerEditParameterIPSerializer(serializers.ModelSerializer):


    class Meta:
        model = ParameterIP
        fields = ('id', 'connectionPartner','connection', 'name', 'value')
    #def create(self, validated_data):
    #    print(self)
            # Override default `.create()` method in order to properly add `sport` and `category` into the model
    #    connectionPartner = validated_data.pop('connectionPartner_id')
    #    parameterIP = ParameterIP.objects.create(sport=connectionPartner,**validated_data)
    #    return parameterIP






class DeviceSerializer(serializers.ModelSerializer):
    location = LocationSerializerDeviceView()
    sensor = SensorSerializerShort()
    connectionPartner = ConnectionPartnerSerializer(source='connectionpartner_set', read_only=True, many=True)

    class Meta:
        model = Device
        fields = ('id', 'description', 'externalID', 'sensor', 'location', 'connectionPartner')
        depth = 2


class RoomSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Room
        fields = ('description', 'number')

class BuildingSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Building
        fields = ('description',)

