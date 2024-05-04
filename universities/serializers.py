from rest_framework import serializers

from universities.models import University

UNIVERSITY_SERIALIZATION_FIELDS = ['short_name', 'region', 'city', 'full_name', 'specialities']


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = UNIVERSITY_SERIALIZATION_FIELDS
