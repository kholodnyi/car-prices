from rest_framework import serializers

from ..models import CarMaker, CarModel, Province, City


class CarModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = ['id', 'name']


class CarMakerSerializer(serializers.ModelSerializer):
    carmodel_set = CarModelSerializer(many=True)

    class Meta:
        model = CarMaker
        fields = ['id', 'name', 'carmodel_set']


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name']


class ProvinceSerializer(serializers.ModelSerializer):
    city_set = CitySerializer(many=True)

    class Meta:
        model = Province
        fields = ['id', 'name', 'city_set']