from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from authentication.models import User
from authentication.serializers import UserModelSerializer


@extend_schema(tags=['auth'])
class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserModelSerializer
