import pathlib

from unv.app.core import create_settings

SETTINGS = create_settings({
    'env': 'testing',
    'app': {
        'root': str(pathlib.Path(__file__).parent)
    }
})
