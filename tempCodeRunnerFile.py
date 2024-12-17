import random
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.properties import NumericProperty
from kivy.graphics import Rectangle
from kivy.core.image import Image as CoreImage
import os

# Ukuran layar
Window.size = (400, 400)

class SnakeGame(Widget):
    snake_parts = []
    food = None
    score = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.grid_size = 20
        self.snake_parts = [[100, 100], [80, 100], [60, 100]]  # Posisi awal ular
        self.food = [200, 200]  # Posisi awal makanan
        self.direction = "RIGHT"
        self.running = True

        # Label skor
        self.score_label = Label(text=f"Score: {self.score}", size_hint=(1, None), height=30)
        self.add_widget(self.score_label)

        # Path ke gambar ular
        snake_image_path = "images/ular.png"
        # Path ke gambar makanan
        food_image_path = "images/apel.png"  # Gambar makanan baru

        # Cek apakah file gambar ular ada
        if not os.path.exists(snake_image_path):
            raise FileNotFoundError(f"Gambar ular tidak ditemukan: {snake_image_path}")
        # Cek apakah file gambar makanan ada
        if not os.path.exists(food_image_path):
            raise FileNotFoundError(f"Gambar makanan tidak ditemukan: {food_image_path}")

        # Load gambar ular
        self.snake_body_image = CoreImage(snake_image_path).texture
        # Load gambar makanan
        self.food_image = CoreImage(food_image_path).texture

        # Jadwal pembaruan permainan
        Clock.schedule_interval(self.update, 1 / 10)

    def reset_game(self):
        """Mengatur ulang permainan."""
        self.snake_parts = [[100, 100], [80, 100], [60, 100]]
        self.food = [200, 200]
        self.direction = "RIGHT"
        self.running = True
        self.score = 0

    def spawn_food(self):
        """Membuat makanan di lokasi acak."""
        self.food = [
            random.randint(0, (Window.width - self.grid_size) // self.grid_size) * self.grid_size,
            random.randint(0, (Window.height - self.grid_size) // self.grid_size) * self.grid_size,
        ]

    def update(self, dt):
        """Mengatur logika permainan."""
        if not self.running:
            return

        # Menggerakkan ular
        head_x, head_y = self.snake_parts[0]
        if self.direction == "UP":
            head_y += self.grid_size
        elif self.direction == "DOWN":
            head_y -= self.grid_size
        elif self.direction == "LEFT":
            head_x -= self.grid_size
        elif self.direction == "RIGHT":
            head_x += self.grid_size

        # Menambahkan posisi baru kepala ular
        new_head = [head_x, head_y]
        self.snake_parts.insert(0, new_head)

        # Periksa jika ular memakan makanan
        if new_head == self.food:
            self.score += 1  # Tambah skor
            self.spawn_food()  # Munculkan makanan baru
        else:
            self.snake_parts.pop()  # Hapus ekor jika tidak memakan makanan

        # Periksa tabrakan dengan dinding
        if (
            head_x < 0
            or head_y < 0
            or head_x >= Window.width
            or head_y >= Window.height
        ):
            self.running = False

        # Periksa tabrakan dengan tubuh ular
        if new_head in self.snake_parts[1:]:
            self.running = False

        # Perbarui tampilan
        self.canvas.clear()
        with self.canvas:
            # Gambar tubuh ular
            for part in self.snake_parts:
                Rectangle(texture=self.snake_body_image, pos=part, size=(self.grid_size, self.grid_size))

            # Gambar makanan
            Rectangle(texture=self.food_image, pos=self.food, size=(self.grid_size, self.grid_size))

        self.score_label.text = f"Score: {self.score}"  # Perbarui label skor

    def change_direction(self, new_direction):
        """Mengubah arah ular."""
        opposite = {"UP": "DOWN", "DOWN": "UP", "LEFT": "RIGHT", "RIGHT": "LEFT"}
        if new_direction != opposite.get(self.direction):  # Hindari arah berlawanan
            self.direction = new_direction

class SnakeApp(App):
    def build(self):
        self.game = SnakeGame()
        Window.bind(on_key_down=self.on_keyboard)
        return self.game

    def on_keyboard(self, window, key, scancode, codepoint, modifier):
        """Menangkap input keyboard."""
        key_mapping = {
            273: "UP",    # Tombol Panah Atas
            274: "DOWN",  # Tombol Panah Bawah
            276: "LEFT",  # Tombol Panah Kiri
            275: "RIGHT", # Tombol Panah Kanan
        }
        if key in key_mapping:
            self.game.change_direction(key_mapping[key])
        if key == 114:  # Tombol "R" untuk reset
            self.game.reset_game()

if __name__ == "__main__":
    SnakeApp().run()
