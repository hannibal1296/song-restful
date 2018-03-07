from rest_framework.pagination import PageNumberPagination


# 페이지 사이즈 커스터마이제이션
class PageNumberFivePagination(PageNumberPagination):
    page_size = 5
