from django.db import models
from django.conf import settings



class Cab(models.Model):
    licensePlateNumber = models.CharField(max_length=100)
    type = models.CharField(max_length=120)
    isActive = models.BooleanField()

    def __unicode__(self):
        #return '%s - %s' % (self.licensePlateNumber, self.type)
        return self.type

class Driver(models.Model):
    name = models.CharField(max_length=80)
    isActive = models.BooleanField()
    cabID = models.OneToOneField(Cab, null=True, blank=True)
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.name




class Status(models.Model):
    SHIRT_SIZES = (
        ('Accepted', 'Accepted'),
        ('Dispatched', 'Dispatched'),
        ('Pickup', 'Pickup'),
        ('Passenger on Board', 'Passenger on Board'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
        ('Rejected', 'Rejected'),
    )
    name = models.CharField(max_length=50, choices=SHIRT_SIZES)

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.name


class Ride(models.Model):
    pickupAddress = models.CharField(max_length=100, verbose_name='pickup Address')
    dropOffAddress = models.CharField(max_length=100)
    ETA = models.CharField(max_length=20)
    calculatedDistance = models.CharField(max_length=20)
    pickupLatitude = models.FloatField()
    pickupLongitude = models.FloatField()
    dropOffLatitude = models.FloatField()
    dropOffLongitude = models.FloatField()
    email = models.EmailField()
    pay = models.FloatField()
    status = models.ForeignKey(Status)
    driverID = models.ForeignKey(Driver, null=True, blank=True)
    cabID = models.ForeignKey(Cab, null=True, blank=True)
    loginID = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, blank=True)
    notes = models.TextField(max_length=300, blank=True, )
    dateCreated = models.DateTimeField(auto_now_add=True, auto_now=True)


    class Meta:
        ordering = ["-dateCreated"]


    def __unicode__(self):  # Python 3: def __str__(self):
        return '%s  %s' % (self.pickupAddress, self.dropOffAddress)