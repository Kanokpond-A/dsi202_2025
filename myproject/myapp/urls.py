from django.urls import path
from . import views

urlpatterns = [
    path('', views.getstart, name='getstarted'),  # หน้าแรก
    path('home/', views.home, name='home'), # หน้า home จริงหลังจากกด Get Started
    path('about/', views.about, name='about'),    
    path('trees/<int:pk>/', views.tree_list, name='tree_list'),
    path('trees-equipment/', views.tree_equipment_list, name='tree_equipment_list'),
    path('cart/', views.cart, name='cart'),
path('add-to-cart/<str:item_type>/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
path('order/', views.order, name='order'),

]
