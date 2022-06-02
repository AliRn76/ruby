from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class Pagination(LimitOffsetPagination):
    default_limit   = 10
    max_limit       = 20

    def get_paginated_response(self, data):
        return Response({
            'has_next': False if self.offset + self.limit >= self.count else True,
            'result': data
        })
