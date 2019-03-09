from kivy.lang import Builder
from kivy.uix.modalview import ModalView
from kivy.factory import Factory
from kivy.app import App

class GameOverPopup(ModalView):
    def on_dismiss(self, *largs, **kwargs):
        app = App.get_running_app()
        app.root.ids.screenmanager.current = 'home'

Factory.register(GameOverPopup.__name__, cls=GameOverPopup)

Builder.load_file('widgets/game_over.kv')
