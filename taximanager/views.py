#!/usr/bin/python2.4
# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import auth
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from taximanager.forms import ContactForm, RideForm, ViewRideForm
from taximanager.models import Ride, Status, Driver, Cab


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/login/")


@login_required
def ride_list(request):
    users_in_group = Group.objects.get(name="admin").user_set.all()
    is_flag = False
    for user in users_in_group:
        if user == request.user:
            is_flag = True
    if is_flag:
        ride_list_all = Ride.objects.all()[:100]
    else:
        ride_list_all = Ride.objects.filter(loginID=request.user)[:100]
    status = Status.objects.all()
    context = {'ride_list': ride_list_all,  'status': status}
    return render(request, 'taximanager/ride_list.html', context)


@login_required
def new_ride(request):
    driver = Driver.objects.all()
    cab = Cab.objects.all()
    status = Status.objects.all()
    default_status = Status.objects.get(name='Accepted')
    if request.method == 'POST':
        form = RideForm(request.POST)   # A form bound to the POST data
        if form.is_valid():     # All validation rules pass
            new_ride = form.save(commit=False)
            new_ride.loginID = request.user
            new_ride.status=default_status
            send_mail('Taxi manager', 'Status is: ' + new_ride.status.name, settings.EMAIL_HOST_USER,
                      [new_ride.email], fail_silently=False)
            new_ride.pay=round(6*round(float(new_ride.calculatedDistance), 1), 1)
            new_ride.save()
            return HttpResponseRedirect('/ridelist/')
    else:
        form = RideForm()
    context = {'driver':driver, 'cab': cab, 'status': status, 'form': form}
    return render(request, 'taximanager/new_ride.html', context)


@login_required
def change_ride(request, ride_id):
    instance = get_object_or_404(Ride, pk=ride_id)
    form = RideForm(request.POST or None, instance=instance)
    if form.is_valid():
        new_ride = form.save(commit=False)
        new_ride.pay=round(6*round(float(new_ride.calculatedDistance), 1), 1)
        form.save()
        return HttpResponseRedirect('/ridelist/')
    return render(request, 'taximanager/changeRide.html', {'form': form})


@login_required
def select_ride(request, ride_id):
    ride = get_object_or_404(Ride, pk=ride_id)
    form = ViewRideForm(initial={
        'pickupAddress': ride.pickupAddress,
        'dropOffAddress': ride.dropOffAddress,
        'ETA': ride.ETA,
        'calculatedDistance': ride.calculatedDistance,
        'pickupLatitude': ride.pickupLatitude,
        'pickupLongitude': ride.pickupLongitude,
        'dropOffLatitude': ride.dropOffLatitude,
        'dropOffLongitude': ride.dropOffLongitude,
        'email': ride.email,
        'pay': ride.pay,
        'status': ride.status,
        'driverID': ride.loginID,
        'cabID': ride.cabID,
        'loginID': ride.loginID,
        'notes': ride.notes,
    })
    return render(request, 'taximanager/select_ride.html', {'ride': ride, 'form':form})


@login_required
def change_status(request, ride_id):
    ride = get_object_or_404(Ride, pk=ride_id)
    send_mail('Taxi manager', 'Status is:' + ride.status.name, settings.EMAIL_HOST_USER,
                      [ride.email], fail_silently=False)
    try:
        new_status = Status.objects.get(id=request.POST['status'])
        ride.status = new_status
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
def change_status_driver(request, driver_id):
    driver = get_object_or_404(Driver, pk=driver_id)
    if request.POST.get('isActive', False):
        cab = Cab.objects.get(id=request.POST['cab'])
        cab.isActive = True
        driver.isActive = True
        driver.cabID = cab
    else:
        cab = Cab.objects.get(id=request.POST['cab'])
        cab.isActive = False
        driver.isActive = False
        driver.cabID = None
    driver.save()
    cab.save()
    return HttpResponseRedirect('/drivers/')
