from django.urls import path
from rest_framework.generics import ListAPIView

from authentication.views import UserUpdateAPIView, ChangePasswordAPIView, \
    UserDeleteAPIView, WishlistCreateAPIView, WishlistDeleteAPIView, WishlistListAPIView, \
    WishlistRetrieveAPIView, CustomTokenObtainPairView, CustomTokenRefreshView, UserGenericAPIView, \
    VerifyCodeGenericAPIView

# auth
urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserGenericAPIView.as_view()),
]

# user
urlpatterns += [
    path('user-create', UserGenericAPIView.as_view()),
    path('user-update/<int:pk>', UserUpdateAPIView.as_view()),
    path('user-delete/<int:pk>', UserDeleteAPIView.as_view()),
    path('users', ListAPIView.as_view()),
    path('user-change-passwd/<int:pk>', ChangePasswordAPIView.as_view()),
    path('verify/code', VerifyCodeGenericAPIView.as_view()),

]

# wishlist
urlpatterns += [
    path('wishlist-create', WishlistCreateAPIView.as_view()),
    path('wishlist-delete/<int:pk>', WishlistDeleteAPIView.as_view()),
    path('wishlist-detail/<int:pk>', WishlistRetrieveAPIView.as_view()),
    path('wishlists', WishlistListAPIView.as_view()),
]
