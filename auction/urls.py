from django.urls import path

from . import views


app_name = 'auction'
urlpatterns = [
    path('<int:item_id>/', views.detail, name='detail'),
    path('create/', views.create, name='create'),
    path('<int:item_id>/add-to-cart/', views.add_prod_to_cart, name='add_prod_to_cart'),
    path('remove-from-cart/', views.remove_prod_from_cart, name='remove_prod_from_cart'),
    path('place-order/', views.place_order, name='place_order'),
    path('<int:item_id>/restock/', views.restock, name='restock'),
]
