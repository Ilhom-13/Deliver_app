from django.urls import path
from . import views

app_name = 'food'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('categories/add/', views.category_create, name='category-add'),
    path('categories/<str:category>/', views.CategoryView.as_view(), name='category'),
    path('items', views.ItemListView.as_view(), name='all-items'),
    path('items/add/', views.item_create, name='item-add'),
    path('items/delete/', views.ItemsDeletionView.as_view(), name='items-for-deletion'),
    path('items/<slug:slug>/', views.ItemDetail.as_view(), name='item-detail'),
    path('items/<int:pk>/delete/', views.item_delete, name='item-delete'),
    path('restaurants/<slug:slug>/', views.RestaurantView.as_view(), name='restaurant'),
    path('restaurants/<slug:slug>/info', views.RestaurantSellInfoView.as_view(), name='restaurant-items-info'),
    path('orders/<int:pk>/update/', views.order_update, name='order-update'),
    path('orders/create', views.order_create, name='order-create')
]
