from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT
from django.http import Http404
from .models import Movie
from .serializers import MovieSerializer, MovieAddSerializer
# Create your views here.


class MoviesView(APIView):
    def get(self, request, format=None):
        all_movie = Movie.objects.all()
        serialize_movie = MovieSerializer(all_movie, 
                                          context={"request": request}, 
                                          many=True)
        return Response(serialize_movie.data)
    
    def post(self, request, format=None):
        serialize_move = MovieAddSerializer(data=request.data)
        if serialize_move.is_valid():
            movie = serialize_move.save()
            if movie is not None:
                return Response(serialize_move.data)
            return Response(serialize_move.errors, status=HTTP_400_BAD_REQUEST)
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
