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
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('article/<str:slug>/', views.article_details, name='article_details'),  
    path('category/<str:slug>/', views.category_detail, name='category_detail'),
    path("articles/tag/<str:tag_slug>/", views.articles_by_tags, name="articles_by_tags"),


    #seo urls
    path('robots.txt', views.robots_txt, name='robots.txt'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps }, name='django.contrib.sitemaps.views.sitemap'),
]
