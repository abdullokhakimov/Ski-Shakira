import arcade

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

class SkiGame(arcade.Window):
    def __init__(self):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, "Software Project")
        arcade.set_background_color(arcade.color.SKY_BLUE)

    def on_draw(self):
        self.clear()

def main():
    game = SkiGame()
    arcade.run()

if __name__ == "__main__":
    main()