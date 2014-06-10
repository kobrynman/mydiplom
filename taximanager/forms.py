from django import forms
from taximanager.models import Ride, Status, Driver
from django.forms import Textarea, DateField

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField()
    sender = forms.EmailField()





class RideForm(forms.ModelForm):
    ETA = forms.CharField(widget=forms.HiddenInput())
    calculatedDistance = forms.CharField(widget=forms.HiddenInput())
    pickupLatitude = forms.FloatField(widget=forms.HiddenInput())
    pickupLongitude = forms.FloatField(widget=forms.HiddenInput())
    dropOffLatitude = forms.FloatField(widget=forms.HiddenInput())
    dropOffLongitude = forms.FloatField(widget=forms.HiddenInput())
    class Meta:
        model = Ride
        exclude = ('loginID','status')

class ViewRideForm(forms.ModelForm):
    ETA = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    calculatedDistance = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    pickupLatitude = forms.FloatField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    pickupLongitude = forms.FloatField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    dropOffLatitude = forms.FloatField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    dropOffLongitude = forms.FloatField(widget=forms.TextInput(attrs={'readonly':'readonly'}))


    class Meta:
        model = Ride
        widgets = {

            'cabID': forms.Select(attrs={'readonly':'readonly'}),
        }