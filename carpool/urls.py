from django.urls import path
from .views import *

urlpatterns = [
    path('', register_view, name='register_view'),
    path('home/', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('confirm/<str:token>/',confirm_email_view,name='confirm_email'),
]
