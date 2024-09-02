from django.contrib import admin

from .models import CustomUser
"""Module for registering models to admin site of application"""
admin.site.register(CustomUser)