from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny

from apps.filter import CarFilter
from apps.models import Car, Category, Review, PickUp, DropOff
from apps.serializers import CarModelSerializer, CategoryModelSerializer, ReviewModelSerializer, PickUpModelSerializer, \
    DropOffModelSerializer, ReviewUpdateModelSerializer


@extend_schema(tags=['category'])
class CategoryCreateAPIView(CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    permission_classes = [IsAdminUser]


@extend_schema(tags=['category'])
class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    permission_classes = [AllowAny]


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


@extend_schema(tags=['car'])
class CarCreateAPIView(CreateAPIView):
    serializer_class = CarModelSerializer
    queryset = Car.objects.all()
    permission_classes = [IsAdminUser]


@extend_schema(tags=['car'])
class CarListAPIView(ListAPIView):
    queryset = Car.objects.all()
    serializer_class = CarModelSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = CarFilter




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
    permission_classes = [AllowAny]
    lookup_field = 'pk'


@extend_schema(tags=['car'])
class CarUpdateAPIView(UpdateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarModelSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'pk'


@extend_schema(tags=['review'])
class ReviewCreateAPIView(CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewModelSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema(tags=['review'])
class ReviewUpdateAPIView(UpdateAPIView):
    serializer_class = ReviewUpdateModelSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)


@extend_schema(tags=['review'])
class ReviewListAPIView(ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewModelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user).select_related('car').order_by('-created_at')


@extend_schema(tags=['review'])
class ReviewDeleteAPIView(DestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewModelSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'pk'


@extend_schema(tags=['pick-up'])
class PickUpCreateAPIView(CreateAPIView):
    queryset = PickUp.objects.all()
    serializer_class = PickUpModelSerializer
    permission_classes = [IsAuthenticated]


@extend_schema(tags=['pick-up'])
class PickUpUpdateAPIView(UpdateAPIView):
    queryset = PickUp.objects.all()
    serializer_class = PickUpModelSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'


@extend_schema(tags=['drop-off'])
class DropOffCreateAPIView(CreateAPIView):
    queryset = DropOff.objects.all()
    serializer_class = DropOffModelSerializer
    permission_classes = [IsAuthenticated]


@extend_schema(tags=['drop-off'])
class DropOffUpdateAPIView(UpdateAPIView):
    queryset = DropOff.objects.all()
    serializer_class = DropOffModelSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'
