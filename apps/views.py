from itertools import chain

from django.db.models.aggregates import Count
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from apps.filter import CarFilter
from apps.models import Car, Category, Review, CarImages, RentalOrder, Region, District
from apps.serializers import CarModelSerializer, CategoryModelSerializer, ReviewModelSerializer, \
    ReviewUpdateModelSerializer, CarImagesModelSerializer, RentalOrderSerializer, RegionModelSerializer, \
    DistrictModelSerializer, RecentTransactionSerializer
from .models import RentalInfo, RentByBot


########################################## CATEGORY ##############################################
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


########################################## CAR ##############################################
@extend_schema(tags=['car'])
class CarCreateAPIView(CreateAPIView):
    serializer_class = CarModelSerializer
    queryset = Car.objects.all()
    permission_classes = [IsAdminUser]


@extend_schema(tags=['car'])
class CarListAPIView(ListAPIView):
    queryset = Car.objects.all()
    serializer_class = CarModelSerializer
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
    lookup_field = 'pk'


@extend_schema(tags=['car'])
class CarUpdateAPIView(UpdateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarModelSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'pk'


########################################## STATISTICS ##############################################
@extend_schema(tags=['top-5-cars'])
class Top5CarsListAPIView(APIView):
    def get(self, request):
        web_orders = (
            RentalInfo.objects
            .values('car__id', 'car__name', 'car__category__name')
            .annotate(rental_count=Count('id'))
        )

        bot_orders = (
            RentByBot.objects
            .values('car__id', 'car__name', 'car__category__name')
            .annotate(rental_count=Count('id'))
        )

        combined = {}
        for order in list(web_orders) + list(bot_orders):
            key = order['car__id']
            if key not in combined:
                combined[key] = {
                    'car__id': order['car__id'],
                    'car__name': order['car__name'],
                    'car__category__name': order['car__category__name'],
                    'rental_count': 0
                }
            combined[key]['rental_count'] += order['rental_count']

        top_cars = sorted(combined.values(), key=lambda x: x['rental_count'], reverse=True)[:5]

        return Response(top_cars)


@extend_schema(tags=['recent-transactions'])
class RecentTransactionsAPIView(APIView):
    def get(self, request):
        web_transactions = RentalInfo.objects.all()
        bot_transactions = RentByBot.objects.all()

        combined = sorted(
            chain(web_transactions, bot_transactions),
            key=lambda x: (x.pickup_date, x.pickup_time),
            reverse=True
        )

        recent = combined[:5]

        serializer = RecentTransactionSerializer(recent, many=True)
        return Response(serializer.data)


########################################## REVIEW ##############################################
@extend_schema(tags=['review'])
class ReviewCreateAPIView(CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewModelSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema(tags=['review'])
class ReviewUpdateAPIView(UpdateAPIView):
    serializer_class = ReviewUpdateModelSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)


@extend_schema(tags=['review'])
class ReviewListAPIView(ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewModelSerializer

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user).select_related('car').order_by('-created_at')


@extend_schema(tags=['review'])
class ReviewDeleteAPIView(DestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewModelSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'pk'


########################################## CAR-IMAGES ##############################################
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


########################################## RENT ##############################################
@extend_schema(tags=['rental-order'])
class RentalOrderListCreateView(APIView):
    serializer_class = RentalOrderSerializer

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
