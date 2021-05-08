import datetime
from .models import Room, Booking, RoomCategory


def check_availability(room, check_in, check_out):
    avail_list = []
    booking_list = Booking.objects.filter(room=room)
    for booking in booking_list:
        if booking.check_in > check_out or booking.check_out < check_in:
            avail_list.append(True)
        else:
            avail_list.append(False)
    return all(avail_list)



def find_total_room_charge(check_in, check_out, category):
    days = check_out-check_in
    room_category = RoomCategory.objects.get(category=category)
    total = days.days * room_category.rate
    return total
