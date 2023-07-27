from rest_framework import serializers
from .models import InputValue


class InputValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = InputValue
        fields = ('timestamp','input_values')