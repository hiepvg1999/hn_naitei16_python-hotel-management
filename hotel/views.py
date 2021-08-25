from django.db.models import query
from django.db.models import Q
from django.db.models.query import Prefetch
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.utils.translation import ugettext_lazy as _
from .models import Room, Booking, RoomImage, User, Bill
from .forms import NewUserForm, EditRoomForm, UserForm
from hotel.utils import constants, comfunc
from datetime import datetime, date, timedelta
import random
import io, base64
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
    return render (request=request, template_name="home.html")

# @login_required
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
                check_in = datetime.strptime(check_in, constants.DATE_FORMAT)
                check_out = datetime.strptime(check_out, constants.DATE_FORMAT)
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

# @login_required
def room_profile(request, number):
    room = Room.objects.filter(id = number).prefetch_related("roomimage_set").first()
    bookings = Booking.objects.filter(room_id= room)
    if request.user.id is not None:
        guest = User.objects.filter(id = request.user.id).first()
        checked = 1
        if request.method == 'POST':
            if "make-booking" in request.POST:
                data = request.POST
                user = guest
                room_id = room
                date = datetime.now()
                start_date = data.get("fd")
                end_date = data.get("ld")
                status = Booking.STATUS_TYPE[0][0]
                room_price = room.room_price
                for booking in bookings:
                    if comfunc.validate_date(request, booking.start_date, booking.end_date, start_date, end_date) == False:
                        checked = 0
                        break
                if(checked == 1):
                    new_booking = Booking(user = user, room_id = room_id, reservation_date = date, \
                        start_date= start_date, end_date= end_date, status= status, room_price= room_price)
                    new_booking.save()
                    messages.success(request, _("Success"))
                    context = {
                        "bookings": Booking.objects.filter(room_id= room),
                        "room": room,
                    }
                    return render(request,"room/room-profile.html", context)
    context = {
        "bookings": bookings,
        "room": room,
    }
    return render(request,"room/room-profile.html", context)

@login_required
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

@login_required
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

# user profile
class UserProfileView(LoginRequiredMixin, generic.DetailView):
    model = User
    template_name = 'user/user-profile.html'

    def get_object(self):
        return self.request.user

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("user-profile")
    else:
        form = UserForm(instance=request.user)
    return render(request, 'user/edit-profile.html', {'form': form})

@login_required
def list_users(request):
    users = User.objects.all()
    if request.method == 'GET':
        user_search = request.GET.get('search' or None)
        if user_search is not None:
            user_search = user_search.strip()
            if user_search != '':
                user_s = User.objects.filter(Q(email__icontains= user_search) | Q(phoneNumber__icontains= user_search)).first()
                context = {'user_search': user_s, 'search_str': user_search}
            else:
                context = {'users': users}
        else:
            context = {'users': users}
        return render(request,'user/list-users.html',context)

@login_required
@permission_required('hotel.staff_booking_list', raise_exception=True)
def list_bookings_staff(request):
    bookings = Booking.objects.filter(status = constants.WAITING)
    if request.method == "GET": 
        data_g = request.GET
        room = data_g.get('room')
        user = data_g.get('user')
        if 'filter' in data_g:
            if room == '' and user == '':
                tmp = bookings
            elif room != '' and user == '':
                tmp = bookings.filter(room_id = room)
            elif user != '' and room == '':
                tmp = bookings.filter(user__username__icontains = user)
            else:
                tmp = bookings.filter(Q(room_id = room), Q(user__username__icontains = user))
            context = {
                "bookings": tmp,
                "room_id": room,
                "username": user
            }
            return render(request, 'user/staff-list-bookings.html', context)
    elif request.method == "POST":
        data_p = request.POST
        booking_id = data_p.get('booking')
        if 'accept' in data_p:
            bookings.filter(pk = booking_id).update(status = constants.APPROVED)
        if 'decline' in data_p:
            bookings.filter(pk = booking_id).update(status = constants.REJECTED)
    bookings = Booking.objects.filter(status = constants.WAITING)
    context = {
        "bookings": bookings
    }
    return render(request, 'user/staff-list-bookings.html', context)

@login_required
@permission_required('hotel.statistic_page', raise_exception=True)
def statistic_page(request):
    # user
    users_len = len(User.objects.filter(Q(is_active=True)))

    # room
    rooms_len = Room.objects.count()

    # total
    bills = Bill.objects.select_related('booking_id')
    total = comfunc.get_total_all_bill(bills)

    # function handle filter status from list booking
    def filter_by_status(i_list, i_status):
        return [item for item in i_list if item.status == i_status]

    # create bar plot for booking
    # booking
    bookings = list(Booking.objects.all())
    approved_bookings_len = len(filter_by_status(bookings, constants.APPROVED))
    waiting_bookings_len = len(filter_by_status(bookings, constants.WAITING))
    cancelled_booking_len = len(filter_by_status(bookings, constants.CANCEL))
    rejected_booking_len = len(filter_by_status(bookings, constants.REJECTED))

    bookings_keys = [constants.APPROVED, constants.CANCEL, constants.WAITING, constants.REJECTED]
    bookings_values = [approved_bookings_len, cancelled_booking_len, waiting_bookings_len, rejected_booking_len]

    chart = comfunc.build_chart(bookings_keys, bookings_values)

    # context
    context = {'users_len': users_len, 'chart': chart, 'total': total, 'rooms_len': rooms_len}

    return render(request, 'statistic/staff_statistic_page.html', context)
