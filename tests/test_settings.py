import os
import importlib

import pytest

from unv.app.settings import ComponentSettings, SETTINGS


class InitModule:
    def __init__(self):
        self.SETTINGS = ComponentSettings.create()


class DevelopmentModule:
    def __init__(self):
        self.SETTINGS = ComponentSettings.create({
            'app': {
                'debug': True,
                'port': 8090,
                'items': [1, 2, 3]
            }
        })


class ProductionModule:
    def __init__(self):
        self.SETTINGS = ComponentSettings.create({
            'app': {
                'debug': False,
                'port': 80,
                'items': [3, 2, 1]
            },
            'otherkey': {'debug': True, 'items': [10, 10, 10]}
        })


class InvalidSettingsModule:
    def __init__(self):
        self.SETTINGS = ComponentSettings.create({
            'otherkey': {'debug': 1, 'items': ['asd', 10, 10]}
        })


class SomeComponentModule:
    def __init__(self, key='app'):
        class SomeSettings(ComponentSettings):
            KEY = key
            SCHEMA = {
                'debug': {'type': 'boolean'},
                'items': {'type': 'list', 'schema': {'type': 'integer'}},
                'port': {'type': 'integer'}
            }
            DEFAULT = {
                'debug': False,
                'items': [1]
            }

        self.SETTINGS = SomeSettings()


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
    ({'SETTINGS': 'app.settings.development'}, {
        'app': {'debug': True, 'items': [1, 2, 3], 'port': 8090},
        'otherkey': {'debug': False, 'items': [1]}
    }),
    ({'SETTINGS': 'app.settings.production'}, {
        'app': {'debug': False, 'items': [3, 2, 1], 'port': 80},
        'otherkey': {'debug': True, 'items': [10, 10, 10]}
    }),
    ({
        'SETTINGS': 'app.settings.development',
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

    # first component
    comp_module = importlib.import_module('app.components.some.settings')
    assert comp_module.SETTINGS._data == settings['app']

    # second other component
    comp_module = importlib.import_module('app.components.other.settings')
    assert comp_module.SETTINGS._data == settings['otherkey']


def test_app_components_with_env():
    assert SETTINGS.is_development
    assert not SETTINGS.is_production
    assert not SETTINGS.is_testing

    assert list(SETTINGS.get_components())


def test_failed_load_settings(monkeypatch):
    class SomeSettings(ComponentSettings):
        KEY = 'somekey'
        SCHEMA = {}
        DEFAULT = {}

    SomeSettings()

    monkeypatch.setattr(importlib, 'import_module', import_fake_module)
    monkeypatch.setattr(
        os, 'environ', {'SETTINGS': 'some_not_found_path.for.development'})

    with pytest.raises(ImportError):
        SomeSettings()


@pytest.mark.parametrize('settings', [
    'app.settings.invalid.missing_key',
    'app.settings.invalid.schema_error'
])
def test_validation_component_settings(settings):
    # TODO: add negative cases
    pass