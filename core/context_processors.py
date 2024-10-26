from .models import Category , Article
from django.utils import timezone

def category_context(request):
    categories = Category.objects.only('title','slug')
    exclusive_category = Category.objects.filter(exclusive=True).last()
    context = {
        'categories': categories,
        'exclusive_category': exclusive_category
    }

    return context



def most_popular_articles(request):
    yesterday = timezone.now() - timezone.timedelta(days=1)
    most_popular_articles = Article.objects.filter(created_at__gte=yesterday).only('title','slug').order_by('-views')[:7]
    context = {
        'most_popular_articles': most_popular_articles
    }

    return context
