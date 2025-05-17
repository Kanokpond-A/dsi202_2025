from django.shortcuts import render, redirect
from .models import Tree, Equipment, Notification, TreeOrder, Purchase, PlantingLocation
from .forms import SignUpForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
import qrcode
from io import BytesIO
from django.http import HttpResponse

def getstart(request):
    return render(request, 'getstarted.html')

def home(request):
    trees = Tree.objects.all()[:3]  # แนะนำ 3 ต้นไม้
    return render(request, 'home.html', {'trees': trees})

def home(request):
    notifications = []
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user).order_by('-notification_date')[:5]
    return render(request, 'home.html', {'notifications': notifications})

# def tree_detail(request, pk):
#     tree = Tree.objects.get(pk=pk)
#     return render(request, 'tree_detail.html', {'tree': tree})


def about(request):
    return render(request, 'aboutus.html')

def tree_equipment_list(request):
    query = request.GET.get('q', '')
    trees = Tree.objects.filter(name__icontains=query)
    equipment = Equipment.objects.filter(name__icontains=query)
    return render(request, 'tree_equipment_list.html', {
        'trees': trees,
        'equipment': equipment,
        'query': query,
    })

def add_to_cart(request, item_type, item_id):
    cart = request.session.get('cart', [])
    cart.append({'type': item_type, 'id': item_id, 'quantity': 1})
    request.session['cart'] = cart
    return redirect('cart')

def cart(request):
    cart_items = request.session.get('cart', [])
    display_items = []

    for item in cart_items:
        if item['type'] == 'tree':
            obj = Tree.objects.get(id=item['id'])
        elif item['type'] == 'equipment':
            obj = Equipment.objects.get(id=item['id'])
        else:
            continue

        display_items.append({
            'type': item['type'],
            'id': item['id'],
            'name': obj.name,
            'image_url': obj.image_url,
            'price': obj.price,
            'quantity': item.get('quantity', 1),
        })

    total_price = sum([i['price'] * i['quantity'] for i in display_items])

    return render(request, 'cart.html', {
        'items': display_items,
        'total': total_price,
    })

@csrf_exempt
def order(request, item_type, item_id):
    tree = Tree.objects.get(id=item_id)
    locations = PlantingLocation.objects.all()
    if request.method == "POST":
        request.session['cart'] = []  # Clear cart
        return redirect('tree_equipment_list')  # or redirect to thank you page
    else:
        cart_items = request.session.get('cart', [])
        display_items = []
        for item in cart_items:
            model = Tree if item['type'] == 'tree' else Equipment
            obj = model.objects.get(id=item['id'])
            display_items.append({
                'name': obj.name,
                'image_url': obj.image_url,
                'price': obj.price,
                'quantity': item['quantity'],
            })
        return render(request, 'order.html', {'items': display_items,
                                              'tree': tree,
        'locations': locations})

def tree_list(request):
    return render(request, 'tree_list.html')

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def notification_list(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-notification_date')
    return render(request, 'notification_list.html', {
        'notifications': notifications
    })

@login_required
def mytree(request):
    my_trees = TreeOrder.objects.filter(user=request.user)
    purchases = Purchase.objects.filter(user=request.user)
    return render(request, 'mytree.html', {'my_trees': my_trees})

def confirm_order(request, item_type, item_id):
    if request.method == 'POST':
        # สมมุติคุณดึงข้อมูลเหล่านี้มาจากฟอร์ม
        tree_id = request.POST.get('tree_id')
        amount = request.POST.get('amount')
        address = request.POST.get('address')  # หรือเอาค่าจาก user.profile ก็ได้
        location_id = request.POST.get('location_id')
        location = PlantingLocation.objects.get(id=location_id)


        # สร้างคำสั่งซื้อ
        order = Purchase.objects.create(
            user=request.user,
            tree_id=tree_id,
            item_type=item_type,
            price=Tree.objects.get(id=item_id).price,
            amount=amount,
            address=address,
            location=location,
        )

        # เก็บ order.id ลง session
        request.session['order_id'] = order.id

        return redirect('payment')  # ไปหน้าแสดง QR

    return redirect('cart')  # fallback ถ้ามาแบบ GET


def payment(request):
    order_id = request.session.get('order_id')

    if not order_id:
        return redirect('cart')  # กลับไปที่ cart ถ้าไม่มีออเดอร์

    order = Purchase.objects.get(id=order_id)

    return render(request, 'payment.html', {'order': order})



def generate_qr(request):
    data = "00020101021129370016A000000677010111011300660123456789802TH530376463041234"  # ใส่ PromptPay Payload หรือ URL
    img = qrcode.make(data)

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    image_data = buffer.getvalue()

    return HttpResponse(image_data, content_type="image/png")



