from rest_framework import generics, status, serializers
from django_filters import rest_framework as filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter, inline_serializer
from django.db.models import Count
from ..serializers import MealEntrySerializer
from ..models import MealEntry
# from rest_framework.permissions import IsAdminUser

class MealEntryFilter(filters.FilterSet):
    class Meta:
        model = MealEntry
        fields = ['student_id']

class MealEntryView(generics.ListCreateAPIView):
    queryset = MealEntry.objects.all()
    serializer_class = MealEntrySerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MealEntryFilter

    def list(self, request, *args, **kwargs):
        student_id = request.query_params.get('student_id')
        if not student_id:
            return Response([])
        return super().list(request, *args, **kwargs)
    

class MealEntryCountView(APIView):

    @extend_schema(
        summary="Get Meal Entry Counts",
        description=(
            "This API endpoint provides a count of meal entries (Breakfast, Lunch, Dinner, and Overall) "
            "for a specific student based on their `student_id`."
        ),
        parameters=[
            OpenApiParameter(
                name='student_id',
                description='Filter meal entry counts by student ID',
                required=True,
                type=str
            ),
        ],
        responses={
            status.HTTP_200_OK: inline_serializer(
                name='MealEntryCountResponse',
                fields={
                    'Breakfast': serializers.IntegerField(),
                    'Lunch': serializers.IntegerField(),
                    'Dinner': serializers.IntegerField(),
                    'Overall': serializers.IntegerField(),
                }
            ),
            status.HTTP_400_BAD_REQUEST: inline_serializer(
                name='MealEntryCountErrorResponse',
                fields={
                    'error': serializers.CharField()
                }
            )
        }
    )

    def get(self, request):
        student_id = request.query_params.get('student_id')
        
        if not student_id:
            return Response(
                {"error": "student_id is required to get the data"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = MealEntry.objects.filter(student_id=student_id)
        counts = queryset.values('meal_type').annotate(count=Count('id'))
        response_data = {
            'Breakfast': 0,
            'Lunch': 0,
            'Dinner': 0,
            'Overall': 0
        }

        for item in counts:
            meal_type = item['meal_type']
            count = item['count']
            response_data[meal_type] = count
            response_data['Overall'] += count
        
        return Response(response_data, status=status.HTTP_200_OK)