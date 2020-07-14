from django.shortcuts import render, HttpResponse, HttpResponsePermanentRedirect
from product.models import Product, Category
from .forms import SearchForm
# Create your views here.


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
                products = Product.objects.filter(title__incontains=query)
            else:
                products = Product.objects.filter(title__incontains=query, category_id=catid)

            category = Category.objects.all()
            context = {
                'product': products,
                'query': query,
                'category': category,
            }
            return render(request, 'search_products.html', context=context)

    return HttpResponsePermanentRedirect('/')
