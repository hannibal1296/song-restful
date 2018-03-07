from .models import Song, Artist, Album, SongOwnership
from .serializers import SongSerializer, AlbumSerializer, ArtistSerializer, SongOwnershipSerializer
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.decorators import list_route
from .pagination import PageNumberFivePagination
from .throttles import *


class ArtistViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    # ADDED
    """
    DjangoFilterBackend
    
    장고 필터 라이브러리는 자유도 높은 필드 필터링이 가능한 DjangoFilterBackend class를 포함한다.
    먼저 "pip install django-filter"를 통해 설치 후 사용이 가능한데 전체 셋팅에 설정해도 되고
    개별 뷰 또는 뷰셋에 설정도 가능하다.
    
    "SearchFilter" 는 간단한 단순 쿼리를 통해 검색을 가능하게 한다.
    "search_fields" 가 존재해야지만 SearchFilter 는 작동을 한다.
    외래키 또는 다수대다수필드 역시 검색이 가능하다.
    """
    filter_backends = [SearchFilter]  # 어떤 기능을 추가하는가
    search_fields = ['kname', ]  # 어떤 필드의 검색을 지원할 것인가

    # throttle_classes = [ArtistRateThrottle]
    throttle_scope = 'artist'


# def get_queryset(self):
#     queryset = super().get_queryset()
#     queryset = queryset.filter(description__icontains="BTS")
#     return queryset

# @list_route
# def no_desc(self, request):
#     qs = self.queryset.objects.all()
#     serializer = self.

class AlbumViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

    # throttle_classes = [AlbumRateThrottle]
    throttle_scope = 'album'
    filter_backends = [SearchFilter]
    search_fields = ['title', 'artist', ]


class SongViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    filter_backends = [SearchFilter]  # 어떤 기능을 추가하는가
    search_fields = ['title', 'artist__name']  # 어떤 필드의 검색을 지원할 것인가
    # 외래키모델__외래필드 의 포맷으로 검색 가능.

    pagination_class = PageNumberFivePagination
    # 한 페이지에 보여질 개수 지정하는 코드

    # throttle_classes = [SongRateThrottle]
    # SongView API's Throttling limit
    throttle_scope = 'song'

class SongOwnershipViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SongOwnership.objects.all()
    serializer_class = SongOwnershipSerializer
    filter_backends = [SearchFilter]
    search_fields = ['artist', 'song', ]
