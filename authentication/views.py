from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from authentication.models import User, Wishlist
from authentication.serializers import UserModelSerializer, UserUpdateSerializer, ChangePasswordSerializer, \
    WishlistModelSerializer


###################################### AUTH ######################################
@extend_schema(tags=['auth'])
class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    permission_classes = [AllowAny]


@extend_schema(tags=['auth'])
class UserUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    lookup_field = 'pk'


@extend_schema(tags=['auth'])
class UserDeleteAPIView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer


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
