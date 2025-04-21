'''Nur ein Test von Spielkonzept.
Automatische Bewegung nach vorne und Space-taste um zu Springen.
Quadrat als Steine(Hindernisse) und Kreise als Münzen. Der Spielfigur ist auch ein Quadrat.'''

import arcade
import random

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Prototyp_default"

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 40
PLAYER_SPEED = 5
PLAYER_JUMP_SPEED = 15
GRAVITY = 0.5

COIN_RADIUS = 10
ROCK_WIDTH = 30
ROCK_HEIGHT = 30
PLATFORM_HEIGHT = 20

SCROLL_SPEED = 3
SPAWN_INTERVAL = 50

class AltoGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Sprite lists
        self.player_list = None
        self.platform_list = None
        self.coin_list = None
        self.rock_list = None

        # Player sprite
        self.player_sprite = None

        # Physics engine
        self.physics_engine = None

        # Game state
        self.score = 0
        self.game_over = False
        self.frame_count = 0

        # Background color
        arcade.set_background_color(arcade.color.SANDY_BROWN)

    def setup(self):
        # Initialize sprite lists
        self.player_list = arcade.SpriteList()
        self.platform_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.rock_list = arcade.SpriteList()

        # Create player
        self.player_sprite = arcade.SpriteSolidColor(PLAYER_WIDTH, PLAYER_HEIGHT, arcade.color.BLUE)
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = SCREEN_HEIGHT - 100
        self.player_list.append(self.player_sprite)

        # Create initial ground
        ground = arcade.SpriteSolidColor(SCREEN_WIDTH * 2, PLATFORM_HEIGHT, arcade.color.DARK_GREEN)
        ground.center_x = SCREEN_WIDTH
        ground.center_y = 50
        self.platform_list.append(ground)

        # Set up physics engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, self.platform_list, gravity_constant=GRAVITY
        )

    def spawn_platform(self):
        # Create a new platform with random height
        platform_width = random.randint(100, 300)
        platform_y = random.randint(50, SCREEN_HEIGHT // 2)
        platform = arcade.SpriteSolidColor(platform_width, PLATFORM_HEIGHT, arcade.color.DARK_GREEN)
        platform.center_x = SCREEN_WIDTH + platform_width // 2
        platform.center_y = platform_y
        self.platform_list.append(platform)

        # Randomly spawn a coin
        if random.random() < 0.5:
            coin = arcade.SpriteCircle(COIN_RADIUS, arcade.color.GOLD)
            coin.center_x = platform.center_x
            coin.center_y = platform.center_y + PLATFORM_HEIGHT + COIN_RADIUS
            self.coin_list.append(coin)

        # Randomly spawn a rock
        if random.random() < 0.3:
            rock = arcade.SpriteSolidColor(ROCK_WIDTH, ROCK_HEIGHT, arcade.color.GRAY)
            rock.center_x = platform.center_x
            rock.center_y = platform.center_y + PLATFORM_HEIGHT // 2 + ROCK_HEIGHT // 2
            self.rock_list.append(rock)

    def on_draw(self):
        self.clear()
        self.platform_list.draw()
        self.coin_list.draw()
        self.rock_list.draw()
        self.player_list.draw()

        # Draw score
        arcade.draw_text(f"Score: {self.score}", 10, SCREEN_HEIGHT - 30, arcade.color.BLACK, 18)

        # Draw game over
        if self.game_over:
            arcade.draw_text("Game Over! Press R to Restart", SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2, arcade.color.RED, 24)

    def on_update(self, delta_time):
        if not self.game_over:
            self.frame_count += 1

            # Spawn new platforms periodically
            if self.frame_count % SPAWN_INTERVAL == 0:
                self.spawn_platform()

            # Scroll everything left
            for sprite in self.platform_list:
                sprite.center_x -= SCROLL_SPEED
            for sprite in self.coin_list:
                sprite.center_x -= SCROLL_SPEED
            for sprite in self.rock_list:
                sprite.center_x -= SCROLL_SPEED

            # Update physics
            self.physics_engine.update()

            # Check for coin collisions
            coins_hit = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)
            for coin in coins_hit:
                coin.remove_from_sprite_lists()
                self.score += 1

            # Check for rock collisions
            if arcade.check_for_collision_with_list(self.player_sprite, self.rock_list):
                self.game_over = True

            # Remove off-screen sprites
            for sprite in self.platform_list:
                if sprite.right < 0:
                    sprite.remove_from_sprite_lists()
            for sprite in self.coin_list:
                if sprite.right < 0:
                    sprite.remove_from_sprite_lists()
            for sprite in self.rock_list:
                if sprite.right < 0:
                    sprite.remove_from_sprite_lists()

            # Keep player from falling too low
            if self.player_sprite.center_y < 0:
                self.game_over = True

    def on_key_press(self, key, modifiers):
        if not self.game_over:
            # Jump
            if key == arcade.key.SPACE and self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
        else:
            # Restart game
            if key == arcade.key.R:
                self.setup()
                self.score = 0
                self.game_over = False
                self.frame_count = 0

def main():
    game = AltoGame()
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()