from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
    path('employees/', include('employees.urls')),
    path('leaves/', include('leaves.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('payroll/', include('payroll.urls')),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('performance/', include('performance_reviews.urls')),
    path('announcements/', include('announcements.urls')),
    path('birthdays/', include('birthday_calendar.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
