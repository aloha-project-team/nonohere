from django.shortcuts import render, redirect
from .models import StoreDB, ReviewDB
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
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
#################################################################
def sign_up(request):
    context = {}

    #POST Method
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password_check = request.POST['password_check']

        if (username and password and password == password_check):
            new_user = User.objects.create_user(
                username = username,
                password = password,
            )
            auth.login(request, new_user)
            return redirect('home') #로그인하면 게시물 목록으로

        else:
            context['error'] = "아이디와 비밀번호를 다시 확인해주세요."

    # GET Method
    return render(request, 'sign_up.html', context)

def login(request):
    context = {}

    #POST Method
    if request.method == "POST":
        username1 = request.POST['username']
        password1 = request.POST['password']
        if username1 and password1 :
            user = auth.authenticate(
                request,
                username = username1,
                password = password1
            )

            if user is not None:
                auth.login(request, user)
                return redirect('home')
            else:
                context['error'] = '아이디와 비밀번호를 다시 확인해주세요.'

        else:
            context['error'] = '아이디와 비밀번호를 모두 입력해주세요.'

    #GET Method
    return render(request, 'login.html', context)

def logout(request):
    if request.method == "POST":
        auth.logout(request)

    return redirect("home")

@login_required
def like(request, store_id):

    if request.method == 'POST':
        try:
            store = StoreDB.objects.get(id=store_id)

            if request.user in store.liked_users.all():
                store.liked_users.remove(request.user)
            else:
                store.liked_users.add(request.user)

            return redirect('detail', store.id)
        
        except StoreDB.DoesNotExist:
            pass

    return redirect('home')
