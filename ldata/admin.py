from django.contrib import admin

from .models import Branch, Mileage, Train

for model in Branch, Train, Mileage:
    admin.site.register(model)
