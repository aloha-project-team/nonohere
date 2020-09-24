from django.shortcuts import render
from .models import StoreDB, ReviewDB
from django.db.models import Q
# Create your views here.

def home(request):
    context={}
    region_list =[]
    stores_result = []

    stores = StoreDB.objects.all()

    if request.method == "POST":
        # 지역별 분류
        region = request.POST.getlist('region[]')
        # print(region)

        if ('전체' in region) or (region == []) :
            region_list = [stores]
            context['region'] = "전체"
            # print("지역전체")
        else :
            context['region'] = region
            for reg in region:
                region_list.append(stores.filter(addcode=reg))
            # print("지역필터링") 

        # 업종별 분류
        category = request.POST.getlist('category[]')
        # print(category)

        if ('전체' in category) or (category == []) :
            # stores = StoreDB.objects.all()
            stores_result=region_list
            context['category'] = "전체"
            # print("카테고리전체")
        else:
            context['category'] = category
            for ministore in region_list:
                for cate in category:
                    stores_result.append(ministore.filter(category=cate))
            # print("카테고리필터링")

        context['store_list'] = stores_result
        # print(stores_result)

    else:
        context['region'] = '전체'
        context['category'] = '전체'
        # print("post없음")
        context['store_list'] = [stores]
    
    return render(request, 'home.html', context)

def detail(request, store_pk):
    context={}
    store = StoreDB.objects.get(pk=store_pk)
    context['store'] = store
    reviews = ReviewDB.objects.filter(store_id = store_pk)
    context['reviews'] = reviews

    return render(request, 'detail.html', context)