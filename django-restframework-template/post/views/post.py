from rest_framework import status, viewsets, generics, mixins
from rest_framework.response import Response

from core.exceptions.base import NotFound
from post.serializers.post import CreatePostSerializer, PostDisplaySerializer
from post.services.post import PostService


class PostViewSet(viewsets.ViewSet,
                  mixins.RetrieveModelMixin,
                  mixins.ListModelMixin):

    def create(self, request):
        serializer = CreatePostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        post = PostService.create(
            title=validated_data['title'],
            content=validated_data['content'],
            author=request.my_user
        )

        return Response(
            data=PostDisplaySerializer(instance=post).data,
            status=status.HTTP_201_CREATED
        )

    def retrieve(self, request, *args, **kwargs):
        post = PostService.filter(
            pk=kwargs['pk'],
            author_id=request.my_user.id
        ).first()

        if post is None:
            raise NotFound

        return Response(
            data=PostDisplaySerializer(instance=post).data,
            status=status.HTTP_200_OK
        )

    def list(self, request, *args, **kwargs):
        qs = PostService.filter(author_id=request.my_user.id)
        return Response(
            data={'results':PostDisplaySerializer(instance=qs, many=True).data},
            status=status.HTTP_200_OK
        )

    def update(self, request, pk=None):
        return Response(
            data={'action': 'update'},
            status=status.HTTP_200_OK
        )
