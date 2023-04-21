from rest_framework import serializers

from social_media.models import Tag, Post


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ("id", "name")


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ("id", "title", "author", "text", "tags")


class PostListSerializer(PostSerializer):
    tags = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )

    class Meta:
        model = Post
        fields = ("id", "title", "author", "tags")


class PostDetailSerializer(PostSerializer):
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ("id", "title", "author", "text", "image", "tags")


class PostImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ("id", "image")
