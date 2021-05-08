from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import ListView, FormView, View, DeleteView, TemplateView
from django.urls import reverse, reverse_lazy
from .models import Room, Booking, RoomCategory, Person
from .forms import AvailabilityForm, PersonForm
from .utils import check_availability
from .utils import find_total_room_charge
# from .utils import get_random_person_name_email
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
import uuid

# Create your views here.

class BookingFormView(LoginRequiredMixin, FormView):
    form_class = AvailabilityForm
    template_name ='roomapp/booking_form.html'
    success_url = reverse_lazy('roomapp:CheckoutView')


    def get_initial(self, *args, **kwargs):
        base_initial = self.initial.copy()
        print(self.request.session.items())
        if self.request.session.get('check_in', False):
            base_initial['check_in'] = self.request.session.get('check_in')
            base_initial['check_out'] = self.request.session.get('check_out')
            base_initial['adults'] = self.request.session.get('adults')
            base_initial['children'] = self.request.session.get('children')
            base_initial['room_category'] = self.request.session.get('room_category')
        return base_initial
    

    def form_valid(self, form, *args, **kwargs):
        data = form.cleaned_data
        self.request.session['check_in'] = data['check_in'].strftime("%Y-%m-%d")
        self.request.session['check_out'] = data['check_out'].strftime("%Y-%m-%d")
        self.request.session['adults'] = data['adults']
        self.request.session['children'] = data['children']
        self.request.session['room_category'] = data['room_category'].category
        amount = find_total_room_charge(data['check_in'], data['check_out'], data['room_category'])
        self.request.session['amount'] = amount
        # self.request.session.modified = True
        return FormView.form_valid(self, form)


class CheckoutView(LoginRequiredMixin, FormView):
    form_class = PersonForm
    template_name='roomapp/checkout.html'
    success_url = reverse_lazy('roomapp:success_view')


    # def post(self, request, *args, **kwargs):
    #     # person_name, person_email = get_random_person_name_email()

    #     person = Person.objects.create(
    #         name=person_name,
    #         email=person_email
    #     )
    #     person.save()
    #     context = {
    #         'person': person,
    #         'checkout_id': uuid.uuid4,
    #         'amount': request.session['amount'],
    #         'room_image': '',
    #         'room_name': request.session['room_category'],
    #         'amount': request.session['amount'],
    #         'check_in': request.session['check_in'],
    #         'check_out': request.session['check_out'],
    #     }
    #     print('chkout_context = ', context)

    #         return render(request, 'roomapp/checkout_confirm.html', context)
    #     except Exception as e:
    #         print('failed , ', request.session)
    #         return render(request, 'roomapp/failure.html', {'error': e})

    def form_valid(self, form, *args, **kwargs):
        person = form.save()
        self.request.session['person'] = person.pk
        self.request.session['checkout_id'] = str(uuid.uuid4)
        context = {
            'person': person,
            'checkout_id': str(uuid.uuid4),
            'amount': self.request.session['amount'],
            'room_name': self.request.session['room_category'],
            'amount': self.request.session['amount'],
            'check_in': self.request.session['check_in'],
            'check_out': self.request.session['check_out'],
        }

        print('chkout_context = ', context)

        return render(self.request, 'roomapp/checkout_confirm.html', context)
        # return FormView.form_valid(self, form)

class CheckoutConfirmView(LoginRequiredMixin, TemplateView):
    templte_name = 'roomapp/checkout_confirm.html'

    def post(self,*args,**kwargs):
        data = {"user":self.request.user,
                "name":Person.objects.get(pk=self.request.session['person']).name,
                "room_category":RoomCategory.objects.get(category=self.request.session['room_category']),
                "check_in":self.request.session['check_in'],
                "check_out":self.request.session['check_out'],
                "amount":self.request.session['amount'],
                }
        Booking.objects.create(**data)
        # context = super().get_context_data(**kwargs)
        # print(context)
        return redirect(reverse('roomapp:success_view'))


class RoomListView(LoginRequiredMixin, ListView):
    model = Room
    template_name = "roomapp/room_list_view.html"


class BookingListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = "roomapp/booking_list_view.html"

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            booking_list = Booking.objects.all()
            return booking_list
        else:
            booking_list = Booking.objects.filter(user=self.request.user)
            return booking_list

    # def get_context_data(self, **kwargs):
    #     room = Room.objects.all()[0]
    #     room_categories = dict(room.ROOM_CATEGORIES)
    #     context = super().get_context_data(**kwargs)
    #     context


class RoomDetailView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        print(self.request.user)
        category = self.kwargs.get('category', None)
        form = AvailabilityForm()
        room_list = Room.objects.filter(category=category)

        if len(room_list) > 0:
            room = room_list[0]
            room_category = dict(room.ROOM_CATEGORIES).get(room.category, None)
            context = {
                'room_category': room_category,
                'form': form,
            }
            return render(request, 'roomapp/room_detail_view.html', context)
        else:
            return HttpResponse('Category does not exist')

    def post(self, request, *args, **kwargs):
        category = self.kwargs.get('category', None)
        room_list = Room.objects.filter(category=category)
        form = AvailabilityForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

        available_rooms = []
        for room in room_list:
            if check_availability(room, data['check_in'], data['check_out']):
                available_rooms.append(room)

        if len(available_rooms) > 0:
            room = available_rooms[0]

            booking = Booking.objects.create(
                user=self.request.user,
                room=room,
                check_in=data['check_in'],
                check_out=data['check_out']
            )
            booking.save()
            message = Mail(
                from_email='dhabaledarshan@gmail.com',
                to_emails='dhabalekalpana@gmail.com',
                subject='Sending from hotelina',
                html_content='<strong>Sending from hotelina</strong>')
            # try:
            #     sg = SendGridAPIClient(env.str('SG_KEY'))
            #     response = sg.send(message)
            #     print(response.status_code)
            #     print(response.body)
            #     print(response.headers)
            #     print('SENT!!!')
            # except Exception as e:
            #     print(e)
            return HttpResponse(booking)
        else:
            return HttpResponse('All of this category of rooms are booked!! Try another one')


class CancelBookingView(LoginRequiredMixin, DeleteView):
    model = Booking
    template_name = 'roomapp/booking_cancel_view.html'
    success_url = reverse_lazy('roomapp:BookingListView')



class SuccessView(LoginRequiredMixin, TemplateView):
    template_name =  'roomapp/success.html'


class CancelView(LoginRequiredMixin, TemplateView):
    template_name =   'roomapp/cancel.html'


class ContactUsView(LoginRequiredMixin, TemplateView):
    template_name =  'roomapp/contact_us.html'
