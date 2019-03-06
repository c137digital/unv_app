import os
import importlib
import pathlib

from .settings import SETTINGS


def get_app_components():
    for component in SETTINGS['components']:
        component = '{}.app'.format(component)
        try:
            yield importlib.import_module(component)
        except ModuleNotFoundError:
            continue


def get_project_root(app_module: str = 'app.settings') -> pathlib.Path:
    """Return project root path, outside "src" directory."""
    module_path = os.environ.get('SETTINGS', 'app.settings')
    module = importlib.import_module(module_path)
    return pathlib.Path(module.__file__).parent
