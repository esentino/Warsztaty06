from rest_framework import serializers
from .models import Movie, Person, MoviePerson
from django.db import IntegrityError

class PersonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Person
        fields = ('id', 'name',)

class PersonRoleSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField(source='person.id')
    name = serializers.ReadOnlyField(source='person.name')
    movie_name = serializers.ReadOnlyField(source='movie.title')
    class Meta:
        model = MoviePerson
        fields = ('role','id', 'name', 'movie_name')


class MovieSerializer(serializers.HyperlinkedModelSerializer):
    director = PersonSerializer(many=False, read_only=True)
    actors = PersonRoleSerializer(source='movieperson_set', many=True)
    class Meta:
        model = Movie
        fields = ('title', 'description', 'year', 'director', 'actors')

class MovieAddSerializer(serializers.HyperlinkedModelSerializer):
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
