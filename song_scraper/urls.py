from django.contrib import admin
from django.urls import path, include
from . import views

# :8000/update-db/
urlpatterns = [
    # path('artist/', views.save_artists),
    # path('album/', views.save_albums),
    # path('song/', views.save_songs),
    path('', views.save_top100),
    path('add_ename/', views.add_ename),
    path('reset_ename/', views.reset_ename),
]