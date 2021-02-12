from django.apps import AppConfig


class LoginConfig(AppConfig):
    name = 'LOGIN'

    def ready(self):
        import  LOGIN.signal