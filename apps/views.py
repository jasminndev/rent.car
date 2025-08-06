from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from apps.models import Car, Category, Wishlist
from apps.serializers import CarModelSerializer, CategoryModelSerializer, WishlistModelSerializer


@extend_schema(tags=['category'])
class CategoryCreateAPIView(CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    permission_classes = [IsAdminUser]


@extend_schema(tags=['category'])
class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer


@extend_schema(tags=['category'])
class CategoryDeleteAPIView(DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'pk'


@extend_schema(tags=['category'])
class CategoryUpdateAPIView(UpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'pk'


@extend_schema(tags=['category'])
class CategoryDetailAPIView(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'pk'


@extend_schema(tags=['car'])
class CarCreateAPIView(CreateAPIView):
    serializer_class = CarModelSerializer
    queryset = Car.objects.all()
    permission_classes = [IsAdminUser]


@extend_schema(tags=['car'])
class CarListAPIView(ListAPIView):
    queryset = Car.objects.all()
    serializer_class = CarModelSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


@extend_schema(tags=['car'])
class CarDeleteAPIView(DestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarModelSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'pk'


@extend_schema(tags=['car'])
class CarDetailAPIView(RetrieveAPIView):
    queryset = Car.objects.all()
    serializer_class = CarModelSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    lookup_field = 'pk'


@extend_schema(tags=['car'])
class CarUpdateAPIView(UpdateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarModelSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'pk'
