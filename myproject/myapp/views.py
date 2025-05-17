from django.shortcuts import render
from .models import Tree

def getstart(request):
    return render(request, 'getstarted.html')

def home(request):
    return render(request, 'home.html')

def tree_list(request):
    return render(request, 'tree_list.html')
