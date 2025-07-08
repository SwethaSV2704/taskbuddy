from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home, name='home'),
    path('toggle/<int:task_id>/', views.toggle_task, name='toggle_task'),
path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
]