from rest_framework import serializers

from social_media.models import Tag, Post


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ("id", "name")


class PostImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ("id", "image")


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ("id", "title", "author", "text", "tags", "image")
        read_only_fields = ("id", "author")


class PostListSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )

    class Meta:
        model = Post
        fields = ("id", "author", "title", "tags", "image")
        # read_only_fields = ()


class PostDetailSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=False)
    image = PostImageSerializer(many=False, read_only=False)

    class Meta:
        model = Post
        fields = ("id", "title", "author", "text", "image", "tags")
        read_only_fields = ("id", "author")
