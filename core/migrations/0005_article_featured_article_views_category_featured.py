# Generated by Django 5.1.2 on 2024-10-24 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_article_slug_alter_category_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='featured',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='article',
            name='views',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='category',
            name='featured',
            field=models.BooleanField(default=False),
        ),
    ]
