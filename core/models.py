from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from enum import Enum

class MealTimeEnum(Enum):
    BREAKFAST = 'Breakfast'
    LUNCH = 'Lunch'
    DINNER = 'Dinner'

    @classmethod
    def choices(cls):
        return [(tag.value, tag.name) for tag in cls]

# Create your models here.
class Student(models.Model):
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    student_id = models.CharField(max_length=50, unique=True)
    phone_number = PhoneNumberField(blank=True, region="UZ")
    photo = models.ImageField(upload_to="students/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Meal(models.Model):
    meal_name = models.CharField(max_length=100)
    price = models.IntegerField()
    photo = models.ImageField(upload_to="meals/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.meal_name

class Menu(models.Model):
    WEEK_DAYS = [
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
    ('Sunday', 'Sunday'),
    ]

    week_days = models.CharField(max_length=50, choices=WEEK_DAYS)
    meal_time = models.CharField(max_length=50, choices=MealTimeEnum.choices())
    meals = models.ManyToManyField(Meal)  
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"{self.meal_time} on {self.week_days}"

class MealEntry(models.Model):
    student_id = models.ForeignKey(Student, to_field='student_id', on_delete=models.CASCADE)
    date = models.DateField()
    meal_type = models.CharField(max_length=50, choices=MealTimeEnum.choices())
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_id} - {self.meal_type} on {self.date}"
    