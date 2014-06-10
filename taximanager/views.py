#!/usr/bin/python2.4
# -*- coding: utf-8 -*-
from taximanager.models import Ride, Status, Driver, Cab
from django.shortcuts import render, get_object_or_404,render_to_response
from django.contrib import auth

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from django.views import generic

from django.utils import timezone
from django.contrib import auth


from  taximanager.forms import ContactForm, RideForm, ViewRideForm


from django.conf import settings

from django.core.mail import send_mail


def base(request):
    return HttpResponse("base!")






from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/ridelist/")
    else:
        form = UserCreationForm()
    return render_to_response("registration/register.html", {'form': form,})










def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/login/")




#test views
class Test1(generic.ListView):
    model = Ride
    template_name = 'taximanager/test1.html'
    def get_context_data(self, **kwargs):
        context = super(Test1, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

def Test2(request):
    # return render_to_response('geolocation/new_ride.html', RequestContext(request))
    driver = Driver.objects.all()
    cab = Cab.objects.all()
    if request.method == 'GET':
        context = {'user':'33', 'driver':driver, 'cab':cab}
        return render(request,'taximanager/new_ride.html', context)
    elif request.method == 'POST':
        form = RideForm(request.POST)
        if form.is_valid():
            new_ride = form.save(commit=False)
            new_ride.LoginID = request.user
            new_ride.save()
            return render(request, 'taximanager/ridelist.html', '')
        else:
            context = {'user':'33', 'driver':driver, 'cab':cab}
            return render(request,'taximanager/new_ride.html', context)

def test_bootstrap(request):
    ride_list = Ride.objects.all().order_by('-pickupAddress')[:5]
    context = {'ride_list': ride_list}
    return render(request, 'taximanager/test_bootstrap.html', context)

def bootstrap(request):
    ride_list = Ride.objects.all().order_by('-pickupAddress')[:5]
    context = {'ride_list': ride_list}
    return render(request, 'taximanager/bootstrap.html', context)

from django.contrib.auth.models import Group


@login_required
def rideList(request):

    users_in_group = Group.objects.get(name="admin").user_set.all()
    isflag = False
    for user in users_in_group:
        if user== request.user:
            isflag=True

    if isflag:
        ride_list = Ride.objects.all()[:100]
    else:
        ride_list = Ride.objects.filter(loginID = request.user )[:100]




    status = Status.objects.all()


    context = {'ride_list': ride_list,  'status': status}
    return render(request, 'taximanager/ride_list.html', context)

@login_required
def taximanager(request):
    return render(request, 'registration.html', "")


@login_required
def newRide(request):

    driver = Driver.objects.all()
    cab = Cab.objects.all()
    status = Status.objects.all()
    defaultStatus = Status.objects.get(name='Accepted')
    if request.method == 'POST':
        form = RideForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            new_ride = form.save(commit=False)
            new_ride.loginID = request.user
            new_ride.status=defaultStatus



            send_mail('Taxi manager', 'Status is:'+ new_ride.status.name , settings.EMAIL_HOST_USER,
                      [new_ride.email], fail_silently=False)

         
            new_ride.pay=round(6*round(float(new_ride.calculatedDistance)/1000,1),0)






            new_ride.save()
            return HttpResponseRedirect('/ridelist/')
    else:
        form=RideForm()

    context = { 'driver':driver, 'cab':cab, 'status':status, 'form':form}
    return render(request, 'taximanager/new_ride.html', context)



def changeRide(request, ride_id):
    instance = get_object_or_404(Ride, pk=ride_id)

    form = RideForm(request.POST or None, instance=instance)
    if form.is_valid():
        new_ride = form.save(commit=False)


        new_ride.pay=round(6*round(float(new_ride.calculatedDistance)/1000,1),0)




        form.save()
        return HttpResponseRedirect('/ridelist/')
    return render(request, 'taximanager/changeRide.html', {'form':form})





@login_required
def selectRide(request, ride_id):

    ride = get_object_or_404(Ride, pk=ride_id)
    form= ViewRideForm(initial={
        'pickupAddress':ride.pickupAddress,
        'dropOffAddress':ride.dropOffAddress,
        'ETA':ride.ETA,
        'calculatedDistance':ride.calculatedDistance,
        'pickupLatitude':ride.pickupLatitude,
        'pickupLongitude':ride.pickupLongitude,
        'dropOffLatitude':ride.dropOffLatitude,
        'dropOffLongitude':ride.dropOffLongitude,
        'email':ride.email,
        'pay':ride.pay,
        'status':ride.status,
        'driverID':ride.loginID,
        'cabID':ride.cabID,
        'loginID':ride.loginID,
        'notes':ride.notes,
    })
    return render(request, 'taximanager/select_ride.html', {'ride': ride, 'form':form})



@login_required
def changeStatus(request, ride_id):

    ride = get_object_or_404(Ride, pk=ride_id)
    send_mail('Taxi manager', 'Status is:'+ ride.status.name , settings.EMAIL_HOST_USER,
                      [ride.email], fail_silently=False)
    try:
        newStatus = Status.objects.get(id = request.POST['status'])
        ride.status=newStatus

        ride.save()
    except (KeyError, Status.DoesNotExist):

        return render(request, 'polls/detal.html', {
            'error_message': "You didn't select a choice.",
        })
    return HttpResponseRedirect('/ridelist/')

@login_required
def about(request):
    return render(request, 'taximanager/about.html', "")


@login_required
def drivers(request):
    drivers = Driver.objects.all()
    cabs = Cab.objects.all()
    context = {'drivers': drivers,'cabs':cabs}
    return render(request, 'taximanager/drivers.html', context)

@login_required
def changeStatusDriver(request, driver_id):

    driver = get_object_or_404(Driver, pk=driver_id)

    if request.POST.get('isActive', False):
        cab = Cab.objects.get(id = request.POST['cab'])
        cab.isActive=True
        driver.isActive = True
        driver.cabID = cab

    else:
        cab = Cab.objects.get(id = request.POST['cab'])
        cab.isActive=False

        driver.isActive=False
        driver.cabID = None



    driver.save()
    cab.save()

    return HttpResponseRedirect('/drivers/')







def testPostForm(request):
    errors = []
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            errors.append('Enter request')
        elif len(q) > 20:
            errors.append('the limit entered symbols are less 20')
        else:
            return render_to_response('taximanager/testPostSelect.html', {'query': q})
    return render_to_response('taximanager/testPostForm.html', {'errors': errors})

#/////////////////////////////////////////////////////////////////////////////
def contact(request):
    errors = []
    if request.method == 'POST':
        if not request.POST.get('subject', ''):
            errors.append('Enter theme')
        if not request.POST.get('message', ''):
            errors.append('Enter message')
        if request.POST.get('e-mail') and '@' not in request.P0ST['e-mail' ]:
            errors.append('Enter correct email address')
        if not errors:
            send_mail(
                request.P0ST['subject'],
                request.P0ST['message'],
                request.POST.get('e-mail', 'noreply@example.com'),['siteowner@example.com'],
            )
        return HttpResponseRedirect('/send/')
    return render_to_response('taximanager/contact_form.html', {'errors': errors})

def send(request):
    return render_to_response('taximanager/send.html')

#////////////////////////////////////////////////////////////////
@login_required
def table(request):
    ride_list = Ride.objects.all().order_by('-pickupAddress')[:5]
    context = {'ride_list': ride_list}
    return render(request, 'taximanager/table.html', context)


def test3(request):
    if request.method == 'POST': # If the form has been submitted...

        form = ContactForm(request.POST) # A form bound to the POST data

        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            return HttpResponseRedirect('/thanks/') # Redirect after POST
    else:
        form = ContactForm() # An unbound form

    return render(request, 'taximanager/test3.html', {'form': form,})








