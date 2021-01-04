from rest_framework import mixins, status, viewsets
from rest_framework.response import Response


class PostViewSet(viewsets.ViewSet):

    def list(self, request):
        return Response(
            data={'action': 'list'},
            status=status.HTTP_200_OK
        )

    def create(self, request):
        return Response(
            data={'action': 'create'},
            status=status.HTTP_201_CREATED
        )

    def retrieve(self, request, pk=None):
        return Response(
            data={'action': 'retrieve'},
            status=status.HTTP_200_OK
        )

    def update(self, request, pk=None):
        return Response(
            data={'action': 'update'},
            status=status.HTTP_200_OK
        )
