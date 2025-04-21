'''
Spiel um die Sprung und Sammlung Mechanik auf eine geneigte Boden zu testen!

Space taste zum springen
Hindernisse sind kommentiert, weil es zu kaotisch war.
'''


import arcade
import random

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Rolling Ball"

PLAYER_RADIUS = 20
PLAYER_JUMP_SPEED = 20
GRAVITY = 1

COIN_RADIUS = 10
OBSTACLE_WIDTH = 30
OBSTACLE_HEIGHT = 30
PLATFORM_HEIGHT = 20

SCROLL_SPEED = 4
SPAWN_INTERVAL = 60
SLOPE_ANGLE = 10  # Degrees for downward slope

class HillRunnerGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Sprite lists
        self.player_list = None
        self.platform_list = None
        self.coin_list = None
        self.obstacle_list = None

        # Player sprite
        self.player_sprite = None

        # Physics engine
        self.physics_engine = None

        # Game state
        self.score = 0
        self.game_over = False
        self.frame_count = 0

    def setup(self):
        # Initialize sprite lists
        self.player_list = arcade.SpriteList()
        self.platform_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.obstacle_list = arcade.SpriteList()

        # Create initial platform (sloped downward)
        platform = arcade.SpriteSolidColor(SCREEN_WIDTH * 2, PLATFORM_HEIGHT, arcade.color.DARK_GREEN)
        platform.center_x = SCREEN_WIDTH
        platform.center_y = SCREEN_HEIGHT - 400  # Lowered platform position
        platform.angle = SLOPE_ANGLE  # Positive angle for downward slope
        self.platform_list.append(platform)

        # Create player
        self.player_sprite = arcade.SpriteCircle(PLAYER_RADIUS, arcade.color.BLUE)
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = SCREEN_HEIGHT - 50  # Adjusted to be above platform
        self.player_list.append(self.player_sprite)

        # Set up physics engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, self.platform_list, gravity_constant=GRAVITY
        )

        # Initial physics update to settle the player
        self.physics_engine.update()

        # Reset game state
        self.score = 0
        self.game_over = False
        self.frame_count = 0

        # Set background color
        arcade.set_background_color(arcade.color.SKY_BLUE)

    def spawn_platform(self):
        # Create a new platform with random length
        platform_width = random.randint(100, 300)
        last_platform = self.platform_list[-1]
        # Calculate y position based on the slope (tan(10°) ≈ 0.176), decreasing y for downward slope
        platform_y = last_platform.center_y - (last_platform.width // 2 + platform_width // 2) * 0.176
        platform = arcade.SpriteSolidColor(platform_width, PLATFORM_HEIGHT, arcade.color.DARK_GREEN)
        platform.center_x = SCREEN_WIDTH + platform_width // 2
        platform.center_y = platform_y
        platform.angle = SLOPE_ANGLE  # Positive angle for downward slope
        self.platform_list.append(platform)

        # Randomly spawn a coin
        if random.random() < 0.5:
            coin = arcade.SpriteCircle(COIN_RADIUS, arcade.color.GOLD)
            coin.center_x = platform.center_x
            coin.center_y = platform.center_y + PLATFORM_HEIGHT + COIN_RADIUS
            self.coin_list.append(coin)

        # Randomly spawn an obstacle
        ''' 
        if random.random() < 0.3:
            obstacle = arcade.SpriteSolidColor(OBSTACLE_WIDTH, OBSTACLE_HEIGHT, arcade.color.GRAY)
            obstacle.center_x = platform.center_x
            obstacle.center_y = platform.center_y + PLATFORM_HEIGHT // 2 + OBSTACLE_HEIGHT // 2
            self.obstacle_list.append(obstacle)
        '''

    def on_draw(self):
        self.clear()
        self.platform_list.draw()
        self.coin_list.draw()
        self.obstacle_list.draw()
        self.player_list.draw()

        # Draw score
        arcade.draw_text(f"Score: {self.score}", 10, SCREEN_HEIGHT - 30, arcade.color.BLACK, 18)

        # Draw game over
        if self.game_over:
            arcade.draw_text(
                "Game Over! Press R to Restart",
                SCREEN_WIDTH // 2 - 150,
                SCREEN_HEIGHT // 2,
                arcade.color.RED,
                24
            )

    def on_update(self, delta_time):
        if not self.game_over:
            self.frame_count += 1

            # Spawn new platforms periodically
            if self.frame_count % SPAWN_INTERVAL == 0:
                self.spawn_platform()

            # Scroll everything left
            for sprite in self.platform_list:
                sprite.center_x -= SCROLL_SPEED
                sprite.center_y += SCROLL_SPEED * 0.176  # Decrease y for downward slope
            for sprite in self.coin_list:
                sprite.center_x -= SCROLL_SPEED
                sprite.center_y += SCROLL_SPEED * 0.176
            for sprite in self.obstacle_list:
                sprite.center_x -= SCROLL_SPEED
                sprite.center_y += SCROLL_SPEED * 0.176

            # Update physics
            self.physics_engine.update()

            # Check for coin collisions
            coins_hit = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)
            for coin in coins_hit:
                coin.remove_from_sprite_lists()
                self.score += 1

            # Check for obstacle collisions
            if arcade.check_for_collision_with_list(self.player_sprite, self.obstacle_list):
                self.game_over = True

            # Remove off-screen sprites
            for sprite in self.platform_list:
                if sprite.right < 0:
                    sprite.remove_from_sprite_lists()
            for sprite in self.coin_list:
                if sprite.right < 0:
                    sprite.remove_from_sprite_lists()
            for sprite in self.obstacle_list:
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

def main():
    game = HillRunnerGame()
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()