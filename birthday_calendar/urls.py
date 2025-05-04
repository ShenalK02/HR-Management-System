from django.urls import path
from . import views

app_name = 'birthday_calendar'

urlpatterns = [
    path('', views.birthday_calendar, name='calendar'),
    path('create-wish/<int:employee_id>/', views.create_birthday_wish, name='create_wish'),
    path('view-wish/<int:wish_id>/', views.view_birthday_wish, name='view_wish'),
    path('api/upcoming/', views.upcoming_birthdays_api, name='upcoming_api'),
]