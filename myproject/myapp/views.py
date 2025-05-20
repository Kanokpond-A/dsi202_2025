from django.shortcuts import render, redirect
from .models import Tree, Equipment, Notification, OrderItem, Purchase, PlantingLocation
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
def order(request):
    if request.method == "POST":
        selected_raw = request.POST.getlist('selected_items')  # ['tree:2', 'equipment:4', ...]
        selected_items = []
        for sel in selected_raw:
            item_type, item_id = sel.split(":")
            item_id = int(item_id)
            quantity = int(request.POST.get(f'quantity_{item_type}_{item_id}', 1))

            model = Tree if item_type == 'tree' else Equipment
            obj = model.objects.get(id=item_id)

            selected_items.append({
                'type': item_type,
                'id': item_id,
                'name': obj.name,
                'image_url': obj.image_url,
                'price': float(obj.price),
                'quantity': quantity,
            })

        request.session['selected_items'] = selected_items
        locations = PlantingLocation.objects.all()
        return render(request, 'order.html', {
            'items': selected_items,
            'locations': locations
        })

    return redirect('cart')


def confirm_selected_order(request):
    if request.method == 'POST':
        selected_raw = request.POST.getlist('selected_items')
        location_id = request.POST.get('location_id')
        location = PlantingLocation.objects.get(id=location_id)

        items = []
        for sel in selected_raw:
            item_type, item_id = sel.split(':')
            item_id = int(item_id)
            quantity = int(request.POST.get(f'quantity_{item_type}_{item_id}', 1))

            model = Tree if item_type == 'tree' else Equipment
            obj = model.objects.get(id=item_id)

            items.append({
                'item_type': item_type,
                'item_id': item_id,
                'name': obj.name,
                'price': obj.price,
                'quantity': quantity
            })

        # สร้าง Purchase หลัก
        purchase = Purchase.objects.create(
            user=request.user,
            location=location
        )

        # บันทึก OrderItem
        for item in items:
            OrderItem.objects.create(
                purchase=purchase,
                item_type=item['item_type'],
                item_id=item['item_id'],
                name=item['name'],
                price=item['price'],
                quantity=item['quantity'],
            )

        request.session['order_id'] = purchase.id
        return redirect('payment')
    
    return redirect('cart')





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
    my_trees = OrderItem.objects.filter(user=request.user)
    purchases = Purchase.objects.filter(user=request.user)
    return render(request, 'mytree.html', {'my_trees': my_trees})

def confirm_order(request):
    if request.method == 'POST':
        selected_raw = request.POST.getlist('selected_items')
        location_id = request.POST.get('location_id')
        location = PlantingLocation.objects.get(id=location_id)

        items = []
        total_price = 0

        for sel in selected_raw:
            item_type, item_id = sel.split(':')
            item_id = int(item_id)
            quantity = int(request.POST.get(f'quantity_{item_type}_{item_id}', 1))

            model = Tree if item_type == 'tree' else Equipment
            obj = model.objects.get(id=item_id)

            item_total = obj.price * quantity
            total_price += item_total

            items.append({
                'item_type': item_type,
                'item_id': item_id,
                'name': obj.name,
                'price': obj.price,
                'quantity': quantity
            })

        # ✅ สร้าง Purchase หลัก
        purchase = Purchase.objects.create(
            user=request.user,
            location=location,
            total_price=total_price  # ✅ ใช้ฟิลด์ใหม่
        )

        # ✅ เพิ่ม OrderItem ทุกรายการ
        for item in items:
            OrderItem.objects.create(
                purchase=purchase,
                item_type=item['item_type'],
                item_id=item['item_id'],
                name=item['name'],
                price=item['price'],
                quantity=item['quantity'],
            )

        # ✅ ส่ง order ไป payment
        request.session['order_id'] = purchase.id
        return redirect('payment')

    return redirect('cart')


def payment(request):
    order_id = request.session.get('order_id')

    if not order_id:
        return redirect('cart')

    order = Purchase.objects.get(id=order_id)
    return render(request, 'payment.html', {'order': order})  # ✅ ต้องมี 'order'



def crc16_ccitt_false(data: bytes) -> int:
    crc = 0xFFFF
    for byte in data:
        crc ^= byte << 8
        for _ in range(8):
            if (crc & 0x8000):
                crc = (crc << 1) ^ 0x1021
            else:
                crc <<= 1
            crc &= 0xFFFF
    return crc

def _format_tlv(tag: str, value: str) -> str:
    return f"{tag}{len(value):02d}{value}"

def calculate_crc(payload: str) -> str:
    encoded_string = payload.encode('ascii')
    crc_val = crc16_ccitt_false(encoded_string)
    return f"{crc_val:04X}"

def generate_promptpay_payload(
    mobile_number: str = None,
    national_id: str = None,
    amount: float = 0.0
) -> str:
    if not mobile_number and not national_id:
        raise ValueError("You must provide either a mobile_number or a national_id")

    payload = ""
    payload += _format_tlv("00", "01")
    payload += _format_tlv("01", "11")  # Static QR

    # --- Merchant Account Info (Tag 29) ---
    merchant = _format_tlv("00", "A000000677010111")  # PromptPay AID

    if mobile_number:
        # Strip 0 -> replace with 66 (Thailand)
        formatted_mobile = f"0066{mobile_number[1:]}"
        merchant += _format_tlv("01", formatted_mobile)
    elif national_id:
        cleaned_nid = national_id.replace("-", "")
        if len(cleaned_nid) != 13 or not cleaned_nid.isdigit():
            raise ValueError("National ID must be 13 digits")
        merchant += _format_tlv("02", cleaned_nid)

    payload += _format_tlv("29", merchant)
    payload += _format_tlv("53", "764")  # Currency: THB
    payload += _format_tlv("54", f"{amount:.2f}")  # Amount
    payload += _format_tlv("58", "TH")  # Country Code

    payload_for_crc = payload + "6304"
    crc = calculate_crc(payload_for_crc)
    payload += _format_tlv("63", crc)

    return payload

def generate_qr(request, order_id):
    order = Purchase.objects.get(id=order_id)

    # คำนวณราคารวมจากรายการย่อย
    items = OrderItem.objects.filter(purchase=order)
    amount = sum(item.price * item.quantity for item in items)

    # ใช้เบอร์หรือบัตรประชาชน PromptPay ของร้านคุณ
    promptpay_mobile = None  # เช่น "0812345678"
    promptpay_nid = "1839901855668"  # ต้องเป็นเลข 13 หลักเท่านั้น

    payload = generate_promptpay_payload(
        mobile_number=promptpay_mobile,
        national_id=promptpay_nid,
        amount=float(order.total_price)
    )

    qr = qrcode.make(payload)
    buffer = BytesIO()
    qr.save(buffer, format='PNG')
    buffer.seek(0)

    return HttpResponse(buffer.getvalue(), content_type='image/png')



