from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from authentication.models import User
from authentication.serializers import UserModelSerializer, UserUpdateSerializer, ChangePasswordSerializer


@extend_schema(tags=['auth'])
class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer


@extend_schema(tags=['auth'])
class UserUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserUpdateSerializer
    lookup_field = 'pk'


@extend_schema(tags=['auth'])
class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserModelSerializer


@extend_schema(tags=['auth'])
class UserRetrieveAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserModelSerializer
    lookup_field = 'pk'


@extend_schema(tags=['passwd'])
class ChangePasswordAPIView(UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer


@extend_schema(tags=['auth'])
class UserDeleteAPIView(DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserModelSerializer
