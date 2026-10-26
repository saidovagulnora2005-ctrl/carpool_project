from django.http import HttpResponse
from .helpers import send_confirmation_email
from django.shortcuts import render, redirect
from .models import CustomUser, EmailConfirmation
from django.contrib.auth import login,authenticate


def home_view(request):
    return render(request, 'home.html')


def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not email or not password1 or not password2:
            return render(request, 'register.html', {'error': 'Заполните все обязательные поля!'})
        if password1 != password2:
            return render(request, 'register.html', {'error': "Пароли не совпадают!"})
        if CustomUser.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': 'Пользователь с такой электронной почтой уже существует!'})

        user = CustomUser.objects.create_user(email=email,password=password1)
        token = EmailConfirmation.objects.create(user=user)
        send_confirmation_email(token)
        return redirect('login')
    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password1 = request.POST.get('password1')

        if not email or not password1:
            return render(request,'login.html',context={"error": "'Заполните все обязательные поля!"})

        user = authenticate(email=email,password=password1)
        if user is None:
            return render(request,'login.html',context={"error": "Неправильная почта или пароль"})
        login(request,user)
        return redirect('home')
    return render(request,'login.html')


def confirm_email_view(request,token):
    conf_token = EmailConfirmation.objects.filter(token=token).first()
    if conf_token:
        user = CustomUser.objects.filter(id=conf_token.user.id).first()
        user.is_active = True
        user.save()
        return redirect('login')
    return HttpResponse("Код подтверждения неправильный или срок действии истек!")
