from django.shortcuts import render
from django.views import generic
from products.models import Option, Product, Size, Category
from products.forms import ContactUsForm
from django.urls import reverse_lazy
from django.db.models import Q
from django.shortcuts import redirect
# Create your views here.
class ProductListView(generic.ListView):
    model = Option
    queryset = Option.objects.filter(stock__gt = 0).order_by('-unit_price')
    context_object_name ='options'
    template_name = "products/index.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.all().order_by('-discount')
        context['products'] = products
        return context

class AllProductListView(generic.ListView):
    model = Product
    queryset = Product.objects.all()
    context_object_name = 'products'
    template_name = 'products/all-product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        context['categories'] = categories
        return context


class SearchView(generic.ListView):
    model = Product
    context_object_name = 'products'
    template_name = "products/all-product.html"
    def get_queryset(self, **kwargs):
        queryset = Product.objects.filter(Q(name__contains= self.request.GET.get('search')))
        return queryset
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         categories = Category.objects.all()
#         context['categories'] = categories
# #         return context

def category_specific(request,id):
    categories = Category.objects.all()
    products = Product.objects.filter(category = id)
    return render(request,'products/all-product.html',context = {'products':products, 'categories':categories})

class SingleProductDetailView(generic.DetailView):
    model = Product
    queryset = Product.objects.all()
    template_name = "products/single-product.html"
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        prod = kwargs.get('object')
        cat = prod.category
        same_category_products = Product.objects.filter(category = cat )
        diff_category_products = Product.objects.exclude(category = cat)
        sizes = Size.objects.all()
        context['same_category_products'] = same_category_products
        context['diff_category_products'] = diff_category_products
        context['sizes'] = sizes
        return context

# class CartView(generic.ListView)
class AboutView(generic.TemplateView):
    template_name = 'products/about.html' 

class ContactUsView(generic.FormView):
    form_class = ContactUsForm
    template_name = "products/contact-us.html"
    success_url = reverse_lazy('success')

class SuccessView(generic.TemplateView):
    template_name = "products/success-response.html"

def AddToCartView(request, id):
    print(request.GET)
    request.session['size'] = request.GET.get('size')
    request.session['qty'] = request.GET.get('qty')
    print(request.session.get('size'))
    return redirect('single-product', id)
