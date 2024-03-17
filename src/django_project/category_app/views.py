from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status


class CategoryViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        return Response(
            status=status.HTTP_200_OK,
            data=[{"id": 1, "name": "Category 1"}, {"id": 2, "name": "Category 2"}],
        )
