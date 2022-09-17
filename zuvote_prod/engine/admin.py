from django.contrib import admin
from .models import Competitions, Contestants, RequestPay
# Register your models here.
admin.site.register(Competitions)
admin.site.register(Contestants)
admin.site.register(RequestPay)