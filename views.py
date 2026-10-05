# File: views.py
# Author: Niyoo Nedi (nnedi@bu.edu), 4/20/2026
# Description: Views for room reservation app

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Building, Room, Booking
from .forms import BookingForm
from django.utils import timezone
from django.core.exceptions import ValidationError


def home(request):
    '''Show home page'''

    #render the main template (shared layout / landing page)
    return render(request, "project/home.html")


def building_list(request):
    '''Show all buildings'''

    #fetch every building row from the database
    buildings = Building.objects.all()
    #pass them to the template under the name "buildings"      
    return render(request, "project/build-list.html", {"buildings": buildings})


def room_list(request):
    '''Show all rooms'''

    #fetch every room so the template can list them all
    rooms = Room.objects.all()

    #get the values of the GET parameters
    building = request.GET.get("building")
    #get the value of the mic_count parameter
    mic_count = request.GET.get("mic_count")
    #get the value of the projector parameter
    projector = request.GET.get("projector")
    #get the value of the opening_time parameter
    opening_time = request.GET.get("opening_time")
    #get the value of the closing_time parameter
    closing_time = request.GET.get("closing_time")

    #filter the rooms by the building parameter
    if building:
        rooms = rooms.filter(building__abr_name__icontains=building)
    #filter the rooms by the mic_count parameter
    if mic_count:
        rooms = rooms.filter(mic_count__gte=mic_count)
    #filter the rooms by the projector parameter
    if projector == "yes":
        rooms = rooms.filter(projector=True)
    elif projector == "no":
        rooms = rooms.filter(projector=False)
    #filter the rooms by the opening_time parameter
    if opening_time:
        rooms = rooms.filter(building__opening_time__lte=opening_time)
    #filter the rooms by the closing_time parameter
    if closing_time:
        rooms = rooms.filter(building__closing_time__gte=closing_time)
    #render the room-list template with the filtered rooms
    return render(request, "project/room-list.html", {"rooms": rooms})


def booking_list(request):
    '''show bookings'''

    #load bookings and order by start time so they appear chronologically, and only keep the ones that haven't ended
    bookings = Booking.objects.filter(end_time__gte=timezone.now()).order_by("start_time")

    #get the values of the GET parameters
    building = request.GET.get("building")
    #get the value of the room parameter
    room = request.GET.get("room")
    #get the value of the date parameter
    date = request.GET.get("date")
    #filter the bookings by the building parameter
    if building:
        bookings = bookings.filter(building__abr_name__icontains=building)
    #filter the bookings by the room parameter
    if room:
        bookings = bookings.filter(room__room_num=room)
    #filter the bookings by the date parameter
    if date:
        bookings = bookings.filter(start_time__date=date)
    #render the booking_list template with the bookings
    return render(request, "project/booking_list.html", {"bookings": bookings,})


@login_required
def create_booking(request):
    '''Allow a logged-in user to reserve a room'''

    #if the method is POST, create a new booking
    if request.method == "POST":
        form = BookingForm(request.POST)

        #if the form is valid, create a new booking
        if form.is_valid():
            #save the booking without committing it to the database
            booking = form.save(commit=False)
            #set the user to the current user
            booking.user = request.user
            #set the building to the building of the room
            booking.building = booking.room.building

            try:
                #save the booking to the database
                booking.save()
                return redirect("booking_list")
            #if the booking is not valid, add an error to the form
            except ValidationError as e:
                form.add_error(None, e)
    #if the method is GET, create a new form
    else:
        form = BookingForm()
    #render the booking_form template with the form
    return render(request, "project/booking_form.html", {"form": form})
    