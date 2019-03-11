import importlib

from .settings import SETTINGS


def get_app_components():
    for component in SETTINGS['components']:
        component = '{}.app'.format(component)
        try:
            yield importlib.import_module(component)
        except ModuleNotFoundError:
            continue
