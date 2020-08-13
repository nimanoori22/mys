from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from product.models import Category
# Create your views here.

def index(request):
    return HttpResponse('user')

def login_form(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return HttpResponseRedirect('/')
        else:
            messages.warning(request,"Login Error !! Username or Password is incorrect")
            return HttpResponseRedirect('/login')
    # Return an 'invalid login' error message.

    category = Category.objects.all()
    context = {
        'category': category
        }
    return render(request, 'login_form.html',context)


def signup_form(request):
    return HttpResponse('signup')

def logout_func(request):
    logout(request)
    return HttpResponseRedirect('/')
    