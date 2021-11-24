
from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views


app_name = 'accounts'

urlpatterns = [
     path('register/', views.user_register, name='register'),
     path('register/restaurnat', views.restaurant_register, name='restaurant-register'),
     path('login/', views.user_login, name='login'),
     path('logout/', auth_views.LogoutView.as_view(next_page='accounts:login'), name='logout'),
     path('dashboard/<int:year>/<str:month>/<int:day>/', views.DailyDashboardView.as_view(), name='dashboard'),
     path('profile/', views.profile, name='profile')
]
