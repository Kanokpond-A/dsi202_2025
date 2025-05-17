from django.shortcuts import render
from .models import Tree, Equipment

def getstart(request):
    return render(request, 'getstarted.html')

def home(request):
    trees = Tree.objects.all()[:3]  # แนะนำ 3 ต้นไม้
    return render(request, 'home.html', {'trees': trees})

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

def tree_list(request):
    return render(request, 'tree_list.html')
