from django.test import TestCase
from django.urls import reverse
from django.test import Client
from hotel.models import User, Room, RoomImage, Bill, Booking, Service, RoomService
import datetime

class RoomViewTest(TestCase):
    def setUp(self):
        test_user1 = User.objects.create_user(email= 'test1@gmail.com', username= 'test_user1', phoneNumber= '+84399695122')
        test_user1.set_password('abcxyz123')
        test_user2 = User.objects.create_user(email= 'test2@gmail.com', username= 'test_user2', phoneNumber= '+84399695123')
        test_user2.set_password('abcxyz123')
        admin_user = User.objects.create_superuser(email= 'admin@gmail.com', username= 'admin_user1', phoneNumber= '+84399695125')
        admin_user.set_password('123abc456')
        room = Room.objects.create(capacity= 2, numberOfBeds= 2, roomType= 'Luxury', room_price= 450.0, description= 'Luxury room')
        start_date = datetime.date.today() + datetime.timedelta(days= 2)
        end_date = datetime.date.today() + datetime.timedelta(days= 5)
        booking = Booking.objects.create(user= test_user1, room_id= room, start_date= start_date, end_date= end_date, status= 'approved', room_price= 450.0)
        test_user1.save()
        test_user2.save()
        admin_user.save()
        room.save()
        booking.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('rooms'))
        self.assertEqual(response.status_code, 200)

    def test_forbidden_if_logged_in_but_not_correct_permission(self):
        self.client.force_login(User.objects.get_or_create(email='test1@gmail.com')[0])
        response = self.client.post(reverse('room-add'),{'capacity' : 2, 'beds': 2, 'roomType': 'Normal', 'price': 200.0})
        self.assertEqual(response.status_code, 403)

    def test_add_room_admin(self):
        self.client.force_login(User.objects.get_or_create(email='admin@gmail.com')[0])
        response = self.client.post(reverse('room-add'),{'capacity' : 1, 'beds': 1, 'roomType': 'Normal', 'price': 200.0})
        self.assertEqual(response.status_code, 302)

    def test_edit_room_admin(self):
        room_id =Room.objects.get(numberOfBeds=2)
        address = '/room-edit/'+ str(room_id)
        self.client.force_login(User.objects.get_or_create(email='admin@gmail.com')[0])
        response = self.client.post(address,{'capacity' : 3, 'numberOfBeds': 2, 'room_price': 200.0, 'roomType': 'Normal'})
        self.assertEqual(response.status_code, 302)

    def test_len_list_users_admin(self):
        self.client.force_login(User.objects.get_or_create(email='admin@gmail.com')[0])
        response = self.client.get(reverse('list-users'),{'search': 'test1'})
        users = User.objects.filter(email__icontains= 'test1')
        self.assertEqual(len(response.context['user_search']), len(users))

    def test_booking_successful(self):
        room_id = Room.objects.first()
        address = '/room-profile/'+ str(room_id)
        self.client.force_login(User.objects.get_or_create(email='admin@gmail.com')[0])
        fd = datetime.date.today() + datetime.timedelta(days= 6)
        ld = datetime.date.today() + datetime.timedelta(days= 8)
        response = self.client.post(address,{'make-booking': 'make-booking','fd': fd, 'ld': ld})
        messages = list(response.context['messages'])
        self.assertEqual(len(response.context['bookings']),2)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(messages[0]),'Success')

    def test_booking_fail_booked(self):
        room_id = Room.objects.first()
        address = '/room-profile/'+ str(room_id)
        self.client.force_login(User.objects.get_or_create(email='admin@gmail.com')[0])
        fd = datetime.date.today() + datetime.timedelta(days= 3)
        ld = datetime.date.today() + datetime.timedelta(days= 4)
        response = self.client.post(address,{'make-booking': 'make-booking','fd': fd, 'ld': ld})
        messages = list(response.context['messages'])
        self.assertEqual(len(response.context['bookings']),1)
        self.assertEqual(str(messages[0]),'Start date has been booked')

    def test_booking_fail_start_date_gt_end_date(self):
        room_id = Room.objects.first()
        address = '/room-profile/'+ str(room_id)
        self.client.force_login(User.objects.get_or_create(email='admin@gmail.com')[0])
        fd = datetime.date.today() + datetime.timedelta(days= 10)
        ld = datetime.date.today() + datetime.timedelta(days= 9)
        response = self.client.post(address,{'make-booking': 'make-booking','fd': fd, 'ld': ld})
        messages = list(response.context['messages'])
        self.assertEqual(len(response.context['bookings']),1)
        self.assertEqual(str(messages[0]),'End date >= Start date')

    def test_booking_fail_start_date_and_end_date_gt_now(self):
        room_id = Room.objects.first()
        address = '/room-profile/'+ str(room_id)
        self.client.force_login(User.objects.get_or_create(email='admin@gmail.com')[0])
        fd = datetime.date.today() + datetime.timedelta(days= -2)
        ld = datetime.date.today() + datetime.timedelta(days= -1)
        response = self.client.post(address,{'make-booking': 'make-booking','fd': fd, 'ld': ld})
        messages = list(response.context['messages'])
        self.assertEqual(len(response.context['bookings']),1)
        self.assertEqual(str(messages[0]),'Start date and End date >= now')
