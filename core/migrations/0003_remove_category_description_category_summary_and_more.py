# Generated by Django 5.1.2 on 2024-10-24 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_article_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='description',
        ),
        migrations.AddField(
            model_name='category',
            name='summary',
            field=models.TextField(blank=True, max_length=160),
        ),
        migrations.AddField(
            model_name='category',
            name='tags',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]