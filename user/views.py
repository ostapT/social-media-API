from django.contrib.auth import get_user_model
from django.http import HttpResponse
from rest_framework import generics, viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from user.models import Profile
from user.serializers import UserSerializer, ProfileSerializer, ProfileListSerializer, ProfileDetailSerializer, \
    ProfileImageSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer) -> None:
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return ProfileListSerializer

        if self.action == "retrieve":
            return ProfileSerializer

        if self.action == "upload-image":
            return ProfileImageSerializer

        return self.serializer_class


class UserFollowersViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        my_user = get_user_model().objects.get(id=self.request.user.id)
        return my_user.profile.followers.all()


def follow_toggle(request, pk):

    another_user = get_user_model().objects.get(id=pk)
    current_user = get_user_model().objects.get(id=request.user.id)
    followers = current_user.profile.followers.all()

    if pk != current_user.id:
        if another_user in followers:
            current_user.profile.followers.remove(another_user.id)
        else:
            current_user.profile.followers.add(another_user.id)

    return HttpResponse(status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
