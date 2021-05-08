from django.urls import path
from .views import BookingListView, RoomDetailView, CancelBookingView, CheckoutView, CheckoutConfirmView, SuccessView, CancelView, BookingFormView, ContactUsView, RoomListView
app_name = 'roomapp'

urlpatterns = [
    path('book/', BookingFormView.as_view(), name='BookingFormView'),
    path('booking_list/', BookingListView.as_view(), name='BookingListView'),
    path('room_list/', RoomListView, name='RoomListView'),
    path('room/<category>', RoomDetailView.as_view(), name='RoomDetailView'),
    path('booking/cancel/<pk>', CancelBookingView.as_view(),
         name='CancelBookingView'),
    path('checkout/', CheckoutView.as_view(), name='CheckoutView'),
    path('checkout_confirm/', CheckoutConfirmView.as_view(), name='CheckoutConfirmView'),
    path('success/', SuccessView.as_view(), name='success_view'),
    path('cancel/', CancelView.as_view(), name='cancel_view'),
    path('contact-us/', ContactUsView.as_view(), name="contact_us")

]
