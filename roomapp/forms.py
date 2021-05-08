from django import forms
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from .models import RoomCategory, Person

#  input_formats=["%Y-%m-%dT%H:%M", ],


class AvailabilityForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        # remove ':' in labels of form
        kwargs.setdefault('label_suffix', '')
        super(AvailabilityForm, self).__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({'class': 'form-control'})


    # CATEGORY_CHOICES = [(x.category, x.category)
    #                     for x in RoomCategory.objects.all()]

    check_in = forms.DateField(required=True,initial=datetime.now())
    check_out = forms.DateField(required=True,initial=(datetime.now()+timedelta(days=1)))
    room_category = forms.ModelChoiceField(queryset=RoomCategory.objects.all(), empty_label="Select Room Category", required=True)
    adults = forms.IntegerField(min_value=1,required=True,initial=1)
    children = forms.IntegerField(min_value=0,initial=0)


    def check_working_hours(self, start, end):
        check_in = self.cleaned_data.get('check_in')
        check_out = self.cleaned_data.get('check_out')
        # This ensures that check_in and check_out are between start and end of your working hours.
        if not(check_in < start and check_out < end):
            raise ValidationError(
                "Times beyond working hours, please enter value within working hours")
        else:
            return self.cleaned_data


class PersonForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # remove ':' in labels of form
        kwargs.setdefault('label_suffix', '')
        super(PersonForm, self).__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({'class': 'form-control'})
    class Meta:
        model = Person
        fields = '__all__'
