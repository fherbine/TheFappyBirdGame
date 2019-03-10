from random import Random

from kivy.app import App
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import (
    ObjectProperty,
    NumericProperty,
)

class Platform(BoxLayout):
    y1 = NumericProperty()
    y2 = NumericProperty()

class Player(Image):
    pass

class GameScreen(Screen):
    time = NumericProperty()
    player = ObjectProperty()
    walls_container = ObjectProperty()

    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.platforms = []
        self.platform_width = 100
        self.player_velocity = 0

    def on_pre_enter(self, *largs, **kwargs):
        app = App.get_running_app()
        self.time = 0
        self.read_high_score()

    def on_enter(self):
        Clock.schedule_interval(self.update_time, 0)
        self.bind(time=self.on_walls_move)

    def update_time(self, dt):
        self.time += dt
        self.recalculate_player_drop(dt)

    def on_touch_up(self, *largs, **kwargs):
        self.player_velocity = 3 if self.player_velocity < 10 else 10

    def recalculate_player_drop(self, dt):
        self.player_velocity -= dt * 15

    def on_walls_move(self, *largs, **kwargs):
        self.check_collision()
        if self.current:
            #FIXME: hacky stuff
            self.moves_player()

        if self.walls_container.x % self.platform_width == 0:
            self.add_platform()

    def moves_player(self):
        if 0 <= self.player.y <= self.walls_container.top - self.player.height:
            self.player.y += self.player_velocity
        else:
            self.game_over()

    def check_collision(self):
        if not self.platforms:
            return

        for platform in self.platforms:
            if platform.x == self.player.right or platform.x <= self.player.center_x <= platform.right:
                if (
                    platform.y1 <= self.player.y
                    and self.player.top <= platform.y2
                ):
                    break
                else:
                    self.game_over()

    def game_over(self):
        Clock.unschedule(self.update_time)
        self.write_high_score()
        popup = Factory.GameOverPopup()
        popup.score = self.current
        popup.open()

    def read_high_score(self):
        with open('data/player_data', 'r') as data:
            line = data.readline()

        self.high_score = line if line else 'None'


    def write_high_score(self):
        with open('data/player_data', 'r') as data:
            line = data.readline()

        if line:
            if int(line) > int(self.current):
                return

        with open('data/player_data', 'w+') as data:
            data.write(str(self.current))

    def add_platform(self):
        platform = Platform()
        platform.width = self.platform_width
        if self.platforms:
            previous = self.platforms[-1]
        else:
            previous = False
        y1, y2 = self.find_ys(previous, self.player.height)
        platform.ids.lower_wall.height = y1
        platform.ids.upper_wall.height = self.walls_container.height - y2
        self.walls_container.width += self.platform_width
        self.platforms.append(platform)
        self.walls_container.add_widget(platform)

    def find_ys(self, previous, player_size):
        y1 = Random().randint(self.height / 4, self.height / 2)
        y2 = Random().randint(self.height / 2, self.height / 1.2)
        if previous:
            py1 = previous.y1
            py2 = previous.y2
        space = y2 - y1

        if space > player_size:
            if not previous:
                return y1, y2
            if y1 < py2 - player_size or y2 > player_size + py1:
                return y1, y2

        return self.find_ys(previous, player_size)




Builder.load_file('screens/game_screen.kv')
