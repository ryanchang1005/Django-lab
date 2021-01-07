from rest_framework import status, viewsets, generics, mixins
from rest_framework.response import Response

from rest_framework.viewsets import mixins
from rest_framework.viewsets import GenericViewSet

from core.exceptions.base import NotFound
from post.serializers.post import CreatePostSerializer, PostDisplaySerializer, UpdatePostSerializer
from post.services.post import PostService


class PostViewSet(GenericViewSet,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin):
    lookup_filed = 'pk'

    def create(self, request, *args, **kwargs):
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
            data={'results': PostDisplaySerializer(instance=qs, many=True).data},
            status=status.HTTP_200_OK
        )

    def update(self, request, *args, **kwargs):
        serializer = UpdatePostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        post = PostService.update(
            pk=kwargs['pk'],
            title=validated_data['title'],
            content=validated_data['content'],
            author=request.my_user
        )

        return Response(
            data=PostDisplaySerializer(instance=post).data,
            status=status.HTTP_200_OK
        )
