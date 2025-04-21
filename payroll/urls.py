from django.urls import path
from . import views

urlpatterns = [
    path('', views.payroll_dashboard, name='payroll_dashboard'),
    path('add/', views.add_payroll, name='add_payroll'),
    path('admin/', views.add_payroll, name='payroll_admin'),  # Optional alias
]

