from rest_framework.pagination import PageNumberPagination


class AdminUserProfilePagination(PageNumberPagination):
    page_size = 20


class CommonPagination(PageNumberPagination):
    page_size = 20


class AdminPagePagination(PageNumberPagination):
    page_size = 30
