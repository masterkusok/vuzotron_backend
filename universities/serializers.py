from rest_framework import serializers

from specialities.serializers import SpecialitySerializer
from universities.models import University

LIST_UNIVERSITY_SERIALIZATION_FIELDS = ['id', 'short_name', 'region', 'city', 'full_name']


class SingleUniversitySerializer(serializers.ModelSerializer):
    speciality_list = SpecialitySerializer(many=True, source='specialities')

    class Meta:
        model = University
        fields = LIST_UNIVERSITY_SERIALIZATION_FIELDS + ['speciality_list']


class UniversityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = LIST_UNIVERSITY_SERIALIZATION_FIELDS
