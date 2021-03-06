from rest_framework.pagination import LimitOffsetPagination

class APIPagination(LimitOffsetPagination):
    default_limit = 20
    max_limit = 100