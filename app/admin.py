from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Locations)
admin.site.register(Barber)
admin.site.register(Cut)
admin.site.register(Appointments)
