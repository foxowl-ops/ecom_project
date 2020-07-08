from django.urls import path
from products.views import ProductListView,AllProductListView, SingleProductDetailView, AboutView, ContactUsView, SuccessView, SearchView, category_specific, AddToCartView, CartView

urlpatterns = [
    path('', ProductListView.as_view(), name='home'),
    path('all',AllProductListView.as_view(), name='all-products'),
    path('product/<int:id>', SingleProductDetailView.as_view(), name='single-product'),
    path('about', AboutView.as_view(), name='about'),
    path('contact',ContactUsView.as_view(), name='contact'),
    path('success', SuccessView.as_view(), name='success'),
    path('url', SearchView.as_view(), name='search_page'),
    path('category_based/<int:id>', category_specific, name='category_specific'),
    path('addtocart/<int:id>', AddToCartView, name='add-to-cart'),
    path('mycart', CartView.as_view() , name='mycart')
]
