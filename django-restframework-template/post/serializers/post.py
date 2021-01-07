from rest_framework import serializers

from core.utils.datetime import to_iso8601_utc_string


class CreatePostSerializer(serializers.Serializer):
    title = serializers.CharField()
    content = serializers.CharField()


class UpdatePostSerializer(serializers.Serializer):
    title = serializers.CharField()
    content = serializers.CharField()


class PostDisplaySerializer(serializers.Serializer):

    def to_representation(self, post):
        return {
            'post_id': post.id,
            'title': post.title,
            'content': post.content,
            'author_id': post.author.id,
            'created': to_iso8601_utc_string(post.created)
        }
