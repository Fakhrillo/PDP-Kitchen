from rest_framework import generics
from django_filters import rest_framework as filters
from ..serializers import MenuSerializer
from ..models import Menu
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from rest_framework import status
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

class StudentMenuView(generics.ListAPIView):
    serializer_class = MenuSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MenuFilter

    @extend_schema(
        summary="List available meals for the day",
        description=(
            "This endpoint returns a list of available meals for the day based on the user's meal entries. "
            "It filters out the meals the user has already consumed today. "
            "If the user has had all the meals for the day, it returns an empty list."
        ),
        parameters=[
            OpenApiParameter(
                name='user_id',
                description="The ID of the user to filter the menu by their meal entries for the day.",
                required=True,
                type=str,
                location=OpenApiParameter.QUERY,
            ),
        ],
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=MenuSerializer(many=True),
                description="List of available meals for the day."
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="User ID is missing or invalid."
            ),
        },
    )


    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        if not user_id:
            raise ValidationError("User ID is required")

        today = timezone.now().date()
        existing_meal_entries = MealEntry.objects.filter(
            student_id__student_id=user_id,
            date=today
        ).values_list('meal_type', flat=True)

        queryset = Menu.objects.exclude(meal_time__in=existing_meal_entries)
        return queryset
