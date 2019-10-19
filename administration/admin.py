from django.contrib import admin
from .models import Order,Type,Service,Profile,Assign
admin.site.register(Order)
admin.site.register(Type)
admin.site.register(Service)
admin.site.register(Profile)
admin.site.register(Assign)
