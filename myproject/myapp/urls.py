from django.urls import path
from . import views

urlpatterns = [
    path('', views.getstart, name='getstarted'),  # หน้าแรก
    path('home/', views.home, name='home'), # หน้า home จริงหลังจากกด Get Started
    # path('tree/<int:pk>/', views.tree_detail, name='tree_detail'),
    path('about/', views.about, name='about'),    
    path('trees/<int:pk>/', views.tree_list, name='tree_list'),
    path('trees-equipment/', views.tree_equipment_list, name='tree_equipment_list'),
    path('trees/', views.tree_equipment_list, name='tree_equipment_list'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<str:item_type>/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('buy-now/<str:item_type>/<int:item_id>/', views.buy_now, name='buy_now'),
    path('order/', views.order, name='order'),
    path('confirm-order/<str:item_type>/<int:item_id>/', views.confirm_order, name='confirm_order'),
    path('confirm-order/', views.confirm_order, name='confirm_order'),
    # path('confirm-order/', views.confirm_order, name='confirm_selected_order'),
    path('confirm-order/', views.confirm_selected_order, name='confirm_selected_order'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('notification/', views.notification_list, name='notification'),
    path('mytree/', views.mytree, name='mytree'),
    path('payment/', views.payment, name='payment'),
    path('generate-qr/<int:order_id>/', views.generate_qr, name='generate_qr'),
    path('confirm-payment/', views.confirm_payment, name='confirm_payment'),
    path('remove-from-cart/<str:item_type>/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('remove-selected/', views.bulk_remove_from_cart, name='bulk_remove_from_cart'),



    





]
