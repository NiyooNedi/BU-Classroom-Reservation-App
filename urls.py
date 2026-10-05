# File: urls.py
# Author: Niyoo Nedi (nnedi@bu.edu), 4/20/2026
# Description: File that will contain the urls for the final project

from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("buildings/", views.building_list, name="build_list"),
    path("rooms/", views.room_list, name="room_list"),
    path("bookings/", views.booking_list, name="booking_list"),
    path("reserve/", views.create_booking, name="create_booking"),
]