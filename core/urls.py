from django.urls import path
from .views.studentview import StudentView
from .views.mealview import MealView
from .views.menuview import MenuView, StudentMenuView
from .views.mealentryview import MealEntryView, MealEntryCountView
from .views.login import SendUserVerificationCode, VerifyUserCode
from .views.face_rec import UserCheck


urlpatterns = [
    path("students/", StudentView.as_view()),
    path("meals/", MealView.as_view()),
    path("menu/", MenuView.as_view()),
    path("students-menu/", StudentMenuView.as_view()),
    path("meal-entries/", MealEntryView.as_view()),
    path('meal-counts/', MealEntryCountView.as_view()),

    path('send_phone/', SendUserVerificationCode.as_view()),
    path('verify_phone/', VerifyUserCode.as_view()),
    path('check_user/', UserCheck.as_view()),
]
