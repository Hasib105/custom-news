# from django.shortcuts import render, get_object_or_404
# from .models import Article, Category
# from django.core.paginator import Paginator
# from django.http import HttpResponse
# from django.views.decorators.cache import cache_page

# # Create your views here.

# @cache_page(60 * 15)  # Cache for 15 minutes
# def about(request):
#     return render(request, 'about.html')

# @cache_page(60 * 15)  # Cache for 15 minutes
# def privacy(request):
#     return render(request, 'privacy.html')

# @cache_page(60 * 15)  # Cache for 15 minutes
# def terms(request):
#     return render(request, 'terms.html')

# @cache_page(60 * 15)  # Cache for 15 minutes
# def contact(request):
#     return render(request, 'contact.html')

# @cache_page(60 * 15)  # Cache for 15 minutes
# def index(request):
#     latest_news = Article.objects.filter(featured=False).only('title', 'slug', 'thumbnail', 'summary').order_by('-id')[:6]

#     first_article = latest_news[0] if latest_news else None
#     second_articles = latest_news[1:3]
#     third_articles = latest_news[3:]

#     featured_articles = Article.objects.filter(featured=True).only('title', 'slug', 'thumbnail', 'summary').order_by('-id')[:5]
#     main_article = featured_articles.first()
#     additional_articles = featured_articles[1:]

#     categories_with_articles = []
#     categories = Category.objects.filter(featured=True).only('title', 'slug')
#     for category in categories:
#         articles = Article.objects.filter(category=category).only('title', 'slug', 'thumbnail', 'summary').order_by('-id')[:4]
#         categories_with_articles.append({
#             'category': category,
#             'articles': articles
#         })

#     context = {
#         'first_article': first_article,
#         'second_articles': second_articles,
#         'third_articles': third_articles,
#         'categories_with_articles': categories_with_articles,
#         'main_article': main_article,
#         'additional_articles': additional_articles
#     }

#     return render(request, 'index.html', context)

# @cache_page(60 * 15)  # Cache for 15 minutes
# def article_details(request, slug):
#     article = get_object_or_404(Article, slug=slug)
#     latest_article = Article.objects.exclude(id=article.id).only('title', 'slug').order_by('-created_at')[:6]
#     related_articles = Article.objects.filter(category=article.category).exclude(id=article.id).only('title', 'slug', 'thumbnail', 'summary').order_by('-created_at')[:6]

#     article.views += 1
#     article.save()

#     context = {
#         'article': article,
#         'latest_article': latest_article,
#         'related_articles': related_articles
#     }
#     return render(request, 'article_detail.html', context)

# @cache_page(60 * 15)  # Cache for 15 minutes
# def category_detail(request, slug):
#     category = get_object_or_404(Category, slug=slug)
#     articles = Article.objects.filter(category=category).only('title', 'slug', 'thumbnail', 'summary').order_by('-created_at')
#     paginator = Paginator(articles, 26)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     context = {
#         'category': category,
#         'page_obj': page_obj
#     }
#     return render(request, 'category_detail.html', context)

# @cache_page(60 * 15)  # Cache for 15 minutes
# def articles_by_tags(request, tag_slug):
#     articles = Article.objects.filter(tags__icontains=tag_slug).only('title', 'slug', 'thumbnail', 'summary').order_by('-created_at')
#     paginator = Paginator(articles, 26)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     context = {
#         "page_obj": page_obj,
#         "tag": tag_slug
#     }

#     return render(request, "articles_by_tags.html", context)

# def robots_txt(request):
#     lines = [
#         "User-agent: *",
#         "Disallow: /admin/",
#         "Allow: /",
#     ]
#     return HttpResponse("\n".join(lines), content_type="text/plain")


from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.utils import timezone
from .models import Article, Category
from .serializers import ArticleSerializer, CategorySerializer


# Pagination class for Category and Tag articles
class CustomPagination(PageNumberPagination):
    page_size = 26  # Default page size
    page_size_query_param = 'page_size'
    max_page_size = 100


# API for the index view
@api_view(['GET'])
def api_index(request):
    # Latest news (non-featured)
    latest_news = Article.objects.filter(featured=False).order_by('-id')[:6]
    first_article = latest_news[0] if latest_news else None
    second_articles = latest_news[1:3]
    third_articles = latest_news[3:]

    # Featured articles
    featured_articles = Article.objects.filter(featured=True).order_by('-id')[:5]
    main_article = featured_articles.first()
    additional_articles = featured_articles[1:]

    # Categories with articles
    categories_with_articles = []
    categories = Category.objects.filter(featured=True)
    for category in categories:
        articles = Article.objects.filter(category=category).order_by('-id')[:4]
        categories_with_articles.append({
            'category': CategorySerializer(category).data,
            'articles': ArticleSerializer(articles, many=True).data
        })

    return Response({
        'first_article': ArticleSerializer(first_article).data if first_article else None,
        'second_articles': ArticleSerializer(second_articles, many=True).data,
        'third_articles': ArticleSerializer(third_articles, many=True).data,
        'categories_with_articles': categories_with_articles,
        'main_article': ArticleSerializer(main_article).data if main_article else None,
        'additional_articles': ArticleSerializer(additional_articles, many=True).data,
    })


# API for article details
@api_view(['GET'])
def api_article_details(request, slug):
    article = get_object_or_404(Article, slug=slug)
    related_articles = Article.objects.filter(category=article.category).exclude(id=article.id).order_by('-created_at')[:6]
    latest_articles = Article.objects.exclude(id=article.id).order_by('-created_at')[:6]

    # Increment views
    article.views += 1
    article.save()

    return Response({
        'article': ArticleSerializer(article).data,
        'related_articles': ArticleSerializer(related_articles, many=True).data,
        'latest_articles': ArticleSerializer(latest_articles, many=True).data,
    })


# API for category detail
@api_view(['GET'])
def api_category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    articles = Article.objects.filter(category=category).order_by('-created_at')

    # Use pagination
    paginator = CustomPagination()
    paginated_articles = paginator.paginate_queryset(articles, request)

    return paginator.get_paginated_response({
        'category': CategorySerializer(category).data,
        'articles': ArticleSerializer(paginated_articles, many=True).data,
    })


# API for articles by tags
@api_view(['GET'])
def api_articles_by_tags(request, tag_slug):
    articles = Article.objects.filter(tags__icontains=tag_slug).order_by('-created_at')

    # Use pagination
    paginator = CustomPagination()
    paginated_articles = paginator.paginate_queryset(articles, request)

    return paginator.get_paginated_response({
        'tag': tag_slug,
        'articles': ArticleSerializer(paginated_articles, many=True).data,
    })



@api_view(['GET'])
def api_category_context(request):
    categories = Category.objects.only('title', 'slug')
    exclusive_category = Category.objects.filter(exclusive=True).last()

    return Response({
        'categories': CategorySerializer(categories, many=True).data,
        'exclusive_category': CategorySerializer(exclusive_category).data if exclusive_category else None,
    })


@api_view(['GET'])
def api_most_popular_articles(request):
    yesterday = timezone.now() - timezone.timedelta(days=1)
    most_popular_articles = Article.objects.filter(created_at__gte=yesterday).only('title', 'slug').order_by('-views')[:7]

    return Response({
        'most_popular_articles': ArticleSerializer(most_popular_articles, many=True).data
    })