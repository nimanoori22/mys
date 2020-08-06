from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from .models import CommentForm, Comment
from django.contrib import messages

# Create your views here.

def productindex(request):
    return HttpResponse('hello')

def addcomment(request, id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            data = Comment()
            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.rate = form.cleaned_data['rate']
            data.ip = request.META.get('REMOTE_ADDR')
            data.product_id = id
            current_user = request.user
            data.user_id = current_user.id
            data.save()
            messages.success(request, 'your review has been sent, thank you <3')
            HttpResponseRedirect(url)

    return HttpResponseRedirect(url)
