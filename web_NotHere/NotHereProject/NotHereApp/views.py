from django.shortcuts import render
from .models import StoreDB, ReviewDB
# Create your views here.

def home(request):
    context={}
    stores_list =[]
    stores_result = []

    stores = StoreDB.objects.all()

    if request.method == "POST":
        # 지역별 분류
        region = request.POST.getlist('region[]')
        print(region)
        # context['region'] = region

        if ('전체' in region) or (region == []) :
            store_list = stores
            print("지역전체")
        else :
            for reg in region:
                stores_list.append(stores.filter(addcode=reg))
            print("지역필터링") 

        # 업종별 분류
        category = request.POST.getlist('category[]')
        print(category)
        # context['category'] = category

        if ('전체' in category) or (category == []) :
            # stores = StoreDB.objects.all()
            print("카테고리전체")
        else:
            for ministore in stores_list:
                for cate in category:
                    stores_result.append(ministore.filter(category=cate))
            print("카테고리필터링")

        context['stores'] = stores_result
        print(stores_result)

    else:
        # context['region'] = '전체'
        # context['category'] = '전체'
        print("post없음")
        context['stores'] = stores
    
    return render(request, 'home.html', context)

def detail(request, store_pk):
    context={}
    store = StoreDB.objects.get(pk=store_pk)
    context['store'] = store
    reviews = ReviewDB.objects.filter(store_id = store_pk)
    context['reviews'] = reviews

    return render(request, 'detail.html', context)