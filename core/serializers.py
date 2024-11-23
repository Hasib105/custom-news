from rest_framework import serializers
from .models import Article, Category, ArticleContent

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'slug', 'tags', 'summary', 'featured', 'exclusive']

class ArticleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Article
        fields = [
            'id',
            'title',
            'slug',
            'category',
            'author',
            'thumbnail',
            'tags',
            'summary',
            'views',
            'featured',
            'created_at',
            'updated_at',
        ]

class ArticleContentSerializer(serializers.ModelSerializer):
    article = ArticleSerializer(read_only=True)

    class Meta:
        model = ArticleContent
        fields = ['id', 'article', 'title', 'image', 'image_title', 'content']
