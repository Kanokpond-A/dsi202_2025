from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import TreeViewSet, EquipmentViewSet, PlantingLocationViewSet

# API Router
router = DefaultRouter()
router.register(r'trees', TreeViewSet)
router.register(r'equipment', EquipmentViewSet)
router.register(r'locations', PlantingLocationViewSet)

urlpatterns = [

    # --- 🌐 Web Views ---
    path('', views.getstart, name='getstarted'),                  # หน้าเริ่มต้น
    path('home/', views.home, name='home'),                       # หน้า Home
    path('about/', views.about, name='about'),                    # เกี่ยวกับเรา
    path('trees/', views.tree_equipment_list, name='tree_equipment_list'),  # ต้นไม้+อุปกรณ์
    path('trees-equipment/', views.tree_equipment_list),          # สำรองให้ลิงก์เก่า
    path('cart/', views.cart, name='cart'),                       # ตะกร้าสินค้า
    path('add-to-cart/<str:item_type>/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('buy-now/<str:item_type>/<int:item_id>/', views.buy_now, name='buy_now'),
    path('order/', views.order, name='order'),                    # หน้ายืนยันคำสั่งซื้อ
    path('confirm-order/', views.confirm_order, name='confirm_order'),  # จาก cart
    path('confirm-order/<str:item_type>/<int:item_id>/', views.confirm_order, name='confirm_order'),  # จาก buy now
    path('confirm-selected/', views.confirm_selected_order, name='confirm_selected_order'),  # cart many
    path('payment/', views.payment, name='payment'),
    path('generate-qr/<int:order_id>/', views.generate_qr, name='generate_qr'),
    path('confirm-payment/', views.confirm_payment, name='confirm_payment'),

    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),

    path('notification/', views.notification_list, name='notification'),
    path('mytree/', views.mytree, name='mytree'),

    path('remove-from-cart/<str:item_type>/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('remove-selected/', views.bulk_remove_from_cart, name='bulk_remove_from_cart'),

    # --- 🧩 API Routes ---
    path('api/', include(router.urls)),  # API: /api/trees/, /api/equipment/, /api/locations/
]
