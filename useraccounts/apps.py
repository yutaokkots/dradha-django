"""Django app configuration for 'useraccounts' app."""
from django.apps import AppConfig

class UseraccountsConfig(AppConfig):
    """Class used to configure the settings for the 'useraccounts' app.
    
    Attributes
    ----------
    default_auto_field:
        Specifies the default primary key field for models in the app.
    name:
        Specifies the name of the app.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "useraccounts"
