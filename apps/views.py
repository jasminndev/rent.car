from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from apps.filter import CarFilter
from apps.models import Car, Category, Review, CarImages, RentalOrder, RentalInfo, Region, District
from apps.serializers import CarModelSerializer, CategoryModelSerializer, ReviewModelSerializer, \
    ReviewUpdateModelSerializer, CarImagesModelSerializer, RentalOrderSerializer, RecentTransactionSerializer, \
    RegionModelSerializer, DistrictModelSerializer


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
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = CarFilter
    search_fields = ['name']


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


@extend_schema(tags=['top-5-cars'])
class Top5CarsListAPIView(APIView):
    def get(self, request):
        top_cars = (
            RentalInfo.objects
            .values('car__id', 'car__name', 'car__category__name')
            .annotate(rental_count=Count('id'))
            .order_by('-rental_count')[:5]
        )
        return Response(top_cars)


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


@extend_schema(tags=['car-images'])
class CarImagesCreateAPIView(CreateAPIView):
    queryset = CarImages.objects.all()
    serializer_class = CarImagesModelSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        car_id = self.request.data.get('car')
        serializer.save(car_id=car_id)


@extend_schema(tags=['car-images'])
class CarImagesUpdateAPIView(UpdateAPIView):
    queryset = CarImages.objects.all()
    serializer_class = CarImagesModelSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'pk'


@extend_schema(tags=['car-images'])
class CarImagesDeleteAPIView(DestroyAPIView):
    queryset = CarImages.objects.all()
    serializer_class = CarImagesModelSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'pk'


@extend_schema(tags=['rental-order'])
class RentalOrderListCreateView(APIView):
    serializer_class = RentalOrderSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = RentalOrder.objects.filter(user=request.user)
        serializer = RentalOrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RentalOrderSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            order = serializer.save()
            return Response(RentalOrderSerializer(order).data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@extend_schema(tags=['recent-transactions'])
class RecentTransactionsAPIView(APIView):
    def get(self, request):
        transactions = RentalInfo.objects.all().order_by("-pickup_date", "-pickup_time")[:5]
        serializer = RecentTransactionSerializer(transactions, many=True)
        return Response(serializer.data)


########################################## REGION ##############################################
@extend_schema(tags=['region'])
class RegionCreateAPIView(CreateAPIView):
    serializer_class = RegionModelSerializer
    queryset = Region.objects.all()
    permission_classes = [IsAdminUser]


@extend_schema(tags=['region'])
class RegionUpdateAPIView(UpdateAPIView):
    serializer_class = RegionModelSerializer
    queryset = Region.objects.all()
    permission_classes = [IsAdminUser]
    lookup_field = 'pk'


@extend_schema(tags=['region'])
class RegionDeleteAPIView(DestroyAPIView):
    serializer_class = RegionModelSerializer
    queryset = Region.objects.all()
    permission_classes = [IsAdminUser]
    lookup_field = 'pk'


class RegionListAPIView(ListAPIView):
    serializer_class = RegionModelSerializer
    permission_classes = [IsAuthenticated]
    queryset = Region.objects.all()


########################################## DISTRICT ##############################################
@extend_schema(tags=['district'])
class DistrictCreateAPIView(CreateAPIView):
    serializer_class = DistrictModelSerializer
    queryset = District.objects.all()
    permission_classes = [IsAdminUser]


@extend_schema(tags=['district'])
class DistrictUpdateAPIView(UpdateAPIView):
    serializer_class = DistrictModelSerializer
    queryset = District.objects.all()
    permission_classes = [IsAdminUser]
    lookup_field = 'pk'


@extend_schema(tags=['district'])
class DistrictDeleteAPIView(DestroyAPIView):
    serializer_class = DistrictModelSerializer
    queryset = District.objects.all()
    permission_classes = [IsAdminUser]
    lookup_field = 'pk'


@extend_schema(tags=['district'])
class DistrictListAPIView(ListAPIView):
    serializer_class = DistrictModelSerializer
    permission_classes = [IsAuthenticated]
    queryset = District.objects.all()
