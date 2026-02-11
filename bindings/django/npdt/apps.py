"""Django app configuration for npdt"""
from django.apps import AppConfig


class NpdatetimeDjangoConfig(AppConfig):
    """Configuration for the npdt app"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'npdt'
    verbose_name = 'Nepali DateTime for Django'
    
    def ready(self):
        """Called when the app is ready"""
        pass
