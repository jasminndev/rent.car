from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from apps.filter import CarFilter
from apps.models import Car, Category, Review, CarImages, RentalOrder
from apps.serializers import CarModelSerializer, CategoryModelSerializer, ReviewModelSerializer, \
    ReviewUpdateModelSerializer, CarImagesModelSerializer, BillingInfoModelSerializer, RentalInfoModelSerializer, \
    PaymentModelSerializer, RentalOrderSerializer


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


@extend_schema(tags=['billing-info'])
class BillingInfoCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BillingInfoModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@extend_schema(tags=['rental-info'])
class RentalInfoCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = RentalInfoModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@extend_schema(tags=['payment'])
class PaymentInfoCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PaymentModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class RentalOrderListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = RentalOrder.objects.filter(user=request.user)
        serializer = RentalOrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RentalOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
