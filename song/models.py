from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from django.conf import settings
from pdb import set_trace


# Whenever a new user is created, a token is also created.
# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)


album_choice = (
    ('Studio', 'Studio'),
    ('Mini', 'Mini'),
    ('EP', 'EP'),
    ('Single', 'Single'),
    ('Mixtape', 'Mixtape'),
    ('Compilation', 'Compilation'),
    ('OST', 'OST'),
    ('Unknown', 'Unknown'),
)

genre_choice = (
    ('Acoustic', 'Acoustic'),
    ('Alternative', 'Alternative'),
    ('Balad', 'Balad'),
    ('Classic', 'Classic'),
    ('Dance', 'Dance'),
    ('Electronic', 'Electronic'),
    ('Hiphop', 'Hiphop'),
    ('Holiday', 'Holiday'),
    ('Indi', 'Indi'),
    ('Jazz', 'Jazz'),
    ('New Age', 'New Age'),
    ('OST', 'OST'),
    ('Rock', 'Rock'),
    ('R&B', 'R&B'),
)

artist_type = (
    ('그룹 (남성)', '그룹 (남성)'),
    ('그룹 (여성)', '그룹 (여성)'),
    ('솔로 (남성)', '솔로 (남성)'),
    ('솔로 (여성)', '솔로 (여성)'),
    ('듀오 (남성)', '듀오 (남성)'),
    ('듀오 (여성)', '듀오 (여성)'),
    ('그룹 (혼성)', '그룹 (혼성)'),
)


# 99141379daf9bcb925c759813531aac92f9cb7ec

class Artist(models.Model):
    kname = models.CharField(max_length=30, verbose_name="Korean Name")
    ename = models.CharField(max_length=30, verbose_name="English Name", blank=True, null=True)
    debut_year = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=20, blank=True, null=True)
    is_group = models.BooleanField(default=False)
    belonged_group = models.ForeignKey('Artist', blank=True, null=True, on_delete=models.SET_NULL)
    nationality = models.CharField(max_length=20, blank=True, null=True, default="South Korea")

    class Meta:
        ordering = ['kname', 'ename', 'type', 'debut_year', ]

    def __str__(self):
        return self.kname


class Album(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, verbose_name="Album")
    type = models.CharField(max_length=20)
    release_date = models.DateField()
    description = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = (('artist', 'title', 'release_date'),)

    def __str__(self):
        return self.title


# class Group(models.Model):
#     kname = models.CharField(max_length=30, verbose_name="Korean Name")
#     ename = models.CharField(max_length=30, verbose_name="English Name", blank=True, null=True)
#     members = models.ManyToManyField(Artist, through='MemberShip', through_fields=('artist', 'group'),)
#
#     class Meta:
#         ordering = ['kname', 'ename',' members',]
#
#     def __str__(self):
#         return self.kname
#
# # Artist : Group = 1 : N
# class MemberShip(models.Model):
#     artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
#     group = models.ForeignKey(Group, on_delete=models.CASCADE)
#     type = models.CharField(max_length=12, blank=True, null=True)
#     debut_year = models.IntegerField(blank=True, null=True)
#
#     def __str__(self):
#         return self.artist.kname

# SONG : Album = N : 1


class Song(models.Model):
    artists = models.ManyToManyField(Artist, through='SongOwnership', through_fields=('song', 'artist'))
    title = models.CharField(max_length=50, verbose_name="Title")
    album = models.ForeignKey('Album', on_delete=models.CASCADE)
    track_num = models.IntegerField(default=1)
    disk_num = models.IntegerField(default=1)
    playtime = models.CharField(max_length=7, blank=True, null=True)
    lyrics = models.TextField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)

    def get_artists(self):
        return " & ".join([str(each) for each in self.artists.all()])

    def __str__(self):
        return str(self.title)

    class Meta:
        ordering = ['title', 'album', ]
        unique_together = (('title', 'album'),)


class SongOwnership(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)

    def get_album(self):
        return str(self.song.album)
    def get_playtime(self):
        return self.song.playtime
    def get_url(self):
        return self.song.url

    def __str__(self):
        return str(self.artist) + " - " + str(self.song)
