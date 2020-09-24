from django.shortcuts import render
from .models import StoreDB, ReviewDB
# Create your views here.

def home(request):
    context={}
    if request.method == "POST":
        region = request.POST['region']
        context['region'] = region

        if region == '전체':
            stores = StoreDB.objects.all()
        else:
            stores = StoreDB.objects.filter(addcode=region)

        category = request.POST['category']
        context['category'] = category

        if category != '전체':
            stores = stores.filter(category=category)
    else:
        stores = StoreDB.objects.all()
        context['region'] = '전체'
        context['category'] = '전체'

    context['stores'] = stores

    return render(request, 'home.html', context)

def detail(request, store_pk):
    context={}
    store = StoreDB.objects.get(pk=store_pk)
    context['store'] = store
    reviews = ReviewDB.objects.filter(store_id = store_pk)
    context['reviews'] = reviews

    return render(request, 'detail.html', context)