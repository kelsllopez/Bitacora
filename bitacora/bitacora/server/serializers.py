from rest_framework import serializers
from .models import *

class BitacoraAccesoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BitacoraAcceso
        fields = '__all__'
