from django.urls import path
from products.views import ProductListView,AllProductListView, SingleProductDetailView

urlpatterns = [
    path('', ProductListView.as_view()),
    path('all',AllProductListView.as_view()),
    path('all/<int:id>', SingleProductDetailView.as_view())
]
