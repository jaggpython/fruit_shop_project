from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from django.db.models import Q  # For complex queries
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required

def increase_quantity(request, id):
    cart = request.session.get('cart', {})
    product_id = str(id)

    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1

    request.session['cart'] = cart
    return redirect('cart')


def decrease_quantity(request, id):
    cart = request.session.get('cart', {})
    product_id = str(id)

    if product_id in cart:
        if cart[product_id] > 1:
            cart[product_id] -= 1
        else:
            del cart[product_id]  # remove item if quantity becomes 0

    request.session['cart'] = cart
    return redirect('cart')

@login_required
def settings_view(request):
    if not request.user.is_superuser:
        messages.error(request, "Unauthorized access.")
        return redirect('product_list')

    products = Product.objects.all().order_by('-id')

    if request.method == "POST":
        Product.objects.create(
            name=request.POST.get('name'),
            price=request.POST.get('price'),
            description=request.POST.get('description'),
            image=request.FILES.get('image')
        )
        messages.success(request, "Product added successfully!")
        return redirect('settings')

    return render(request, 'products/settings.html', {'products': products})


@login_required
def update_product(request, id):
    if not request.user.is_superuser:
        messages.error(request, "Unauthorized access.")
        return redirect('product_list')

    product = get_object_or_404(Product, id=id)

    if request.method == "POST":
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.description = request.POST.get('description')

        if request.FILES.get('image'):
            product.image = request.FILES.get('image')

        product.save()
        messages.success(request, "Product updated successfully!")
        return redirect('settings')

    return render(request, 'products/update_product.html', {'product': product})


@login_required
def delete_product(request, id):
    if not request.user.is_superuser:
        messages.error(request, "Unauthorized access.")
        return redirect('product_list')

    product = get_object_or_404(Product, id=id)

    if request.method == "POST":
        product.delete()
        messages.success(request, "Product deleted successfully!")
        return redirect('settings')

    return render(request, 'products/delete_product.html', {'product': product})



# SIGNUP VIEW
def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Check if passwords match
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('signup')

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('signup')

        # Create new user
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        messages.success(request, "Account created successfully! Please login.")
        return redirect('login')

    return render(request, 'products/signup.html')

# LOGIN VIEW
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome, {user.username}!")
            return redirect('product_list')  # redirect to homepage
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'products/login.html')

# LOGOUT VIEW
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('login')

def product_list(request):
    query = request.GET.get('q', '')
    product_qs = Product.objects.all().order_by('-id')

    if query:
        product_qs = product_qs.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    paginator = Paginator(product_qs, 8)  # 🔴 use SMALL number for testing
    page_number = request.GET.get('page')

    products = paginator.get_page(page_number)

    return render(request, 'products/product_list.html', {
        'products': products,
        'query': query
    })



def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'products/product_detail.html', {'product': product})


def add_to_cart(request, id):
    cart = request.session.get('cart', {})
    cart[str(id)] = cart.get(str(id), 0) + 1
    request.session['cart'] = cart
    return redirect('cart')


def cart(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0

    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        subtotal = product.price * quantity
        total += subtotal
        items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

    return render(request, 'products/cart.html', {'items': items, 'total': total})


def remove_from_cart(request, id):
    cart = request.session.get('cart', {})
    product_id = str(id)
    if product_id in cart:
        del cart[product_id]
        request.session['cart'] = cart
    return redirect('cart')
