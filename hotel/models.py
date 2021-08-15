from django.db import models
from django.contrib.auth.models import User,AbstractUser
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
import uuid
from phonenumber_field.modelfields import PhoneNumberField

class User(AbstractUser):
    phoneNumber = PhoneNumberField(unique=True)
    USERNAME_FIELD = 'email'
    email = models.EmailField(_('email address'), unique=True)
    REQUIRED_FIELDS = ['username','phoneNumber']
    def __str__(self):
        return f'{self.username}'

class Room(models.Model):
    ROOM_TYPES = (
        ('King', 'King'),
        ('Luxury', 'Luxury'),
        ('Normal', 'Normal'),
        ('Economic', 'Economic'),

    )
    capacity = models.SmallIntegerField()
    numberOfBeds = models.SmallIntegerField()
    roomType = models.CharField(max_length=20, choices=ROOM_TYPES)
    room_price = models.FloatField()
    description = models.TextField(max_length=100)

    def __str__(self):
        return str(self.room_id)

class Booking(models.Model):
    STATUS_TYPE = (
        ('waiting','waiting'),
        ('approved', 'approved'),
        ('cancelled', 'cancelled'),
        ('rejected','rejected'),
    )
    booking_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
        help_text='Unique ID for this particular booking')
    user = models.ForeignKey(User, null= True, on_delete=models.RESTRICT) # user_id
    room_id = models.ForeignKey(Room, null= True, on_delete=models.RESTRICT) # room_id
    dateOfReservation = models.DateField(default=timezone.now)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices= STATUS_TYPE)
    room_price = models.FloatField()

    def __str__(self):
        return str(self.user)+ 'is booking '+ str(self.room_id)+ 'at ' +str(self.start_date)

class Bill(models.Model):
    bill_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
        help_text='Unique ID for this particular bill')
    booking_id = models.ForeignKey(Booking, null= True, on_delete=models.CASCADE)
    totalAmount = models.FloatField()
    summary = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.summary) + " " + str(self.totalAmount)

class RoomImage(models.Model):
    room_id = models.ForeignKey(Room, null= True, on_delete=models.CASCADE)
    img_url = models.CharField(max_length=50,null=True)

    def __str__(self):
        return str(self.img_url)

class Service(models.Model):
    service_name = models.CharField(max_length=20)
    service_price = models.FloatField()
    description = models.TextField()

    def __str__(self):
        return str(self.description)

class RoomService(models.Model):
    booking_id= models.ForeignKey(Booking, null= True, on_delete=models.CASCADE)
    service_id= models.ForeignKey(Service, null= True, on_delete=models.RESTRICT)
    service_price = models.FloatField()

    def __str__(self):
        return str(self.service_price)

class Review(models.Model):
    review_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
        help_text='Unique ID for this particular review')
    user = models.ForeignKey(User, null= True, on_delete=models.CASCADE)
    date = models.DateField()
    content = models.CharField(max_length=100)

    def __str__(self):
        return str(self.content)
