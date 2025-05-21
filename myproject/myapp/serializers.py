from rest_framework import serializers
from .models import Tree, Equipment, PlantingLocation

class TreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tree
        fields = '__all__'

class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = '__all__'

class PlantingLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantingLocation
        fields = '__all__'