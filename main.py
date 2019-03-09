from kivy.app import App
from kivy.clock import Clock
from kivy.properties import (
    ObjectProperty,
    NumericProperty,
    StringProperty,
)

import config
from screens import * # noqa
from widgets import * # noqa


class FappyBirdApp(App):
    screenmanager = ObjectProperty()
    time = NumericProperty(0.0)
    player_pic = StringProperty('data/images/fherbine.png')

    def build(self):
        Clock.schedule_interval(self.update_time, 0)

    def update_time(self, dt):
        self.time += dt

if __name__ == '__main__':
    FappyBirdApp().run()
