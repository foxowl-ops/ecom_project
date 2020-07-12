from django.shortcuts import render
from django.views import generic
from django.contrib.auth import get_user_model
from products.models import Product, Category, Cart, CIM, OIM, Item, Order
from products.forms import ContactUsForm, CommentForm
from django.urls import reverse_lazy
from django.db.models import Q
from django.shortcuts import redirect
from django.db.models import Sum
from django.conf import settings
from products.models import Comment
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
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
    paginate_by = 8

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
        print(kwargs.get('object').id)
        context['same_category_products'] = same_category_products
        context['diff_category_products'] = diff_category_products
        comments = Comment.objects.filter(product = kwargs.get('object')).order_by('-rate')
        print(comments)
        average_rating = comments.aggregate(Avg('rate'))
        print(average_rating['rate__avg'])
        context['comments'] = comments
        context['average_rating'] = average_rating.get("rate__avg")
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
        cart = request.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = request.session[settings.CART_SESSION_ID] = {}
        ID = str(id)
        quantity = request.GET.get('qty')
        if ID not in cart:
            cart[ID] = {'identity':id, "qty": quantity}
        else:
            cart[ID]['qty'] = request.GET.get('qty')
        print(cart.values())
        print(request.session.get(settings.CART_SESSION_ID))
        request.session.modified = True
        # print(request.session['cart']) #{'cart':{id:qty, id1:qty2}}
        # if id not in request.session['cart']:
        #     print(request.session['cart'])
        #     print('hey')
        #     request.session['cart'] = {int(id) : int(request.GET.get('qty'))}
        # else:
        #     print('hi')
        #     request.session['cart'].update({int(id) : int(request.GET.get('qty'))})
        # print(request.session['cart'][id])
        # # request.session.get('cart').get(id) = request.GET.get('qty')
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
        else:
            cart = request.session.get(settings.CART_SESSION_ID)
            print(cart)
            items = []
            qty = []
            price = []
            total = []
            for dic in cart.values():
                items.append(Product.objects.get(id = int(dic.get('identity'))))
                qty.append(int(dic.get('qty')))
            print(items)
            print(qty)
            for p in items:
                price.append(p.discounted_price)
            print(price)
            for num1, num2 in zip(qty,price):
                total.append(num1*num2)
            print(total)
            total_bill = sum(total)
            print(total_bill)
            # for i,t in enumerate(prices):
            #     for k,j enumerate(qty):
            #         if i == k:
            #             total.append(t*j)
            context = {"items":items, "qty":qty, "price":price, 'total':total, 'total_bill':total_bill}
            return render(request, "products/viewcart.html",context)            

class AddToOrderView(generic.View):
    def get(self, request):
        if request.user.is_authenticated:
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
        else:
            print(request.session.get(settings.CART_SESSION_ID))
            return redirect('bufferurl')
            

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

def AddCommentView(request, id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            data = Comment()  # create relation with model
            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            print(form.cleaned_data['rate'])
            data.rate = form.cleaned_data['rate']
            data.product_id=id
            current_user= request.user
            data.user_id=current_user.id
            data.save()  # save data to tables
            return redirect('single-product', id)
@login_required(login_url='login')
def BufferUrlView(request, *args, **kwargs):
    cart = request.session.get(settings.CART_SESSION_ID)
    print(cart)
    items = []
    qty = []
    price = []
    total = []
    for dic in cart.values():
        items.append(Product.objects.get(id = int(dic.get('identity'))))
        qty.append(int(dic.get('qty')))
    print(items)
    print(qty)
    for p in items:
        price.append(p.discounted_price)
    print(price)
    for num1, num2 in zip(qty,price):
        total.append(num1*num2)
    print(total)
    total_bill = sum(total)
    print(total_bill)
    cart_obj = Cart.objects.get_or_create(user = request.user)
    for p, q in zip(items,qty):
        item_obj = Item.objects.create(product = p ,quantity = q)
        cim_obj = CIM.objects.create(cart = cart_obj[0], item = item_obj)
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
