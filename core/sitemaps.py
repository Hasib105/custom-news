# myapp/sitemaps.py
from django.contrib.sitemaps import Sitemap
from .models import Category, Article, ArticleContent

class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return Category.objects.all()

    def location(self, item):
        return item.get_absolute_url()

class ArticleSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return Article.objects.all()

    def location(self, item):
        return item.get_absolute_url()

class ArticleContentSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return ArticleContent.objects.all()

    def location(self, item):
        return item.article.get_absolute_url()  # Assuming you want to link to the article