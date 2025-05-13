from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # ✅ เส้นทาง root แสดงหน้า welcome
    path('trees/', views.tree_list, name='tree_list'),
]
