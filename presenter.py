from model import Model
from view import View

class Presenter:
    def __init__(self, model, view):
        self._init_model(model)
        self._init_view(view)


    def _init_model(self, model):
        self._model = model


    def _init_view(self, view):
        self._view = view


    def show(self):
        self._view.show()
