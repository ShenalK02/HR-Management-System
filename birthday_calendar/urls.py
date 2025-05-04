from django.urls import path
from . import views

app_name = 'birthday_calendar'

urlpatterns = [
    path('', views.calendar_view, name='calendar'),
    path('create/', views.create_wish, name='create_wish'),
    path('create/<int:user_id>/', views.create_wish, name='create_wish_for_user'),
    path('view/<int:wish_id>/', views.view_wish, name='view_wish'),
    path('edit/<int:wish_id>/', views.edit_wish, name='edit_wish'),
    path('delete/<int:wish_id>/', views.delete_wish, name='delete_wish'),
    path('todays-birthdays/', views.todays_birthdays, name='todays_birthdays'),
]