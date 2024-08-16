from rest_framework import generics
from ..serializers import StudentSerializer
from ..models import Student
# from rest_framework.permissions import IsAdminUser


class StudentView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
