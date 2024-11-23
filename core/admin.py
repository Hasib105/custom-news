from django.contrib import admin as django_admin
from unfold import admin
from unfold.admin import ModelAdmin
from .models import Article, ArticleContent, Category



class ArticleContentInline(admin.StackedInline):
    model = ArticleContent
    extra = 1  # Defines how many empty inlines to show by default
    fields = ('title', 'image', 'image_title', 'content')  # Fields to display in the inline

    # def get_formset(self, request, obj=None, **kwargs):
    #     formset = super().get_formset(request, obj, **kwargs)
    #     formset.form.base_fields['content'].widget.attrs.update({
    #         'class': 'quill-editor',
    #         'style': 'height: 500px; overflow-y: auto;'  # Set height and enable scrolling
    #     })
    #     return formset


@django_admin.register(Article)
class ArticleAdmin(ModelAdmin):
    list_display = ('title', 'category', 'slug', 'tags', 'summary')
    exclude = ('author','slug',)
    search_fields = ('title', 'tags')  
    inlines = [ArticleContentInline]  

    def save_model(self, request, obj, form, change):
        if not obj.author:
            obj.author = request.user
        super().save_model(request, obj, form, change)

@django_admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ('title', 'slug', 'summary')
    exclude = ('slug',)
    search_fields = ('title',)

# Optionally register other models if needed