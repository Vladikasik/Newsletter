from django.contrib import admin
from .models import User, Bot_message, Code
# Register your models here.
admin.site.register(User)
admin.site.register(Bot_message)
admin.site.register(Code)
