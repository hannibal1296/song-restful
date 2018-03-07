from django.contrib import admin
from .models import Song, Album, Artist, SongOwnership


@admin.register(Artist)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('kname', 'ename', 'belonged_group', 'type', 'debut_year',)
    search_fields = ('kname',)


@admin.register(Album)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'type', 'release_date')
    search_fields = ('title', 'artist__kname',)


@admin.register(Song)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_artists', 'album', 'url')
    search_fields = ('title', 'artists__kname',)


@admin.register(SongOwnership)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('song', 'artist', 'get_album', 'get_playtime', 'get_url',)
    search_fields = ('song__title', 'artist__kname', 'artist__ename', )
    list_display_links = ('song', 'artist')