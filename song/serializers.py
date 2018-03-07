from rest_framework.serializers import ModelSerializer, StringRelatedField
from .models import Song, Album, Artist, SongOwnership
from rest_framework import serializers


class ArtistSerializer(ModelSerializer):
    class Meta:
        model = Artist
        fields = "__all__"
        # fields 에 등장한 특성만 등장함.
        depth = 2


class AlbumSerializer(ModelSerializer):
    # artist_name = serializers.ReadOnlyField(source='artist.artist')

    class Meta:
        model = Album
        fields = "__all__"
        depth = 2


class SongSerializer(ModelSerializer):
    class Meta:
        model = Song
        fields = "__all__"
        # depth = 2

class SongOwnershipSerializer(ModelSerializer):
    class Meta:
        model = SongOwnership
        fields = "__all__"
        depth = 2