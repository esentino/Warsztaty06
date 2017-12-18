from django.db import models

# Create your models here.

class Person(models.Model):
    name = models.CharField(max_length=200)


class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    #Reżyser może być nieustawiony a w przypadku usunięcia Reżysera zostaje usunięty powiązanie z filmem
    director = models.ForeignKey(Person, related_name="movie_director", on_delete=models.SET_NULL, null=True)
    actors = models.ManyToManyField(Person, through='MoviePerson', related_name="aktorzy")
    year = models.IntegerField()


class MoviePerson(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    role = models.CharField(max_length=200)