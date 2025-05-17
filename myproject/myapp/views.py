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

def tree_list(request):
    return render(request, 'tree_list.html')
