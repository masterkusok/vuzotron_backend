from rest_framework import serializers

from specialities.models import Speciality

SPECIALITY_SERIALIZATION_FIELDS = {'code': str, 'form': str, 'level': str, 'name': str}


class SpecialitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Speciality
        fields = [key for key in SPECIALITY_SERIALIZATION_FIELDS.keys()]
