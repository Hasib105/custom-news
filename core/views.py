from django.shortcuts import render
from .models import Article,Category,ArticleContent
# Create your views here.


def index(request):
    context = {}
    return render(request, 'index.html',context)

def about(request):
    return render(request, 'about.html')

def privacy(request):
    return render(request, 'privacy.html')


def terms(request):
    return render(request, 'terms.html')


def contact(request):
    return render(request, 'contact.html')