from django.urls import path
from . import views


app_name = 'basket'
urlpatterns = [
     path('', views.basket_summary, name='basket-summary'),
     path('add/item/<int:pk>/', views.basket_add, name='basket-add'),
     path('delete/item/<int:pk>/', views.basket_delete, name='basket-delete')
]