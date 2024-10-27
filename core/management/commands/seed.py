import random
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from faker import Faker
from django.contrib.auth import get_user_model
from core.models import Category, Article, ArticleContent  # Make sure ArticleContent is imported
import datetime

User = get_user_model()
fake = Faker()

class Command(BaseCommand):
    help = "Generate 10 categories, 20 articles, 100 article contents, and create an admin user."

    def handle(self, *args, **kwargs):
        # Create superuser named "admin" with password "admin" if not exists
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@example.com", "admin")
            self.stdout.write(self.style.SUCCESS("Superuser 'admin' created with password 'admin'."))
        else:
            self.stdout.write(self.style.WARNING("Superuser 'admin' already exists."))

        # Check if there is an existing user for authoring articles
        if not User.objects.exists():
            self.stdout.write(self.style.ERROR("No users available. Please create at least one user."))
            return

        author = User.objects.first()

        # Create 10 categories
        categories = []
        for i in range(10):
            title = fake.unique.word().capitalize()
            category, created = Category.objects.get_or_create(
                title=title,
                defaults={
                    'slug': slugify(title),
                    'tags': ', '.join(fake.words(3)),
                    'summary': fake.text(160),
                    'featured': random.choice([True, False]),
                },
            )
            categories.append(category)
            self.stdout.write(self.style.SUCCESS(f"Created Category: {title}"))

        # Create 20 articles
        articles = []
        for _ in range(20):
            title = fake.sentence(nb_words=5)
            article, created = Article.objects.get_or_create(
                title=title,
                defaults={
                    'slug': slugify(title),
                    'category': random.choice(categories),
                    'author': author,
                    'tags': ', '.join(fake.words(5)),
                    'summary': fake.text(160),
                    'views': random.randint(0, 1000),
                    'featured': random.choice([True, False]),
                },
            )
            articles.append(article)
            self.stdout.write(self.style.SUCCESS(f"Created Article: {title}"))

        # Create 5 ArticleContents for each Article (100 in total for 20 articles)
        for article in articles:
            for _ in range(5):  # Adjust this if you want more or fewer contents per article
                content = ArticleContent.objects.create(
                    article=article,
                    title=fake.sentence(nb_words=3),
                    image=None,  # You could assign an image here if desired
                    image_title=fake.sentence(nb_words=2),
                    content=fake.paragraph(nb_sentences=5)
                )
                self.stdout.write(self.style.SUCCESS(f"Created Content for Article: {content.article.title}"))

        self.stdout.write(self.style.SUCCESS("Successfully generated 10 categories, 20 articles, 100 article contents, and created an admin user."))
