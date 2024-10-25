from django.shortcuts import render
from .models import Article,Category,ArticleContent
# Create your views here.


def index(request):
    latest_news = Article.objects.all().order_by('-id')[:6]
    
    first_article = latest_news[0] if latest_news else None
    second_articles = latest_news[1:3]
    third_articles = latest_news[3:]

    context = {
        'first_article': first_article,
        'second_articles': second_articles,
        'third_articles': third_articles,
    }
    
    return render(request, 'index.html', context)

def about(request):
    return render(request, 'about.html')

def privacy(request):
    return render(request, 'privacy.html')


def terms(request):
    return render(request, 'terms.html')


def contact(request):
    return render(request, 'contact.html')