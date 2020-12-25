from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.core.mail import send_mail
from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views.decorators.cache import cache_control
from .models import Product_details, product_category, add_to_cart, bill
from .forms import *

dic = {}

# Create your views here.
all_object = []


@cache_control(no_store=True, must_revalidate=True, no_cache=True)
def index(request):
    username = request.POST.get("username")
    password = request.POST.get("pass")
    user = auth.authenticate(username=username, password=password)
    print(user)
    if request.method == 'POST':
        if user is not None:
            auth.login(request, user)
            return redirect("home")
        else:
            # messages.info(request, 'invalid credentials')
            invalid="Username or Password is invalid"
            return render(request, 'index.html',{'invalid':invalid})
    else:
        return render(request, 'index.html')


@cache_control(no_store=True, must_revalidate=True, no_cache=True)
def register(request):
    if request.method == 'POST':
        username = request.POST.get("name")
        password = request.POST.get("password")
        re_password = request.POST.get("re_password")
        if password == re_password:
            if User.objects.filter(username=username).exists():
                exist="user is already exists"
                return render(request,'register.html',{'exist':exist})
            else:
                user = User.objects.create_user(username=username, password=password)
                user.save()
                return render(request, 'index.html')
        else:
            exist='password does not match'
            return render(request, 'register.html', {'exist': exist})

    return render(request, 'register.html')


@login_required(login_url='index')
@cache_control(no_store=True, must_revalidate=True, no_cache=True)
def checkout(request):
    username=request.user.username
    bill_object =bill.objects.get(username=username)
    return render(request, 'checkout.html',{'bill':bill_object})


@login_required(login_url='index')
@cache_control(no_store=True, must_revalidate=True, no_cache=True)
def feedback(request):
    return render(request, 'feedback.html')


@login_required(login_url='index')
@cache_control(no_store=True, must_revalidate=True, no_cache=True)
def home(request):
    category = product_category.objects.all()
    search = request.GET.get('search')
    if search:
        category_obj = Product_details.objects.filter(product_name=search).first()
        if category_obj is not None:
            c = category_obj.category_name
            return redirect('/shop/' + c)

    return render(request, 'home.html', {'category': category})


@login_required(login_url='index')
@cache_control(no_store=True, must_revalidate=True, no_cache=True)
def shop(request, category_name):
    search = request.GET.get('search')
    if search:
        category_obj = Product_details.objects.filter(product_name=search).first()
        if category_obj is not None:
            c = category_obj.category_name
            return redirect('/shop/' + c)
    request.session['category'] = category_name

    category_obj=product_category.objects.get.all()
    pd = Product_details.objects.filter(category_name=category_name)

    return render(request, 'shop1.html', {'pd': pd})


@login_required(login_url='index')
@cache_control(no_store=True, must_revalidate=True, no_cache=True)
def cart(request, id):
    id = int(id)
    usr = request.user.username
    product = Product_details.objects.get(id=id)
    category_name = request.session['category']
    st = []
    product_in_cart = add_to_cart.objects.filter(id=id)

    if product.quantity > 0:
        product.quantity = product.quantity - 1
        product.save()
        if not product_in_cart:
            insert_in_table = add_to_cart(id=id, username=usr, product_name=product.product_name, quantity=1)
            insert_in_table.save()

        else:
            add_to_cart.objects.filter(id=id).update(quantity=F('quantity') + 1)
    else:
        st.append('stock is not avilable for ' + product.product_name)
        return render(request, 'stock_unavailable.html', {'st': st})

    return redirect('/shop/' + category_name)


@login_required(login_url='index')
@cache_control(no_store=True, must_revalidate=True, no_cache=True)
def show_cart(request):
    search = request.GET.get('search')
    if search:
        category_obj = Product_details.objects.filter(product_name=search).first()
        if category_obj is not None:
            c = category_obj.category_name
            return redirect('/shop/' + c)


    user = request.user.username
    b = add_to_cart.objects.filter(username=user)
    a = []
    total_price = 0
    for i in b:
        if i.quantity > 0:
            a.append(i)
    d = []
    e = []
    for i in a:
        product = Product_details.objects.get(id=i.id)
        d.append(product)
        product_price = product.product_price * i.quantity
        total_price = total_price + product_price

    bill_object = bill.objects.filter(username=user)

    if not bill_object:
        p=bill(username=user,total_bill=total_price)
        p.save()
    else:
        bill.objects.filter(username=user).update(total_bill=total_price)

    return render(request, 'cart.html', {'data': zip(d, a), 'total_price': total_price})


