"""View modules"""
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT
from .models import Movie, Person
from .serializers import MovieSerializer, PersonSerializer
from django.shortcuts import render


class MoviesView(APIView):
    """Movies View"""
    def get(self, request, format=None):
        """Zwraca listę filmów"""

        #Pobieramy wszystkie filmy z naszej bazy danych
        all_movie = Movie.objects.all()
        # Serializujemy nasze filmy. Domyślnie ModelSerializer za pierwszy
        # parametr przyjmuję objekt klasy. Ustawienie many na True powoduje,
        # że jest on wstanie zserializować QuerySet do jsona
        serialize_movie = MovieSerializer(all_movie,
                                          context={"request": request},
                                          many=True)
        #Zwracamy przy użyciu obiektu klasy Response jsonową odpowiedź.
        return Response(serialize_movie.data)


    def post(self, request):
        """Dodaje nowy film do bazy danych"""

        # Serializujemy dane otrzymaje w poście do MovieSerializer-a
        serialize_move = MovieSerializer(data=request.data)
        # Sprawdzamy dane są poprawne
        if serialize_move.is_valid():
            #Zapisujemy nowy obiekt do bazy danych
            serialize_move.save()
            #Zwracany zapisany model
            return Response(serialize_move.data)
        # Jeśli walidacja nie przebiegnie pozytywnie zwracamy 400 z informacją
        # o błędach
        return Response(serialize_move.errors, status=HTTP_400_BAD_REQUEST)


class MovieView(APIView):
    """MovieView - klasa odpowiedzialna za wyświetlanie pojedycznego rekordu
       z bazy danych, jego usunięcie i aktualizację"""

    def get_object(self, pk):
        """Pobiera film o zadanym id lub zwraca wyjątek w przypadku braku"""
        try:
            return Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            raise Http404


    def get(self, request, id):
        """Zwracanie filmu o podanym id w przypadku braku 404"""

        # Pobieramy film
        selected_movie = self.get_object(id)
        # Serializujemy film
        movie_serializer = MovieSerializer(selected_movie,
                                           context={"request": request})
        # Wracamy odpowiedź
        return Response(movie_serializer.data)


    def delete(self, request, id):
        """Metoda odpowiedzialna za usunięcie filmu z bazy danych"""

        # Odnajdujemy film w bazie danych
        selected_movie = self.get_object(id)
        # Usuwamy go
        selected_movie.delete()
        # Wzracamy w przypadku sukcesu 204, bez treści
        return Response(status=HTTP_204_NO_CONTENT)


    def put(self, request, id):
        """Aktualizacja filmu"""

        # Pobieramy objekt filmu z bazy danych
        selected_movie = self.get_object(id)

        # Przekazujemy do serializera obiekt filmy oraz dane żądania http
        movie_serializer = MovieSerializer(selected_movie, request.data)

        # Sprawdzamy czy dane są poprawne
        if movie_serializer.is_valid():
            # Zapisujemy dane
            movie_serializer.save()
            # zwracamy zaktualizowane informacje o filmie
            return Response(movie_serializer.data)
        # Jak coś nie udało się zwalidować to zwracamy informacje o będzie-
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


def dziwnyWidok(request):
    person = Person.objects.get(pk=2)
    movie = Movie.objects.filter(director=person).first()
    return render(request, "index.html", {"movies": movie})
