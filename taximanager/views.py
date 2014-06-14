#!/usr/bin/python2.4
# -*- coding: utf-8 -*-

from taximanager.models import Ride, Status, Driver, Cab
from django.shortcuts import render, get_object_or_404,render_to_response

from django.contrib.auth.decorators import login_required

from django.contrib import auth

from  taximanager.forms import ContactForm, RideForm, ViewRideForm

from django.conf import settings

from django.core.mail import send_mail

from django.http import HttpResponseRedirect

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/login/")












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
            send_mail('Taxi manager', 'Status is: '+ new_ride.status.name , settings.EMAIL_HOST_USER,
                      [new_ride.email], fail_silently=False)
            new_ride.pay=round(6*round(float(new_ride.calculatedDistance),1),1)
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

        new_ride.pay=round(6*round(float(new_ride.calculatedDistance),1),1)




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
