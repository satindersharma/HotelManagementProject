from django.db import models
from django.conf import settings
from django.urls import reverse
from django.contrib.auth import get_user_model
USER = get_user_model()


class RoomCategory(models.Model):
    category = models.CharField(max_length=50)
    rate = models.FloatField()

    def __str__(self):
        return self.category


class Room(models.Model):
    number = models.IntegerField()
    beds = models.IntegerField()
    capacity = models.IntegerField()
    category = models.ForeignKey(
        RoomCategory, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'Room No = {self.number} | Beds = {self.beds} | People = {self.capacity}'


class Booking(models.Model):
    PAYMENT_STATUSES = (
        ('INC', 'PAYMENT_INCOMPLETE'),
        ('PAR', 'PAYMENT_PARTIALLY_COMPLETE'),
        ('COM', 'PAYMENT_COMPLETE'),
    )
    name = models.CharField(max_length=100)
    user = models.ForeignKey(USER,
                             on_delete=models.CASCADE)
    # room = models.ForeignKey(Room, on_delete=models.CASCADE)
    room_category = models.ForeignKey(RoomCategory, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    payment_status = models.CharField(max_length=3, choices=PAYMENT_STATUSES,default=PAYMENT_STATUSES[0][0])
    amount = models.IntegerField()
    def __str__(self):
        return f'From = {self.check_in.strftime("%d-%b-%Y %H:%M")} To = {self.check_out.strftime("%d-%b-%Y %H:%M")}'

    def get_cancel_booking_url(self):
        return reverse('roomapp:CancelBookingView', kwargs={'pk': self.pk})

# Hola im darshan


class Person(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
