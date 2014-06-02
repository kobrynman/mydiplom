from django.contrib import admin
from taximanager.models import Driver,Cab,Status,Ride


class DriverAdmin(admin.ModelAdmin):
    list_display = ['name', 'isActive']


class CabAdmin(admin.ModelAdmin):
    list_display = ['licensePlateNumber', 'type', 'isActive']


class StatusAdmin(admin.ModelAdmin):
    list_display = ['name']


class RideAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,          {'fields': ['pickupAddress','dropOffAddress','ETA','calculatedDistance',
                                    'pickupLatitude','pickupLongitude','dropOffLatitude','dropOffLongitude',]}),
        ('Foreign Key', {'fields': ['status','driverID','cabID','loginID',]}),
        ('notes',        {'fields': ['notes'],'classes': ['collapse']}),
    ]
    list_display = ('dateCreated','pickupAddress','dropOffAddress','ETA','calculatedDistance','status','loginID')


class LoginAdmin(admin.ModelAdmin):
    #fields = ['userName', 'email', 'password', 'isActive']
    list_display = ('userName', 'email', 'password', 'isActive')
    search_fields = ['userName']


admin.site.register(Driver,DriverAdmin)
admin.site.register(Cab,CabAdmin)
admin.site.register(Status,StatusAdmin)
admin.site.register(Ride,RideAdmin)


