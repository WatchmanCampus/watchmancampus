from django.contrib import admin
from .models import Tick, Hostel, Post, Transaction, Institution
# Register your models here.


admin.site.register(Tick)
admin.site.register(Hostel)
admin.site.register(Post)
admin.site.register(Transaction)
admin.site.register(Institution)
