from django.urls import path
from .views import *

urlpatterns = [
    path('', register_view, name='register_view'),
    path('home/', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('confirm/<str:token>/',confirm_email_view,name='confirm_email'),
    path('tripslist/', trip_list_view, name='trip_list'),
    path('createtrip/', trip_create_view, name='trip_create'),
    path('edittrips/<int:pk>/', trip_update_view, name='trip_update'),
    path('deletetrips/<int:pk>/', trip_delete_view, name='trip_delete'),
    path('companionrequests/',companion_request_list_view,name='companion_request_list'),
    path('companionrequests/create/',companion_request_create_view,name='companion_request_create'),
]
