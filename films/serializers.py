from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Film, Director, Genre
class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = 'id fio age'.split()


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class FilmDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = '__all__'


class FilmSerializer(serializers.ModelSerializer):
    director = DirectorSerializer(many=False)
    genres = GenreSerializer(many=True)
    director_fio = serializers.SerializerMethodField()

    class Meta:
        model = Film
        fields = 'id reviews name kp_rating created director genres director_fio genre_names'.split()
        depth = 1

    def get_director_fio(self, film):
        return film.director.fio if film.director_id else None

class FilmValidateSerializer(serializers.Serializer):
    name = serializers.CharField(required=True,min_length=2, max_length=100)
    text = serializers.CharField(required=False,default='no text')
    kp_rating = serializers.FloatField(min_value=0, max_value=10)
    is_active = serializers.BooleanField(default=False)
    director_id = serializers.IntegerField(min_value=1)
    genres = serializers.ListField(child=serializers.IntegerField(min_value=1))

    def validate_director_id(self, director_id):
        try:
            Director.objects.get(id=director_id)
        except:
            raise ValidationError({'director_id': 'Director with this id does not exist.'})
        return director_id

    def validate_genres(self, genres):
        return genres
