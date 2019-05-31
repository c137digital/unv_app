# import inspect

from .settings import SETTINGS


class Application:
    """Used for setup in other components to provide universal way
    of starting and decomposing apps."""
    def __init__(self):
        self.apps = {}
        self.start = {}

    def register(self, app):
        self.apps[type(app)] = app

    async def setup(self):
        for component in SETTINGS.get_components():
            component.setup()

        # inspector
        # insepctor.getfullargspec()
        # .annotations
        # with annotated type
        # for apps[annotated.type] = app
