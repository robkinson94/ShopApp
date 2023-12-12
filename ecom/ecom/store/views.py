from django.shortcuts import render, redirect
from .models import Product, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django import forms

# Create your views here.
def home(request):
    products = Product.objects.all()
    category = Category.objects.all()
    return render(request, 'home.html', {'products':products, 'category':category})


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You have been logged in successfully!"))
            return redirect('home')
        else:
            messages.error(request, ("There was an error, please try again."))
            return redirect('login')
 
    return render(request, 'login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out successfully"))
    return redirect('home')


def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, email=email, password=password)
            login(request, user)
            messages.success(request, ("You have logged in successfully"))
            return redirect('home')
        else:
            messages.error(request, ("Something went wrong, please try again."))
            return redirect('register')
    else:
        return render(request, 'register.html', {'form':form})
    
    
def product(request, pk):
    product = Product.objects.get(id=pk)
    category = Category.objects.all()
    return render(request, 'product.html', {'product':product, 'category':category})


def category(request, foo):
    foo = foo.replace("-", " ")
    category = Category.objects.all()
    try:
        categories = Category.objects.get(name=foo)
        products = Product.objects.filter(category=categories)
        return render(request, 'category.html', {'products':products, 'category':category})
    except:
        messages.success(request, ("Category does not exist..."))
        return redirect('home')