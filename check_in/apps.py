from django.apps import AppConfig

"""
Include this config class in gamification/settings.py INSTALLED_APPS 
to activate the check_in models in the main settings
"""
class CheckInConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'check_in'
