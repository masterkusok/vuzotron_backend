from rest_framework import serializers

from specialities.models import Speciality

SPECIALITY_SERIALIZATION_FIELDS = ['code', 'form', 'level', 'name']


class SpecialitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Speciality
        fields = SPECIALITY_SERIALIZATION_FIELDS
