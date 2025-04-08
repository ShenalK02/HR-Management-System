from django.urls import path
from . import views

urlpatterns = [
    # Leave Request URLs
    path('', views.leave_request_list, name='leave_list'),
    path('create/', views.leave_request_create, name='leave_create'),
    path('<int:pk>/approve/', views.leave_request_approve, name='leave_approve'),
    path('<int:pk>/reject/', views.leave_request_reject, name='leave_reject'),

    # LeaveType URLs
    path('types/', views.LeaveTypeListView.as_view(), name='leavetype_list'),
    path('types/create/', views.LeaveTypeCreateView.as_view(), name='leavetype_create'),
    path('types/<int:pk>/update/', views.LeaveTypeUpdateView.as_view(), name='leavetype_update'),
    path('types/<int:pk>/delete/', views.LeaveTypeDeleteView.as_view(), name='leavetype_delete'),
]