import os
import importlib

import pytest

from unv.app.core import create_settings, create_component_settings


class InitModule:
    def __init__(self):
        self.SETTINGS = create_settings()


class DevelopmentModule:
    def __init__(self):
        self.SETTINGS = create_settings({
            'app': {
                'debug': True,
                'port': 8090,
                'items': [1, 2, 3]
            }
        })


class ProductionModule:
    def __init__(self):
        self.SETTINGS = create_settings({
            'app': {
                'debug': False,
                'port': 80,
                'items': [3, 2, 1]
            },
            'otherkey': {'debug': True, 'items': [10, 10, 10]}
        })


class InvalidSettingsModule:
    def __init__(self):
        self.SETTINGS = create_settings({
            'otherkey': {'debug': 1, 'items': ['asd', 10, 10]}
        })


class SomeComponentModule:
    def __init__(self, key='app'):
        self.SCHEMA = {
            'debug': {'type': 'boolean'},
            'items': {'type': 'list', 'schema': {'type': 'integer'}},
            'port': {'type': 'integer'}
        }
        self.DEFAULT = {
            'debug': False,
            'items': [1]
        }
        self.SETTINGS = \
            create_component_settings(key, self.DEFAULT, self.SCHEMA)


class OtherComponentModule(SomeComponentModule):
    def __init__(self):
        super().__init__('otherkey')


MODULES = {
    'app.settings.development': DevelopmentModule,
    'app.settings.production': ProductionModule,
    'app.components.some.settings': SomeComponentModule,
    'app.components.other.settings': OtherComponentModule
}


def import_fake_module(name):
    if name not in MODULES:
        raise ImportError
    return MODULES[name]()


@pytest.mark.parametrize('env, settings', [
    ({}, {
        'app': {'debug': True, 'items': [1, 2, 3], 'port': 8090},
        'otherkey': {'debug': False, 'items': [1]}
    }),
    ({'SETTINGS': 'app.settings.production'}, {
        'app': {'debug': False, 'items': [3, 2, 1], 'port': 80},
        'otherkey': {'debug': True, 'items': [10, 10, 10]}
    }),
    ({
        'SETTINGS_APP_DEBUG': 'False',
        'SETTINGS_OTHERKEY_DEBUG': 'True',
        'SETTINGS_APP_PORT': '9020'
    }, {
        'app': {'debug': False, 'items': [1, 2, 3], 'port': 9020},
        'otherkey': {'debug': True, 'items': [1]}
    })
])
def test_success_load_settings(monkeypatch, env, settings):
    monkeypatch.setattr(importlib, 'import_module', import_fake_module)
    monkeypatch.setattr(os, 'environ', env)

    # main settings
    app_module = importlib.import_module(
        os.environ.get('SETTINGS', 'app.settings.development'))
    assert app_module.SETTINGS['app'] == settings['app']

    # first component
    comp_module = importlib.import_module('app.components.some.settings')
    assert comp_module.SETTINGS == settings['app']

    # second other component
    comp_module = importlib.import_module('app.components.other.settings')
    assert comp_module.SETTINGS == settings['otherkey']


def test_failed_load_settings(monkeypatch):
    create_component_settings('somekey', {}, {})

    monkeypatch.setattr(importlib, 'import_module', import_fake_module)
    monkeypatch.setattr(
        os, 'environ', {'SETTINGS': 'some_not_found_path.for.development'})

    with pytest.raises(ImportError):
        create_component_settings('somekey', {}, {})


@pytest.mark.parametrize('settings', [
    'app.settings.invalid.missing_key',
    'app.settings.invalid.schema_error'
])
def test_validation_component_settings(settings):
    # TODO: add negative cases
    pass
