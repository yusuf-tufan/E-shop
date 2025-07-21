from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import datetime
import json
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect


def registerPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            return render(request, 'tufshopapp/register.html', {'error': 'Passwords do not match.'})

        if User.objects.filter(username=username).exists():
            return render(request, 'tufshopapp/register.html', {'error': 'Username already taken.'})

        user = User.objects.create_user(username=username, email=email, password=password1)

        Customer.objects.create(user=user, name=username, email=email)

        return redirect('login')

    return render(request, 'tufshopapp/register.html')


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  
        else:
            return render(request, 'tufshopapp/login.html', {'error': 'Username or password is incorrect!'})

    return render(request, 'tufshopapp/login.html')

def logoutUser(request):
    logout(request)
    return redirect('home')

def home(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created = Order.objects.get_or_create(customer=customer,complete=False)
        items= order.orderitem_set.all()
        cartItems=order.get_cart_items()
    else:
        items =[]
        order={'get_cart_total': 0,'get_cart_items': 0,'shipping':False}
        cartItems = order['get_cart_items']
    products=Product.objects.all()
    context={'products':products,'cartItems':cartItems}
    return render(request,'tufshopapp/home.html',context)

def cart(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created = Order.objects.get_or_create(customer=customer,complete=False)
        items= order.orderitem_set.all()
        cartItems=order.get_cart_items()
    else:
        items =[]
        order={'get_cart_total': 0,'get_cart_items': 0,'shipping':False}
        cartItems = order['get_cart_items']
    context={'items':items,'order':order,'cartItems':cartItems}
    return render(request,'tufshopapp/cart.html',context)



def checkout(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created = Order.objects.get_or_create(customer=customer,complete=False)
        items= order.orderitem_set.all()
        cartItems=order.get_cart_items()
    else:
        items =[]
        order={'get_cart_total': 0,'get_cart_items': 0,'shipping':False}
        cartItems = order['get_cart_items']
    context={'items':items,'order':order,'cartItems':cartItems}
    return render(request,'tufshopapp/checkout.html',context)




from django.http import HttpResponse

def updateItem(request):
    if not request.user.is_authenticated:
        return HttpResponse("Giriş yapmalısınız", status=401)
    
    data=json.loads(request.body)
    productId=data['productId']
    action=data['action']

    print('Action',action)
    print('ProductId',productId)
    
    
    customer=request.user.customer
    product = Product.objects.get(id=productId)
    order,created = Order.objects.get_or_create(customer=customer,complete=False)

    orderItem,created=OrderItem.objects.get_or_create(order=order,product=product)


    if action=='add':
        orderItem.quantity=(orderItem.quantity+1)

    elif action=='remove':
        orderItem.quantity=(orderItem.quantity-1)  

    orderItem.save()
    if orderItem.quantity<=0:
        orderItem.delete()
    return JsonResponse('Item was added',safe=False)

#from django.views.decorators.csrf import csrf_exempt
#@csrf_exempt
def processOrder(request):
    transaction_id=datetime.datetime.now().timestamp()
    data =json.loads(request.body)

    if request.user.is_authenticated:
        customer=request.user.customer
        order,created = Order.objects.get_or_create(customer=customer,complete=False)
        total =float(data['form']['total'])
        order.transaction_id=transaction_id

        if total==float(order.get_cart_total):
            order.complete=True
        order.save()

        if order.shipping==True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address =data['shipping']['address'],
                city =data['shipping']['city'],
                state =data['shipping']['state'],
            )

    else:
        print('User is not logged in')


    return JsonResponse('Payment completed',safe=False)

