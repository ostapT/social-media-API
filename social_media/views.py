from django.shortcuts import render
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from social_media.models import Tag, Post
from social_media.permissions import IsAdminOrIfAuthenticatedReadOnly
from social_media.serializers import TagSerializer, PostSerializer, PostListSerializer, PostDetailSerializer, \
    PostImageSerializer


class TagViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    # permission_classes = (IsAuthenticated,)


class PostPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100


class PostViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Post.objects.prefetch_related("tag")
    serializer_class = PostSerializer
    pagination_class = PostPagination
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


    @staticmethod
    def _params_to_ints(qs):
        """Converts a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        title = self.request.query_params.get("title")
        tags = self.request.query_params.get("tags")

        queryset = self.queryset.filter(author=self.request.user)

        if title:
            queryset = queryset.filter(title__icontains=title)

        if tags:
            tags_ids = self._params_to_ints(tags)
            queryset = queryset.fiter(tags__id__in=tags_ids)

        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer

        if self.action == "retrieve":
            return PostDetailSerializer

        if self.action == "upload_image":
            return PostImageSerializer

        return self.serializer_class

    @action(
        methods=["POST"],
        detail=True,
        url_path="upload-image",
        permission_classes=[IsAuthenticated],
    )
    def upload_image(self, request, pk=None):

        movie = self.get_object()
        serializer = self.get_serializer(movie, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
