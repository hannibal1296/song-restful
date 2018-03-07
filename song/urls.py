from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from django.conf import settings
from rest_framework.authtoken import views as drf_views
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'song', views.SongViewSet)
router.register(r'artist', views.ArtistViewSet)
router.register(r'album', views.AlbumViewSet)
router.register(r'songownership', views.SongOwnershipViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('get-auth-token/', drf_views.obtain_auth_token, name='get_auth_token'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)