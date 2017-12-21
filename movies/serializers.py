"""Serialize module"""
from rest_framework import serializers
from django.db import IntegrityError
from .models import Movie, Person, MoviePerson

class PersonIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('id',)

class PersonSerializer(serializers.ModelSerializer):
    """Serializer for Person model"""
    class Meta:
        model = Person
        fields = ('id', 'name',)

class PersonRoleSerializer(serializers.ModelSerializer):
    """Serializer for role with person information"""
    id = serializers.ReadOnlyField(source='person.id')
    name = serializers.ReadOnlyField(source='person.name')
    movie_name = serializers.ReadOnlyField(source='movie.title')

    class Meta:
        model = MoviePerson
        fields = ('role','id', 'name', 'movie_name')



class MovieSerializer(serializers.ModelSerializer):
    """Serializer for movie model with director and actors"""
    director = PersonSerializer(many=False, allow_null=True, read_only=True)
    actors = PersonRoleSerializer(source='movieperson_set', many=True, read_only=True)
    class Meta:
        model = Movie
        fields = ('title', 'description', 'year', 'director', 'actors')

class MovieAddSerializer(serializers.ModelSerializer):
    director_id = serializers.IntegerField()
    class Meta:
        model = Movie
        fields = ('title', 'description', 'year', 'director_id')
    def create(self, validated_data):
        nowy = Movie(**validated_data)
        try:
            nowy.save()
        except IntegrityError:
            return nowy
        return nowy
