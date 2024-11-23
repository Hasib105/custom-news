from django.urls import path
from . import views

from django.contrib.sitemaps.views import sitemap
from .sitemaps import CategorySitemap, ArticleSitemap, ArticleContentSitemap

sitemaps = {
    'categories': CategorySitemap,
    'articles': ArticleSitemap,
    'article_contents': ArticleContentSitemap,
}


urlpatterns = [
    path('index/', views.api_index, name='index'),
    path('article/<str:slug>/', views.api_article_details, name='article_details'),  
    path('category/<str:slug>/', views.api_category_detail, name='category_detail'),
    path("articles/tag/<str:tag_slug>/", views.api_articles_by_tags, name="articles_by_tags"),
    path('categories/', views.api_category_context, name='api_category_context'),
    path('most-popular-articles/', views.api_most_popular_articles, name='api_most_popular_articles'),


    # #seo urls
    # path('robots.txt', views.robots_txt, name='robots.txt'),
    # path('sitemap.xml', sitemap, {'sitemaps': sitemaps }, name='django.contrib.sitemaps.views.sitemap'),
]


