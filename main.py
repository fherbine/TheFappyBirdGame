from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ObjectProperty

import config


class FappyBirdApp(App):
    screenmanager = ObjectProperty()

    def build(self):
        self.time = 0.0
        Clock.schedule_interval(self.update_time, 0)

    def update_time(self, dt)
        self.time += dt

if __name__ == '__main__':
    FappyBirdApp().run()
