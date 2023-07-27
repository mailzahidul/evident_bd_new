from django.contrib import admin
from .models import InputValue
# Register your models here.

class InputValueAdmin(admin.ModelAdmin):
    list_display = ['user', 'timestamp', 'input_values']

admin.site.register(InputValue, InputValueAdmin)
