from django.apps import AppConfig


class MayaConfig(AppConfig):
    name = 'maya'

    def ready(self):
        super(MayaConfig,self).ready()

        from django.utils.module_loading import autodiscover_modules
        autodiscover_modules('dove')
