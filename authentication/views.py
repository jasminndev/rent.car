import json
import random
from http import HTTPStatus

from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView, \
    GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from authentication.models import User, Wishlist
from authentication.serializers import UserModelSerializer, UserUpdateSerializer, ChangePasswordSerializer, \
    WishlistModelSerializer, VerifyCodeSerializer
from authentication.tasks import send_code_email
from root.settings import redis


###################################### AUTH ######################################
@extend_schema(tags=['auth'])
class UserGenericAPIView(GenericAPIView):
    serializer_class = UserModelSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        code = str(random.randrange(10 ** 5, 10 ** 6))
        send_code_email.delay(user, code)
        redis.set(code, json.dumps(user))
        return Response({'message': "Tasdiqlash kodi jo'natildi"}, status=HTTPStatus.OK)


@extend_schema(tags=['auth'])
class VerifyCodeGenericAPIView(GenericAPIView):
    serializer_class = VerifyCodeSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.context.get("user_data")

        referral_code = user_data.pop("referral_code", None)

        user = User.objects.create(**user_data)

        if referral_code:
            try:
                referrer = User.objects.get(referral_code=referral_code)
                user.referred_by = referrer
                user.save(update_fields=["referred_by"])
            except User.DoesNotExist:
                pass

        return Response(UserModelSerializer(user).data, status=HTTPStatus.CREATED)


@extend_schema(tags=['auth'])
class CustomTokenObtainPairView(TokenObtainPairView):

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == HTTPStatus.OK:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.user
            user.last_login = timezone.now()
            user.save(update_fields=['last_login'])
        return response


@extend_schema(tags=['auth'])
class CustomTokenRefreshView(TokenRefreshView):
    pass


###################################### USER ######################################
@extend_schema(tags=['user'])
class UserUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    lookup_field = 'pk'


@extend_schema(tags=['user'])
class UserDeleteAPIView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    permission_classes = [IsAdminUser]


@extend_schema(tags=['user'])
class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [SearchFilter]
    search_fields = ['first_name', 'last_name', 'email']


###################################### PASSWORD ######################################
@extend_schema(tags=['passwd'])
class ChangePasswordAPIView(UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer


###################################### WISHLIST ######################################
@extend_schema(tags=['wishlist'])
class WishlistCreateAPIView(CreateAPIView):
    serializer_class = WishlistModelSerializer
    queryset = Wishlist.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema(tags=['wishlist'])
class WishlistListAPIView(ListAPIView):
    serializer_class = WishlistModelSerializer

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user).select_related('car').order_by('-created_at')


@extend_schema(tags=['wishlist'])
class WishlistDeleteAPIView(DestroyAPIView):
    serializer_class = WishlistModelSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)


@extend_schema(tags=['wishlist'])
class WishlistRetrieveAPIView(RetrieveAPIView):
    serializer_class = WishlistModelSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)
