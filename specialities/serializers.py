from rest_framework import serializers

from specialities.models import Speciality

SPECIALITY_SERIALIZATION_FIELDS = ['id', 'code', 'form', 'level', 'name']


class SpecialitySerializer(serializers.ModelSerializer):
    """
    Speciality serializer class
    """
    class Meta:
        model = Speciality
        fields = SPECIALITY_SERIALIZATION_FIELDS
