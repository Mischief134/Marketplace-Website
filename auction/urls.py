from django.urls import path

from . import views


app_name = 'auction'
urlpatterns = [
    # path('', views.IndeView.as_view(), name='index'),
    # path('',views.list_of_products, name='list_of_products')
    path('<int:item_id>/', views.detail, name='detail'),
    path('create/', views.create, name='create'),
    path('<int:item_id>/add_prod_to_cart/', views.add_prod_to_cart, name='add_prod_to_cart'),
    path('<int:item_id>/add_prod_to_order/', views.add_prod_to_order, name='add_prod_to_order'),
    path('<int:item_id>/restock/', views.restock, name='restock')

]
