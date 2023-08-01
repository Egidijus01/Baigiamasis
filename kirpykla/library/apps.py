from django.apps import AppConfig

class LibraryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'library'

    def ready(self):
        # Import and register your template tags here
        from .templatetags.user_tags import in_kirpejai_group

        from library.templatetags.user_tags import in_kirpejai_group  # Replace 'library' with your app's name
        from django.apps import apps
        User = apps.get_model('auth', 'User')
        from .signals import create_profile, save_profile

# Make sure the custom template tag is imported at the top of the 'user_tags.py' file