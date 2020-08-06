from django.urls import path
from . import views

urlpatterns = [
    path('', views.productindex, name='productindex'),
    path('addcomment/<int:id>', views.addcomment, name='addcomment'),
]
