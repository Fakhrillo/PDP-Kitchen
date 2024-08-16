from django.contrib import admin
from .models import *
from django.db import models
from image_uploader_widget.widgets import ImageUploaderWidget
from django.contrib.auth.models import Group
admin.site.unregister(Group)
# Register your models here.
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "student_id", "phone_number", "photo", "created_at")
    search_fields = ("first_name", "last_name", "student_id", "phone_number")
    list_filter = ("created_at",)
    list_display_links = ("id", "first_name")

    formfield_overrides = {
        models.ImageField: {'widget': ImageUploaderWidget},
    }

@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ("id", "meal_name", "price", 'photo', "created_at")
    search_fields = ("meal_name",)
    list_filter = ("created_at", "price")
    list_display_links = ("id", "meal_name", "price")

    formfield_overrides = {
        models.ImageField: {'widget': ImageUploaderWidget},
    }

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ("id", "week_days", "meal_time", "created_at")
    list_display_links = ("id", "week_days", "meal_time",)
    search_fields = ("week_days", "meal_time", "meals")

@admin.register(MealEntry)
class MealEntryAdmin(admin.ModelAdmin):
    list_display = ("id", "student_id", "meal_type", "date", "created_at")
    list_display_links = ("id", "student_id", "meal_type")
    search_fields = ("student_id", "meal_type", "date")
    list_filter = ("date", "meal_type", "student_id")