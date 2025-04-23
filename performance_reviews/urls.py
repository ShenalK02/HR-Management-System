from django.urls import path
from . import views

urlpatterns = [
    path('calendar/', views.review_calendar, name='review_calendar'),
    path('schedule/', views.schedule_review, name='schedule_review'),
    path('review/<int:pk>/', views.review_detail, name='review_detail'),
    path('review/<int:pk>/feedback/', views.edit_feedback, name='edit_feedback'),
    path('review/<int:pk>/employee-feedback/', views.employee_feedback, name='employee_feedback'),
]