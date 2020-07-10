from django.shortcuts import render
from django.views import generic
from django.contrib.auth import get_user_model
from products.models import Product, Category, Cart, CIM, OIM, Item, Order
from products.forms import ContactUsForm
from django.urls import reverse_lazy
from django.db.models import Q
from django.shortcuts import redirect
from django.db.models import Sum
# Create your views here.
class ProductListView(generic.ListView):
    model = Product
    products = Product.objects.all().order_by('-discount')
    context_object_name ='products'
    template_name = "products/index.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        context['categories'] = categories
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
        context['same_category_products'] = same_category_products
        context['diff_category_products'] = diff_category_products
        return context

class AboutView(generic.TemplateView):
    template_name = 'products/about.html' 

class ContactUsView(generic.FormView):
    form_class = ContactUsForm
    template_name = "products/contact-us.html"
    success_url = reverse_lazy('success')

class SuccessView(generic.TemplateView):
    template_name = "products/success-response.html"

def AddToCartView(request, id):
    if not request.user.is_authenticated:
        print(request.GET)
        request.session['cart'] = {id : request.GET.get('qty')}
        request.session['cart'] = {id : request.GET.get('qty')}
        return redirect('single-product', id)
    else:
        product = Product.objects.get(id = id)
        cart_obj = Cart.objects.get_or_create(user = request.user)
        # if cart_obj:
        #     print(cart_obj)
        #     item_obj = Item.objects.create(product = product, quantity = request.GET.get('qty'))
        #     cim_obj = CIM.objects.create(cart = cart_obj, item = item_obj)
        # else:
        #     cart_obj = Cart.objects.create(user = request.user)
        #     print(cart_obj)
        item_obj = Item.objects.create(product = product ,quantity = request.GET.get('qty'))
        cim_obj = CIM.objects.create(cart = cart_obj[0], item = item_obj)
        return redirect('single-product', id)

class CartView(generic.View):
    def get(self, request):
        if request.user.is_authenticated:
            cart_id = Cart.objects.get(user = request.user)
            cims = CIM.objects.filter(cart = cart_id)
            context = {'cims':cims}
            total_price = cims.aggregate(total =Sum('total'))
            total_bill = total_price.get('total')
            print(total_bill)
            context['total_bill'] = total_bill
            return render(request, 'products/viewcart.html', context )

class AddToOrderView(generic.View):
    def get(self, request):
        cart_id = Cart.objects.get(user = request.user)
        cims = CIM.objects.filter(cart = cart_id)
        total_price = cims.aggregate(total =Sum('total'))
        total_bill = total_price.get('total')
        order = Order.objects.create(user=request.user, total_bill = total_bill)
        context = {'order':order}
        for cim in cims:
            oim = OIM.objects.create(order=order, item = cim.item)
        cims.delete()
        return render(request, 'products/order-placed.html', context)

class OrderView(generic.View):
    def get(self,request, *args, **kwargs):
        orders = Order.objects.filter(user_id = kwargs['id'])
        context = {'orders':orders}
        return render(request, "products/order-details.html", context)
    
class OrderItemView(generic.View):
    def get(self, request,id, *args, **kwargs):
        print(id)
        oims = OIM.objects.filter(order_id = id)
        print(oims)
        context = {'oims':oims}
        return render(request, "products/order-items.html" , context)