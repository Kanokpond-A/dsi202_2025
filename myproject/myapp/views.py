from django.shortcuts import render
from .models import Tree

def home(request):
    return render(request, 'home.html')

def tree_list(request):
    return render(request, 'tree_list.html')
