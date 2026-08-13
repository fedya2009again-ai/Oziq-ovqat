from django.shortcuts import render, get_object_or_404
from .models import Recipe
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
import random

def home(request):
    recipes = Recipe.objects.all()
    context = {
        'recipes': recipes
    }
    return render(request, 'main/home.html', context)


def search(request):
    query = request.GET.get('q', '').strip()
    recipes = Recipe.objects.all()

    if query:
        recipes = recipes.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(ingredients__icontains=query) |
            Q(category__icontains=query)
        )
    else:
        recipes = recipes.none()

    context = {
        'recipes': recipes,
        'search_query': query,
        'is_search': True,
    }
    return render(request, 'main/home.html', context)

def random_recipe(request):
    recipes = list(Recipe.objects.all())

    if recipes:
        recipe = random.choice(recipes)
        return redirect('recipe_detail', recipe_id=recipe.id)

    return redirect('home')


def category(request, category_name):
    recipes = Recipe.objects.filter(category=category_name)
    context = {
        'recipes': recipes,
        'category_name': category_name
    }
    return render(request, 'main/home.html', context)


def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    context = {
        'recipe': recipe
    }
    return render(request, 'main/recipe_detail.html', context)


def about(request):
    return render(request, 'main/about.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            messages.error(request, "Parollar bir xil emas!")
            return render(request, 'main/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Bu username allaqachon mavjud!")
            return render(request, 'main/register.html')

        user = User.objects.create_user(
            username=username,
            password=password
        )

        login(request, user)

        return redirect('home')

    return render(request, 'main/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Username va password ni tekshirish
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Foydalanuvchini tizimga kiritish
            login(request, user)
            # Home sahifasiga redirect qilish
            return redirect('home')
        else:
            # Xatolik xabarini qo'shish
            messages.error(request, 'Username yoki parol noto\'g\'ri!')
            return render(request, 'main/login.html')

    return render(request, 'main/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, "Tizimdan muvaffaqiyatli chiqdingiz!")
    return redirect('home')