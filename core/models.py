from django.db import models
from django.conf import settings
from django_quill.fields import QuillField
from django.core.files.images import get_image_dimensions
from django.core.files.base import ContentFile
from PIL import Image
import io
import os
import pillow_avif
from django.urls import reverse
from unidecode import unidecode
from django.utils.text import slugify
import datetime

User = settings.AUTH_USER_MODEL

def convert_image(image_field, quality=None):
    """
    Convert uploaded images to WebP format while preserving transparency.

    Args:
        image_field (File): The uploaded image file.
        quality (int): Quality percentage for compression (1-100).

    Returns:
        ContentFile: The converted image file.
    """
    quality = quality or getattr(settings, "IMAGE_CONVERSION_QUALITY", 75)

    try:
        # Open the uploaded image
        img = Image.open(image_field)
    except Exception as e:
        # Handle the error appropriately
        print(f"Error opening image: {e}")
        return image_field

    # Preserve transparency if present
    has_transparency = img.mode in ("RGBA", "LA") or (
        img.mode == "P" and "transparency" in img.info
    )
    img = img.convert("RGBA") if has_transparency else img.convert("RGB")

    # Prepare a BytesIO buffer to save the converted image
    buffer = io.BytesIO()

    # Save as WebP format
    img.save(buffer, format='WEBP', quality=quality)

    # Create a new filename with the appropriate extension
    filename = os.path.splitext(image_field.name)[0] + ".webp"

    # Create a ContentFile from the buffer
    converted_image = ContentFile(buffer.getvalue(), name=filename)

    return converted_image


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Category(BaseModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True,allow_unicode=True)
    tags = models.CharField(max_length=255, blank=True)  # Store tags as a comma-separated string
    summary = models.TextField(max_length=160, blank=True)
    featured = models.BooleanField(default=False)
    exclusive = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_tags_list(self):
        return [tag.strip() for tag in self.tags.split(',')] if self.tags else []

    class Meta:
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            slug_str = f"{self.title}-{datetime.datetime.now()}"
            self.slug = slugify(slug_str, allow_unicode=True) 
        super().save(*args, **kwargs)

    
    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"slug": self.slug})

class Article(BaseModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, allow_unicode=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    thumbnail = models.ImageField(upload_to='thumbnails', null=True, blank=True)
    tags = models.CharField(max_length=255, blank=True)
    summary = models.TextField(max_length=160, blank=True)
    views = models.PositiveIntegerField(default=0)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_tags_list(self):
        return [tag.strip() for tag in self.tags.split(',')] if self.tags else []

    def save(self, *args, **kwargs):
        if not self.slug:
            slug_str = f"{self.title}-{datetime.datetime.now()}"
            self.slug = slugify(slug_str, allow_unicode=True) 
        
            # Check if thumbnail needs conversion
        if self.thumbnail:
            if not self.thumbnail.name.endswith((".webp", ".avif")):
                converted_image = convert_image(self.thumbnail)
                self.thumbnail = converted_image

            # Save the instance
        super().save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse("article_details", kwargs={"slug": self.slug})



class ArticleContent(BaseModel):
    article = models.ForeignKey(Article, related_name='contents', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='article_images/', blank=True, null=True)  # For images
    image_title = models.CharField(max_length=255, blank=True, null=True)  # Image title
    content = QuillField(null=True, blank=True)

    def __str__(self):
        return f"{self.article.title}"

    def save(self, *args, **kwargs):
        if self.image and not self.image.name.endswith((".webp", ".avif")):
            converted_image = convert_image(self.image)
            self.image = converted_image
        super().save(*args, **kwargs)