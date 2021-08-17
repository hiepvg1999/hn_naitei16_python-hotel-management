from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Room, Booking, RoomImage, User
from .forms import NewUserForm, EditRoomForm, UserForm
from datetime import datetime, date, timedelta
import random
from hotel.utils import constant

def user_register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
    else:
        form = NewUserForm()
    return render (request=request, template_name="registration/register.html", context={"form":form})

def index(request):
    return render (request=request, template_name="index.html")

# @login_required(login_url='login')
# room function (add, edit, filter)
def rooms(request):
    rooms = Room.objects.all()
    check_in = None
    check_out = None
    room_arr = []
    def check_valid(start_date, end_date):
        availableRooms = []
        for room in rooms:
            availList = []
            bookingList = Booking.objects.filter(room_id= room)
            for booking in bookingList:
                if booking.start_date > end_date.date() or booking.end_date < start_date.date():
                    availList.append(True)
                else:
                    availList.append(False)
            if all(availList):
                availableRooms.append(room)
        return availableRooms

    if request.method == 'POST':
        data = request.POST
        if 'dateFilter' in request.POST:
            check_in = data.get("fd", "")
            check_out = data.get("ld", "")
            try:
                check_in = datetime.strptime(check_in, constant.DATE_FORMAT)
                check_out = datetime.strptime(check_out, constant.DATE_FORMAT)
            except ValueError:
                raise ValueError("Incorrect data format, should be YYYY-MM-DD")
            rooms = check_valid(check_in, check_out)
        if "filter" in request.POST:
            if data.get('id') != '':
                rooms = rooms.filter(id=data.get('id'))
            if data.get('capacity') != '':
                rooms = rooms.filter(capacity__gte=data.get('capacity'))
            if data.get('nob') != '':
                rooms = rooms.filter(numberOfBeds__gte= data.get('nob'))
            if data.get('type') != '':
                rooms = rooms.filter(roomType__contains= data.get('type'))
            if data.get('price') != '':
                rooms = rooms.filter(room_price__lte= data.get('price'))
            context = {
                "rooms": room_arr,
                "id": data.get("id"),
                "capacity": data.get("capacity"),
                "nob": data.get("nob"),
                "price": data.get("price"),
                "type": data.get("type")
            }
            return render(request, 'room/rooms.html',context)
    context = {
        "rooms": rooms,
        "fd": check_in,
        "ld": check_out
    }
    return render(request, 'room/rooms.html', context)

# @login_required(login_url='login')
def room_profile(request, number):
    tempRoom = Room.objects.get(id=number)
    img_urls = RoomImage.objects.filter(room_id= number)
    bookings = Booking.objects.filter(room_id= tempRoom)
    context = {
        "bookings": bookings,
        "room": tempRoom,
        "img_urls": img_urls
    }

    return render(request,"room/room-profile.html", context)

@login_required(login_url='login')
@permission_required('hotel.can_edit', raise_exception=True)
def room_edit(request, number):
    room = Room.objects.get(id= number)
    form = EditRoomForm(instance=room)
    room_types = Room.ROOM_TYPES
    type_arr = []
    for type in room_types:
        type_arr.append(type[0])
    context = {
        "room": room,
        "form": form,
        "room_types": type_arr
    }

    if request.method == 'POST':
        form = EditRoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect("room-profile", number = room.id)
    return render(request, "room/room-edit.html", context)

@login_required(login_url='login')
@permission_required('hotel.can_add', raise_exception=True)
def room_add(request):
    room_types = Room.ROOM_TYPES
    type_arr = []
    for type in room_types:
        type_arr.append(type[0])
    message= ''
    if request.method == 'POST':
        data = request.POST
        capacity = data.get('capacity')
        numberOfBeds = data.get('beds')
        roomType = data.get('roomType')
        room_price = data.get('price')
        if int(capacity) < 1 or int(numberOfBeds) < 1 or float(room_price) <= 0 or capacity.isdigit() is False or numberOfBeds.isdigit() is False:
            message = 'Add room fail'
        else:
            new_room = Room(capacity= capacity, numberOfBeds= numberOfBeds, roomType= roomType, room_price= room_price)
            new_room.save()
            return redirect('rooms')
    context = {'message': message, 'room_types': type_arr}
    return render(request,'room/room-add.html',context)

# booking functions (make booking, list booking)

def make_booking(request):
    pass

def list_booking(request):
    pass

# user profile
class UserProfileView(LoginRequiredMixin, generic.DetailView):
    model = User
    template_name = 'user/user-profile.html'
    
    def get_object(self):
        return self.request.user

@login_required(login_url='login')
def edit_profile(request):
    if request.method == 'POST':
        form = UserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("user-profile")
    else:
        form = UserForm(instance=request.user)
    return render(request, 'user/edit-profile.html', {'form': form})
