from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('song.urls')),
    path('account/', include('account.urls')),

    path('update-db/', include('song_scraper.urls')),

    path('api-token-auth/', obtain_auth_token),

    # path('auth/', include('rest_framework_social_oauth2.urls')),
]