@login_required(login_url='index')
@cache_control(no_store=True, must_revalidate=True, no_cache=True)
def update_cart_quantity(request):
    if request.method == 'POST':
        user = request.user.username
        a = add_to_cart.objects.filter(username=user)
        no_more_quantity = []

        for i in a:
            if i.quantity > 0:
                quantity_before_update = i.quantity
                id = str(i.id)
                req_param = str(request.POST.get(id))

                quantity_after_update = int(req_param)
                delta = quantity_after_update - quantity_before_update
                product = Product_details.objects.get(id=i.id)
                q_in_product=product.quantity
                if product.quantity >= delta:

                    Product_details.objects.filter(id=i.id).update(quantity=F('quantity') - delta)
                    add_to_cart.objects.filter(id=i.id).update(quantity=quantity_after_update)

                    cart_object_after_update = add_to_cart.objects.filter(id=i.id, quantity=0)

                    if cart_object_after_update is not None:
                        cart_object_after_update.delete()
                else:
                    add_to_cart.objects.filter(id=i.id).update(quantity=quantity_before_update+q_in_product)
                    no_more_quantity.append('stock is not available for ' + product.product_name)

        request.session['stock_is_not_available'] = no_more_quantity
        if 'stock_is_not_available' in request.session:
            for e in request.session['stock_is_not_available']:
                print('e bjbkj igiukj =========================================================',e)
        return redirect('/show_cart')
    else:
        return redirect('/show_cart')


@login_required(login_url='index')
@cache_control(no_store=True, must_revalidate=True, no_cache=True)
def logout(request):
    logout1 = 'you are successfully logout'
    auth.logout(request)
    messages.info(request,logout1)
    return render(request, 'index.html', {'logout': logout1})


def email(request):
    user = request.user.username
    message = 'your first mail'


    email = request.POST['email']
    # message = get_template('register.html').render(ctx)


    subject = 'Subscription of DRP grocerry store'
    html_message = render_to_string('mail_template.html', {'context': 'values'})
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = email
    try:
        send_mail(subject,
                  plain_message,
                  from_email,
                  [to],
                  html_message=html_message)
        c="thank you for subscribing our Grocery Store"
        return render(request, 'thank.html',{'c':c})
    except Exception as e:
        return HttpResponse('something error while sending mail')

@login_required(login_url='index')
@cache_control(no_store=True, must_revalidate=True, no_cache=True)
def product_category_view(request):
    if request.method == 'POST':
        form = product_categoryForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = product_category()

    return render(request, 'category.html', {'form': form})

@login_required(login_url='index')
@cache_control(no_store=True, must_revalidate=True, no_cache=True)
def success(request):
    return render(request,'success.html')

@login_required(login_url='index')
@cache_control(no_store=True, must_revalidate=True, no_cache=True)
def Product_details_view(request):
    category_ob=product_category.objects.all()
    if request.method == 'POST':
        form = product_detailsForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = Product_details()
    return render(request, 'add_product1.html', {'form': form,'category':category_ob})


def thankyou(request):
    user = request.user.username
    usr=User.objects.get(username=user)
    email=usr.email
    bill_ob=bill.objects.get(username=user)
    subject = 'Order Placed'
    c = "thank you for Shopping"
    html_message = render_to_string('mail_template.html', {'bill': bill_ob,'c':c})

    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = email
    try:
        send_mail(subject,
                  plain_message,
                  from_email,
                  [to],
                  html_message=html_message)
        c = "thank you for Shopping"
        return render(request, 'thank.html', {'c': c})
    except Exception as e:
        return HttpResponse('something error while sending mail')





