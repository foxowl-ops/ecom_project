from django.shortcuts import render
from django.views import generic
from products.models import Option, Product
# Create your views here.
class ProductListView(generic.ListView):
    model = Option
    queryset = Option.objects.filter(stock__gt = 0).order_by('-unit_price')
    context_object_name ='options'
    template_name = "products/index.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.all()
        context['products'] = products
        return context

class AllProductListView(generic.ListView):
    model = Product
    queryset = Product.objects.all()
    context_object_name = 'products'
    template_name = 'products/all-product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        options = Option.objects.filter(bottle_size__size = '250 ML')
        context['options'] = options
        return context

class SingleProductDetailView(generic.DetailView):
    model = Product
    queryset = Product.objects.all()
    template_name = "products/single-product.html"
    pk_url_kwarg = 'id'

    # def  get_context_data(self,**kwargs):
    #     context = super().get_context_data(**kwargs)
    #     options = Option.objects.filt
    #     context['options'] = options
    #     return context

