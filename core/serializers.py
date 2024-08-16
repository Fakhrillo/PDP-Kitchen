from rest_framework import serializers
from .models import *

class StudentSerializer(serializers.Serializer):
    class Meta:
        model = Student
        fields = '__all__'

class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = '__all__'

class MenuSerializer(serializers.ModelSerializer):
    meals = serializers.StringRelatedField(many=True)
    class Meta:
        model = Menu
        fields = ['id', 'week_days', 'meal_time', 'created_at', 'meals']

class MealEntrySerializer(serializers.ModelSerializer):
    student_id = serializers.SlugRelatedField(
        queryset=Student.objects.all(),
        slug_field='student_id'
    )
    class Meta:
        model = MealEntry
        fields = ['student_id', 'date', 'meal_type', 'created_at']