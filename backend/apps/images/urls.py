from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_create_image, name='list_create_view'),
    path('<int:pk>/', views.image_detail, name='image_detail_view'),
]
