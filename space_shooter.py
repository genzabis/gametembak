from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics import Rectangle, Color
from random import randint
from kivy.core.window import Window
from kivy.uix.label import Label

# Atur ukuran layar
Window.size = (800, 600)

class SpaceShooterGame(Widget):
    def __init__(self, **kwargs):
        super(SpaceShooterGame, self).__init__(**kwargs)
        self.game_over = False
        self.score = 0  # Inisialisasi skor
        self._setup_game()
        self.bind(size=self.on_size)
        Clock.schedule_interval(self.update, 1 / 60.0)

    def _setup_game(self):
        self.background = None
        self.ship = None
        self.bullets = []
        self.asteroids = []
        self.spawn_background()
        self.spawn_ship()
        self.spawn_score_label()  # Menambahkan label skor di bagian atas kiri

    def spawn_background(self):
        # Tambahkan background
        with self.canvas:
            self.background = Rectangle(source='images/background.png', pos=self.pos, size=Window.size)

    def spawn_score_label(self):
        # Tambahkan label untuk skor di bagian atas kiri
        self.score_label = Label(text=f"Skor: {self.score}", font_size='20sp', color=(1, 1, 1, 1),
                                 pos=(10, self.height - 40), size_hint=(None, None))
        self.add_widget(self.score_label)

    def spawn_ship(self):
        # Tambahkan pesawat
        with self.canvas:
            self.ship = Rectangle(source='images/ship.png', size=(140, 140), pos=(self.center_x, 50))

    def on_size(self, *args):
        # Update ukuran elemen-elemen ketika layar berubah
        self.background.size = self.size
        self.score_label.pos = (10, self.height - 40)
        self.spawn_asteroids()

    def spawn_asteroids(self):
        # Buat asteroid di posisi acak
        with self.canvas:
            for _ in range(10):
                x = randint(0, self.width - 60)
                y = randint(self.height // 2, self.height - 60)
                asteroid = Rectangle(source='images/asteroid.png', size=(80, 80), pos=(x, y))
                self.asteroids.append(asteroid)

    def on_touch_move(self, touch):
        if not self.game_over:
            self.ship.pos = (touch.x - self.ship.size[0] / 2, 50)

    def on_touch_down(self, touch):
        if not self.game_over:
            self.spawn_bullet()

    def spawn_bullet(self):
        with self.canvas:
            bullet = Rectangle(source='images/bullet.png', size=(10, 70),
                               pos=(self.ship.pos[0] + 25, self.ship.pos[1] + 50))
            self.bullets.append(bullet)

    def update(self, dt):
        if self.game_over:
            return

        # Update posisi peluru
        for bullet in self.bullets:
            bullet.pos = (bullet.pos[0], bullet.pos[1] + 10)

        # Update posisi asteroid
        for asteroid in self.asteroids:
            asteroid.pos = (asteroid.pos[0], asteroid.pos[1] - 2)
            if asteroid.pos[1] < 0:  # Jika asteroid keluar layar, kembalikan ke atas
                asteroid.pos = (randint(0, self.width - 60), self.height)

        # Cek collision peluru dengan asteroid
        for bullet in self.bullets[:]:
            for asteroid in self.asteroids[:]:
                if self.check_collision(bullet, asteroid):
                    # Hapus asteroid dan peluru saat terjadi tabrakan
                    self.asteroids.remove(asteroid)
                    self.bullets.remove(bullet)
                    self.canvas.remove(asteroid)
                    self.canvas.remove(bullet)

                    # Tambahkan skor
                    self.score += 100
                    self.score_label.text = f"Skor: {self.score}"  # Perbarui teks skor

        # Cek collision pesawat dengan asteroid
        for asteroid in self.asteroids:
            if self.check_collision(self.ship, asteroid):
                self.end_game()

    def check_collision(self, obj1, obj2):
        return (
            obj1.pos[0] < obj2.pos[0] + obj2.size[0] and
            obj1.pos[0] + obj1.size[0] > obj2.pos[0] and
            obj1.pos[1] < obj2.pos[1] + obj2.size[1] and
            obj1.pos[1] + obj1.size[1] > obj2.pos[1]
        )

    def end_game(self):
        self.game_over = True
        Clock.unschedule(self.update)
        print("Game Over!")
        label = Label(text="GAME OVER", font_size='40sp', bold=True,
                      pos=(self.width / 2 - 100, self.height / 2))
        self.add_widget(label)

class SpaceShooterApp(App):
    def build(self):
        game = SpaceShooterGame()
        return game

if __name__ == "__main__":
    SpaceShooterApp().run()
