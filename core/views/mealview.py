from rest_framework import generics
from ..serializers import MealSerializer
from ..models import Meal
# from rest_framework.permissions import IsAdminUser


class MealView(generics.ListCreateAPIView):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
