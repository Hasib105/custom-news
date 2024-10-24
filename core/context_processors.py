from .models import Category , Article

def category_context(request):
    categories = Category.objects.only('title','slug')
    featured_category = Category.objects.filter(featured=True).last()
    context = {
        'categories': categories,
        'featured_category': featured_category
    }

    return context

def latest_articles(request):
    latest_articles = Article.objects.only('title','slug').order_by('-created_at')[:6]
    context = {
        'latest_articles': latest_articles
    }

    return context


def most_popular_articles(request):
    most_popular_articles = Article.objects.only('title','slug').order_by('-views')[:7]
    context = {
        'most_popular_articles': most_popular_articles
    }

    return context