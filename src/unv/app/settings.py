from .core import ComponentSettings


class AppSettings(ComponentSettings):
    KEY = 'app'
    SCHEMA = {
        'env': {
            'type': 'string',
            'allowed': ['production', 'development', 'testing'],
            'required': True
        },
        'components': {
            'type': 'list',
            'empty': True,
            'schema': {'type': 'string'},
            'required': True
        }
    }
    DEFAULTS = {
        'env': 'development',
        'components': [],
    }

    def is_development(self):
        return self._data['env'] == 'development'

    def is_production(self):
        return self._data['env'] == 'production'

    def is_testing(self):
        return self._data['env'] == 'testing'


SETTINGS = AppSettings()
