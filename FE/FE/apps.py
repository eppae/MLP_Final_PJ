from django.apps import AppConfig


class FeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "FE"
    
    def ready(self):
        import FE.signals 
        
