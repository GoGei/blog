from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import UserSerializer, UserCreateUpdateSerializer, PasswordSerializer
from core.User.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-email')
    serializer_class = UserSerializer
    serializer_map = {
        'create': UserCreateUpdateSerializer,
        'update': UserCreateUpdateSerializer,
        'set_password': PasswordSerializer,
    }

    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['email']
    filterset_fields = ['is_active', 'is_staff', 'is_superuser']
    ordering_fields = ['email']

    def get_serializer_class(self):
        serializer = self.serializer_map.get(self.action, self.serializer_class)
        return serializer

    @action(detail=True, methods=['post'])
    def set_password(self, request, pk=None):
        user = self.get_object()
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
