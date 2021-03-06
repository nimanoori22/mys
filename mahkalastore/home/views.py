from django.shortcuts import render, HttpResponse, HttpResponsePermanentRedirect
from product.models import Product, Category, Images, Comment
from home.models import Setting, ContactForm, ContactMessage
from .forms import SearchForm
from django.contrib import messages
from django.http import HttpResponseRedirect
import json
# Create your views here.

def index(request):
    page = "home"
    category  = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    products_slider = Product.objects.all().order_by('id')[:4] #first 4 products
    products_latest= Product.objects.all().order_by('-id')[:4] #last 4 products
    products_picked = Product.objects.all().order_by('?')[:4] #randomly picked

    context = {'setting': setting, 
    'page': page,
    'products_slider': products_slider,
    'products_latest': products_latest,
    'products_picked': products_picked,
    'category': category}
    return render(request, 'index.html', context=context)

def aboutus(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting}
    return render(request, 'about.html', context=context)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactMessage()
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, 'your message has been sent, thank you <3')
            HttpResponseRedirect('/contact')
    setting = Setting.objects.get(pk=1)
    form = ContactForm
    context = {'setting': setting, 'form': form,}
    return render(request, 'contact.html', context=context)


def category_product(request, id, slug):
    category = Category.objects.all()
    products = Product.objects.filter(category_id=id)
    context = {
        'products': products,
        'category': category,
    }
    return render(request, 'category_product.html', context=context)

def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            catid = form.cleaned_data['catid']
            if catid == 0:
                products = Product.objects.filter(name__icontains=query)
            else:
                products = Product.objects.filter(name__icontains=query, category_id=catid)

            category = Category.objects.all()
            context = {
                'products': products,
                'query': query,
                'category': category,
            }
            return render(request, 'search_products.html', context=context)

    return HttpResponsePermanentRedirect('/')

def search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        products = Product.objects.filter(name__icontains=q)

        results = []
        for rs in products:
            product_json = {}
            product_json = rs.name
            results.append(product_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def product_detail(request, id, slug):
    category = Category.objects.all()
    product = Product.objects.get(pk=id)
    images = Images.objects.filter(product_id=id)
    comments = Comment.objects.filter(product_id=id, status='True')
    context = {
        'product': product,
        'category': category,
        'mypics': images,
        'comments': comments,
    }
    return render(request, 'product_detail.html', context=context)
