from rest_framework import generics
from django_filters import rest_framework as filters
from ..serializers import MenuSerializer
from ..models import Menu
# from rest_framework.permissions import IsAdminUser

class MenuFilter(filters.FilterSet):
    class Meta:
        model = Menu
        fields = ['week_days']

class MenuView(generics.ListCreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MenuFilter
