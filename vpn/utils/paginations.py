from rest_framework.pagination import PageNumberPagination


class AdminUserProfilePagination(PageNumberPagination):
    page_size = 20
