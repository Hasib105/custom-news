from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('article/<str:slug>/', views.article_details, name='article_details'),  
    path('category/<str:slug>/', views.category_detail, name='category_detail'),

]
