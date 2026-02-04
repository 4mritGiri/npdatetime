"""Django app configuration for npdatetime_django"""
from django.apps import AppConfig


class NpdatetimeDjangoConfig(AppConfig):
    """Configuration for the npdatetime_django app"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'npdatetime_django'
    verbose_name = 'Nepali DateTime for Django'
    
    def ready(self):
        """Called when the app is ready"""
        pass
