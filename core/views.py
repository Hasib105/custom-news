from django.shortcuts import render , get_object_or_404
from .models import Article,Category,ArticleContent
# Create your views here.


def index(request):
    latest_news = Article.objects.only('title','slug','thumbnail','summary').order_by('-id')[:6]
    
    first_article = latest_news[0] if latest_news else None
    second_articles = latest_news[1:3]
    third_articles = latest_news[3:]

    featured_articles = Article.objects.filter(featured=True).only('title','slug','thumbnail','summary').order_by('-id')[:5]
    main_article = featured_articles.first()  
    additional_articles = featured_articles[1:]  

    categories_with_articles = []
    categories = Category.objects.filter(featured=True).only('title', 'slug')
    for category in categories:
        articles = Article.objects.filter(category=category).only('title', 'slug', 'thumbnail', 'summary').order_by('-id')[:4]
        categories_with_articles.append({
            'category': category,
            'articles': articles
        })

    
    context = {
        'first_article': first_article,
        'second_articles': second_articles,
        'third_articles': third_articles,
        'categories_with_articles': categories_with_articles,
        'main_article': main_article,
        'additional_articles': additional_articles
    }
    
    return render(request, 'index.html', context)


def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)

    article.views += 1
    article.save()
    context = {
        'article': article
    }
    return render(request, 'article_detail.html', context)

def about(request):
    return render(request, 'about.html')

def privacy(request):
    return render(request, 'privacy.html')


def terms(request):
    return render(request, 'terms.html')


def contact(request):
    return render(request, 'contact.html')