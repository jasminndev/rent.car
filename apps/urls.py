from django.urls import path

from apps.views import CarCreateAPIView, CategoryDeleteAPIView, CategoryCreateAPIView, CategoryListAPIView, \
    CategoryUpdateAPIView, CategoryDetailAPIView, CarDeleteAPIView, CarListAPIView, CarDetailAPIView, CarUpdateAPIView

urlpatterns = [
    path('category-create', CategoryCreateAPIView.as_view()),
    path('category-delete/<int:pk>', CategoryDeleteAPIView.as_view()),
    path('category-update/<int:pk>', CategoryUpdateAPIView.as_view()),
    path('category-detail/<int:pk>', CategoryDetailAPIView.as_view()),
    path('categories', CategoryListAPIView.as_view()),
    path('car-create', CarCreateAPIView.as_view()),
    path('car-delete/<int:pk>', CarDeleteAPIView.as_view()),
    path('car-detail/<int:pk>', CarDetailAPIView.as_view()),
    path('car-update/<int:pk>', CarUpdateAPIView.as_view()),
    path('cars', CarListAPIView.as_view()),

]
