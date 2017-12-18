from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT
from django.http import Http404
from .models import Movie, Person
from .serializers import MovieSerializer, MovieAddSerializer, PersonSerializer, PersonIdSerializer
# Create your views here.


class MoviesView(APIView):
    def get(self, request, format=None):
        all_movie = Movie.objects.all()
        serialize_movie = MovieSerializer(all_movie, 
                                          context={"request": request}, 
                                          many=True)
        return Response(serialize_movie.data)
    
    def post(self, request, format=None):
        serialize_move = MovieSerializer(data=request.data)
        if serialize_move.is_valid():
            serialize_move.save()
            return Response(serialize_move.data)
        return Response(serialize_move.errors, status=HTTP_400_BAD_REQUEST)

class MovieView(APIView):
    def get_object(self, pk):
        try:
            return Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            raise Http404
    def get(self, request, id):
        selected_movie = self.get_object(id)
        movie_serializer = MovieSerializer(selected_movie,
                                           context={"request": request})
        return Response(movie_serializer.data)
    def delete(self, request, id):
        selected_movie = self.get_object(id)
        selected_movie.delete()
        return Response(status=HTTP_204_NO_CONTENT)
    
    def put(self, request, id):
        selected_movie = self.get_object(id)
        movie_serializer = MovieSerializer(selected_movie, request.data)
        if movie_serializer.is_valid():
            movie_serializer.save()
            return Response(movie_serializer.data)
        return Response(movie_serializer.errors, status=HTTP_400_BAD_REQUEST)

class PersonView(APIView):
    def get_object(self, pk):
        try:
            return Person.objects.get(pk=pk)
        except Person.DoesNotExist:
            raise Http404
    def get(self, request, id):
        selected_person = self.get_object(id)
        person_serializer = PersonSerializer(selected_person,
                                             context={"request": request})
        return Response(person_serializer.data)
    def delete(self, request, id):
        selected_person = self.get_object(id)
        selected_person.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    def put(self, request, id):
        selected_person = self.get_object(id)
        person_serializer = PersonSerializer(selected_person, request.data)
        if person_serializer.is_valid():
            person_serializer.save()
            return Response(person_serializer.data)
        return Response(person_serializer.errors, status=HTTP_400_BAD_REQUEST)

class PersonsView(APIView):
    def get(self, request):
        all_movie = Person.objects.all()
        serialize_movie = PersonSerializer(all_movie, 
                                          context={"request": request}, 
                                          many=True)
        return Response(serialize_movie.data)
    
    def post(self, request):
        serialize_move = PersonSerializer(data=request.data)
        if serialize_move.is_valid():
            serialize_move.save()
            return Response(serialize_move.data)
        return Response(serialize_move.errors, status=HTTP_400_BAD_REQUEST)

class AssignDirectorMovie(APIView):
    def get_movie(self, pk):
        try:
            return Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            raise Http404
    def get_person(self, pk):
        try:
            return Person.objects.get(pk=pk)
        except Person.DoesNotExist:
            raise Http404
    def put(self, request, movie_id, person_id):
        movie = self.get_movie(movie_id)
        person = self.get_person(person_id)
        movie.director = person
        movie.save()
        movie_serializer = MovieSerializer(movie, context={"request": request})
        return Response(movie_serializer.data)
