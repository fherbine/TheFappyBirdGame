from kivy.lang import Builder
from kivy.uix.modalview import ModalView
from kivy.factory import Factory
from kivy.app import App
from kivy.properties import ObjectProperty

class GameOverPopup(ModalView):
    target = ObjectProperty()

    def on_dismiss(self, *largs, **kwargs):
        super(GameOverPopup, self).on_dismiss(**kwargs)
        app = App.get_running_app()
        app.root.ids.screenmanager.current = 'home'
        if self.target:
            self.target.reset()

Factory.register(GameOverPopup.__name__, cls=GameOverPopup)

Builder.load_file('widgets/game_over.kv')
