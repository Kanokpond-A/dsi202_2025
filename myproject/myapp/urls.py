from django.urls import path
from . import views

urlpatterns = [
    path('', views.getstart, name='getstarted'),  # หน้าแรก
    path('home/', views.home, name='home'),      # หน้า home จริงหลังจากกด Get Started
    path('trees/<int:pk>/', views.tree_list, name='tree_list'),
]
