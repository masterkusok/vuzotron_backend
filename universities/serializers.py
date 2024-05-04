from rest_framework import serializers

from specialities.serializers import SpecialitySerializer
from universities.models import University

UNIVERSITY_SERIALIZATION_FIELDS = ['short_name', 'region', 'city', 'full_name', 'speciality_list']


class UniversitySerializer(serializers.ModelSerializer):
    speciality_list = SpecialitySerializer(many=True, source='specialities')

    class Meta:
        model = University
        fields = UNIVERSITY_SERIALIZATION_FIELDS
