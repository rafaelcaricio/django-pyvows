

class SettingsOverrideSupport(object):
    def __init__(self):
        self.ignore('settings')

    def settings(self, **kwargs):
        from django.test.utils import override_settings
        return override_settings(**kwargs)
