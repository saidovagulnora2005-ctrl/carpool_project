from django.http import HttpResponse
from .helpers import send_confirmation_email
from django.shortcuts import render, redirect,get_object_or_404
from .models import CustomUser, EmailConfirmation,Trip, CompanionRequest
from django.contrib.auth import login,authenticate
from django.contrib.auth.decorators import login_required
from .forms import TripForm, CompanionRequestForm


def home_view(request):
    trips = Trip.objects.filter(seats_available__gt=0).order_by('date')

    if request.GET.get('start_location'):
        trips = trips.filter(start_location__icontains=request.GET.get('start_location'))
    if request.GET.get('end_location'):
        trips = trips.filter(end_location__icontains=request.GET.get('end_location'))
    if request.GET.get('date'):
        trips = trips.filter(date__date=request.GET.get('date'))

    return render(request, 'home.html', {'trips': trips})


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
    return HttpResponse("Код подтверждения неправильный!")


def trip_list_view(request):
    trips = Trip.objects.all()

    start_location = request.GET.get('start_location', '')
    end_location = request.GET.get('end_location', '')
    trip_date = request.GET.get('date', '')

    if start_location:
        trips = trips.filter(start_location__icontains=start_location)
    if end_location:
        trips = trips.filter(end_location__icontains=end_location)
    if trip_date:
        trips = trips.filter(date__date=trip_date)

    return render(request, 'trip_list.html', {'trips': trips,'start_location': start_location,'end_location': end_location,'trip_date': trip_date})


@login_required
def trip_create_view(request):
    if request.method == 'POST':
        form = TripForm(request.POST)
        if form.is_valid():
            trip = form.save(commit=False)
            trip.user = request.user
            trip.save()
            return redirect('trip_list')
    else:
        form = TripForm()
    return render(request, 'trip_create.html')


@login_required
def trip_update_view(request, pk):
    trip = get_object_or_404(Trip, id=pk, user=request.user)
    if request.method == 'POST':
        form = TripForm(request.POST, instance=trip)
        if form.is_valid():
            form.save()
            return redirect('trip_list')
    else:
        form = TripForm(instance=trip)
    return render(request, 'trip_update.html')


@login_required
def trip_delete_view(request, pk):
    trip = get_object_or_404(Trip, id=pk, user=request.user)
    if request.method == 'POST':
        trip.delete()
        return redirect('trip_list')
    return render(request, 'trip_delete.html', {'trip': trip})


def companion_request_list_view(request):
    requests = CompanionRequest.objects.select_related('user').order_by('date')
    return render(request, 'companion_request_list.html', {'requests': requests,})


@login_required
def companion_request_create_view(request):
    form = CompanionRequestForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        companion_request = form.save(commit=False)
        companion_request.user = request.user
        companion_request.save()
        return redirect('companion_request_list')
    return render(request, 'companion_request_create.html')
