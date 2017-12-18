from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
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
            serialize_move.save()
            return Response(serialize_move.data)
        return Response(serialize_move.errors, status=HTTP_400_BAD_REQUEST)
