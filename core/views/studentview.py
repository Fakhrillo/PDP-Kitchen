from rest_framework import generics
from django_filters import rest_framework as filters
from ..serializers import StudentSerializer
from ..models import Student
# from rest_framework.permissions import IsAdminUser

class StudentFilter(filters.FilterSet):
    class Meta:
        model = Student
        fields = ['student_id']

class StudentView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = StudentFilter
