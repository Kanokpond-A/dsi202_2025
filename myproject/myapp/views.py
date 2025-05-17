from django.shortcuts import render
from .models import Tree

def getstart(request):
    return render(request, 'getstarted.html')

def home(request):
    trees = Tree.objects.all()[:3]  # แนะนำ 3 ต้นไม้
    return render(request, 'home.html', {'trees': trees})

def tree_list(request):
    return render(request, 'tree_list.html')
