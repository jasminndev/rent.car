from django.urls import path

from apps.views import CarCreateAPIView, CategoryDeleteAPIView, CategoryCreateAPIView, CategoryListAPIView, \
    CategoryUpdateAPIView, CarDeleteAPIView, CarListAPIView, CarDetailAPIView, CarUpdateAPIView, \
    ReviewCreateAPIView, ReviewUpdateAPIView, ReviewDeleteAPIView, ReviewListAPIView, CarImagesCreateAPIView, \
    CarImagesUpdateAPIView, CarImagesDeleteAPIView, RentalOrderListCreateView

urlpatterns = [
    path('category-create', CategoryCreateAPIView.as_view()),
    path('category-delete/<int:pk>', CategoryDeleteAPIView.as_view()),
    path('category-update/<int:pk>', CategoryUpdateAPIView.as_view()),
    path('categories', CategoryListAPIView.as_view()),
    path('car-create', CarCreateAPIView.as_view()),
    path('car-delete/<int:pk>', CarDeleteAPIView.as_view()),
    path('car-detail/<int:pk>', CarDetailAPIView.as_view()),
    path('car-update/<int:pk>', CarUpdateAPIView.as_view()),
    path('cars', CarListAPIView.as_view()),
    path('review-create', ReviewCreateAPIView.as_view()),
    path('reviews', ReviewListAPIView.as_view()),
    path('review-update/<int:pk>', ReviewUpdateAPIView.as_view()),
    path('review-delete/<int:pk>', ReviewDeleteAPIView.as_view()),
    path('car-images-create', CarImagesCreateAPIView.as_view()),
    path('car-images-update/<int:pk>', CarImagesUpdateAPIView.as_view()),
    path('car-images-delete/<int:pk>', CarImagesDeleteAPIView.as_view()),
    path('rental-orders', RentalOrderListCreateView.as_view()),


]
