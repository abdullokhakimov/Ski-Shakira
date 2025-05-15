import arcade
import os
import time
from typing import Optional

# Game constants
TILE_SCALING = 0.5
PLAYER_SCALING = 1

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Ski Platformer"
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING
CAMERA_PAN_SPEED = 0.5

# Player states
SKIING = 0
JUMPING = 1
GAME_OVER = 2
LEVEL_COMPLETE = 3  # Added new state for level completion
DANCING = 4  # New state for dancing animation

# Physics constants
GRAVITY = 2500
DEFAULT_DAMPING = 0.05
PLAYER_DAMPING = 0.03
PLAYER_FRICTION = 0.01
WALL_FRICTION = 0.2
DYNAMIC_ITEM_FRICTION = 0.3
PLAYER_MASS = 1.5
PLAYER_MAX_HORIZONTAL_SPEED = 1500
PLAYER_MAX_VERTICAL_SPEED = 1800
PLAYER_MOVE_FORCE_ON_GROUND = 1500
PLAYER_MOVE_FORCE_IN_AIR = 1000
PLAYER_JUMP_IMPULSE = 2000

# Animation constants
DANCE_ANIMATION_SPEED = 0.3  # Time between frames in seconds


class GameView(arcade.View):
    """Main game view class."""

    def __init__(self):
        """Initialize the game view."""
        super().__init__()

        # Game state
        self.score = 0
        self.game_over = False
        self.level_complete = False  # Added new state variable

        # Level management
        self.current_level = 1
        self.max_level = 3  # Set the maximum number of levels here

        # Player properties
        self.player_sprite = None
        self.player_rotation = 0
        self.player_state = SKIING

        # Animation properties
        self.dance_textures = []
        self.current_dance_frame = 0
        self.dance_timer = 0
        self.dance_start_time = None

        # Input tracking
        self.left_pressed = False
        self.right_pressed = False
        self.jump_needs_reset = False

        # Map properties
        self.tile_map = None
        self.end_of_map = 0

        # Sprite lists
        self.player_list = None
        self.terrain_list = None
        self.coin_list = None
        self.obstacle_list = None

        # Physics engine
        self.physics_engine = None

        # Performance tracking
        self.last_time = None
        self.frame_count = 0

        # Cameras
        self.camera = None
        self.camera_bounds = None
        self.gui_camera = None

        # UI elements
        self.fps_text = None
        self.distance_text = None
        self.score_text = None
        self.level_text = None  # Added level display

        # Set background color
        self.background_color = arcade.color.SKY_BLUE

    def setup(self):
        """Set up the game and initialize variables."""
        # Initialize sprite lists
        self.player_list = arcade.SpriteList()

        # Initialize UI elements
        self._setup_ui()

        # Load animation textures
        self._load_dance_textures()

        # Load map and sprites for the current level
        self._load_level(self.current_level)

        # Set up cameras
        self._setup_cameras()

        # Set up physics engine
        self._setup_physics_engine()

        # Reset game state
        self.game_over = False
        self.level_complete = False  # Reset level complete flag
        self.player_state = SKIING  # Reset player state

    def _load_dance_textures(self):
        """Load the dance animation textures."""
        self.dance_textures = []

        # Load the four dancing animation frames
        for i in range(1, 5):
            texture_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                f"assets/Sprites/shakira_dance{i}.png"
            )
            texture = arcade.load_texture(texture_path)
            self.dance_textures.append(texture)

    def _setup_ui(self):
        """Set up UI text elements."""
        self.fps_text = arcade.Text(
            "",
            x=10,
            y=40,
            color=arcade.color.BLACK,
            font_size=14
        )
        self.distance_text = arcade.Text(
            "0.0",
            x=10,
            y=20,
            color=arcade.color.BLACK,
            font_size=14,
        )
        self.score_text = arcade.Text(
            "Score: 0",
            x=10,
            y=60,
            color=arcade.color.BLACK,
            font_size=14,
        )
        self.level_text = arcade.Text(
            f"Level: {self.current_level}/{self.max_level}",
            x=10,
            y=80,
            color=arcade.color.BLACK,
            font_size=14,
        )

    def _load_level(self, level_number):
        """Load a specific level by number."""
        # Load the tilemap for the current level
        map_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"map/Level{level_number}.tmj")
        layer_options = {
            "Platforms": {"use_spatial_hash": True},
            "Obstacles": {"use_spatial_hash": True},
            "Coins": {"use_spatial_hash": True}
        }

        self.tile_map = arcade.load_tilemap(
            map_path, layer_options=layer_options, scaling=TILE_SCALING
        )
        self.end_of_map = self.tile_map.width * GRID_PIXEL_SIZE

        # Get map layers
        self.terrain_list = self.tile_map.sprite_lists.get("Terrain")
        self.coin_list = self.tile_map.sprite_lists.get("Collectibles")
        self.obstacle_list = self.tile_map.sprite_lists.get("Obstacles")

        # Create player sprite
        player_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   "assets/Sprites/shakira.png")
        self.player_sprite = arcade.Sprite(player_path, scale=PLAYER_SCALING)

        # Position player at top left of map
        self.player_sprite.center_x = GRID_PIXEL_SIZE * 2
        self.player_sprite.center_y = (self.tile_map.height * GRID_PIXEL_SIZE -
                                       GRID_PIXEL_SIZE * 2 + 128)

        self.player_rotation = 0
        self.player_state = SKIING
        self.player_list.append(self.player_sprite)

        # Update level text
        if hasattr(self, 'level_text'):
            self.level_text.text = f"Level: {self.current_level}/{self.max_level}"

    def _load_map_and_sprites(self):
        """Load the map and initialize game sprites."""
        # This method is replaced by _load_level for multi-level support
        self._load_level(self.current_level)

    def _setup_cameras(self):
        """Set up game cameras."""
        self.camera = arcade.Camera2D()
        self.gui_camera = arcade.Camera2D()

        # Define camera bounds
        if self.tile_map:
            max_x = GRID_PIXEL_SIZE * self.tile_map.width
            max_y = GRID_PIXEL_SIZE * self.tile_map.height
        else:
            max_x = 5000  # Default value
            max_y = 2000  # Default value

        self.camera_bounds = arcade.LRBT(
            self.window.width / 2.0, max_x - self.window.width / 2.0,
            self.window.height / 2.0, max_y
        )

        # Set initial camera position
        if self.tile_map:
            left_edge = self.window.width / 2.0
            top_edge = max_y - self.window.height / 2.0
            self.camera.position = (left_edge, top_edge)

        # Center camera on player
        self.pan_camera_to_user(1.0)

    def _setup_physics_engine(self):
        """Set up the Pymunk physics engine."""
        # Create physics engine with gravity
        self.physics_engine = arcade.PymunkPhysicsEngine(
            damping=DEFAULT_DAMPING,
            gravity=(0, -GRAVITY)
        )

        # Add player to physics engine
        self.physics_engine.add_sprite(
            self.player_sprite,
            friction=PLAYER_FRICTION,
            mass=PLAYER_MASS,
            moment_of_inertia=arcade.PymunkPhysicsEngine.MOMENT_INF,
            collision_type="player",
            max_horizontal_velocity=PLAYER_MAX_HORIZONTAL_SPEED,
            max_vertical_velocity=PLAYER_MAX_VERTICAL_SPEED,
        )

        # Add terrain as static bodies
        if self.terrain_list:
            self.physics_engine.add_sprite_list(
                self.terrain_list,
                friction=WALL_FRICTION,
                collision_type="wall",
                body_type=arcade.PymunkPhysicsEngine.STATIC,
            )

        # Add obstacles as dynamic bodies
        if self.obstacle_list:
            self.physics_engine.add_sprite_list(
                self.obstacle_list,
                friction=DYNAMIC_ITEM_FRICTION,
                collision_type="item"
            )

    def on_draw(self):
        """Render the screen."""
        # Clear screen and set background
        self.clear()
        arcade.set_background_color(arcade.color.SKY_BLUE)

        # Use game camera for world elements
        self.camera.use()

        # Increment frame counter
        self.frame_count += 1

        # Draw game elements
        self._draw_game_elements()

        # Use GUI camera for UI elements
        self.gui_camera.use()

        # Draw UI elements
        self._draw_ui_elements()

    def _draw_game_elements(self):
        """Draw all game elements."""
        # Draw map elements if they exist
        if self.terrain_list:
            self.terrain_list.draw()
        if self.coin_list:
            self.coin_list.draw()
        if self.obstacle_list:
            self.obstacle_list.draw()

        # Draw player
        self.player_list.draw()

    def _draw_ui_elements(self):
        """Draw all UI elements."""
        # Update and draw FPS
        if self.last_time and self.frame_count % 60 == 0:
            fps = round(1.0 / (time.time() - self.last_time) * 60)
            self.fps_text.text = f"FPS: {fps:3d}"
        self.fps_text.draw()

        # Update time for FPS calculation
        if self.frame_count % 60 == 0:
            self.last_time = time.time()

        # Update and draw distance
        distance = self.player_sprite.right
        self.distance_text.text = f"Distance: {distance:.1f}"
        self.distance_text.draw()

        # Draw score
        self.score_text.text = f"Score: {self.score}"
        self.score_text.draw()

        # Draw level indicator
        self.level_text.text = f"Level: {self.current_level}/{self.max_level}"
        self.level_text.draw()

        # Draw level complete message if applicable
        if self.level_complete:
            if self.current_level < self.max_level:
                arcade.draw_text(
                    "Level Complete! - Press N for Next Level",
                    self.window.width // 2,
                    self.window.height // 2,
                    arcade.color.GREEN,
                    30,
                    anchor_x="center"
                )
            else:
                arcade.draw_text(
                    "Congratulations! You completed all levels!",
                    self.window.width // 2,
                    self.window.height // 2,
                    arcade.color.GREEN,
                    30,
                    anchor_x="center"
                )
            arcade.draw_text(
                f"Final Score: {self.score}",
                self.window.width // 2,
                self.window.height // 2 - 40,
                arcade.color.GREEN,
                20,
                anchor_x="center"
            )

        # Draw game over text if applicable
        elif self.game_over:
            arcade.draw_text(
                "Game Over - Press R to Restart",
                self.window.width // 2,
                self.window.height // 2,
                arcade.color.RED,
                30,
                anchor_x="center"
            )

    def on_key_press(self, key, modifiers):
        """Handle key press events."""
        if self.game_over:
            # Restart game if 'R' is pressed
            if key == arcade.key.R:
                self.current_level = 1  # Reset to first level
                self.setup()
                self.score = 0
                return
        elif self.level_complete:
            # Go to next level if 'N' is pressed
            if key == arcade.key.N and self.current_level < self.max_level:
                self.current_level += 1
                # Clear current sprite lists before loading next level
                if self.player_list:
                    self.player_list = arcade.SpriteList()
                self.setup()
                return
        else:
            # Jump if space is pressed and player is on ground
            if key == arcade.key.SPACE:
                if self.physics_engine.is_on_ground(self.player_sprite):
                    impulse = (0, PLAYER_JUMP_IMPULSE)
                    self.physics_engine.apply_impulse(self.player_sprite, impulse)

        # Show pause screen if Escape is pressed
        if key == arcade.key.ESCAPE:
            pause_view = PauseView(self)
            self.window.show_view(pause_view)

    def on_key_release(self, key, modifiers):
        """Handle key release events."""
        if key == arcade.key.SPACE:
            self.jump_needs_reset = False

    def on_update(self, delta_time):
        """Update game state and logic."""
        # Skip updates if game is over
        if self.game_over:
            return

        # Handle dancing animation if level is complete
        if self.level_complete:
            self._update_dance_animation(delta_time)
            return

        # Check for game over conditions
        self._check_end_conditions()

        # Skip the rest of updates if game is over or level is complete after check
        if self.game_over or self.level_complete:
            if self.level_complete:
                # Start dancing when level is complete
                self.player_state = DANCING
                self.dance_start_time = time.time()
                self.current_dance_frame = 0
                self.dance_timer = 0
            return

        # Update player state and position
        self._update_player_state()

        # Check for collisions
        self._handle_collisions()

        # Update camera position
        self.pan_camera_to_user(CAMERA_PAN_SPEED)

    def _update_dance_animation(self, delta_time):
        """Update the dance animation frames."""
        if self.player_state != DANCING:
            return

        # Update dance animation timer
        self.dance_timer += delta_time

        # Change animation frame when timer exceeds frame duration
        if self.dance_timer >= DANCE_ANIMATION_SPEED:
            self.dance_timer = 0
            self.current_dance_frame = (self.current_dance_frame + 1) % len(self.dance_textures)

            # Update the player sprite texture
            if self.dance_textures and len(self.dance_textures) > 0:
                self.player_sprite.texture = self.dance_textures[self.current_dance_frame]

    def _check_end_conditions(self):
        """Check if any end conditions are met."""
        # Check if player reached the end of the map
        if self.player_sprite.right >= self.end_of_map:
            self.level_complete = True
            self.player_state = DANCING  # Switch to dancing state
            self.dance_start_time = time.time()
            self.current_dance_frame = 0
            self.dance_timer = 0
            # Set initial dance frame
            if self.dance_textures and len(self.dance_textures) > 0:
                self.player_sprite.texture = self.dance_textures[0]
            return

        # Check if player fell off the map
        if self.player_sprite.center_y < -100:
            self.game_over = True
            self.player_state = GAME_OVER
            return

    def _update_player_state(self):
        """Update player state and physics."""
        # Check if player is on ground
        is_on_ground = self.physics_engine.is_on_ground(self.player_sprite)

        # Apply appropriate force based on ground contact
        if is_on_ground:
            force = (PLAYER_MOVE_FORCE_ON_GROUND, 0)
        else:
            force = (PLAYER_MOVE_FORCE_IN_AIR, 0)

        # Apply force to player
        self.physics_engine.apply_force(self.player_sprite, force)

        # Set friction to zero while moving
        self.physics_engine.set_friction(self.player_sprite, 0)

        # Update physics simulation
        self.physics_engine.step()

    def _handle_collisions(self):
        """Handle collisions with coins and obstacles."""
        # Check for coin collisions
        if self.coin_list:
            coins_hit = arcade.check_for_collision_with_list(
                self.player_sprite, self.coin_list
            )

            # Remove collected coins and update score
            for coin in coins_hit:
                coin.remove_from_sprite_lists()
                self.score += 1

        # Check for obstacle collisions
        if self.obstacle_list:
            obstacle_hit_list = arcade.check_for_collision_with_list(
                self.player_sprite, self.obstacle_list
            )

            # Game over if hit obstacle
            if len(obstacle_hit_list) > 0:
                self.game_over = True
                self.player_state = GAME_OVER

    def pan_camera_to_user(self, panning_fraction: float = 1.0):
        """
        Pan camera to follow the player.

        Args:
            panning_fraction: Speed of camera movement (0 to 1)
        """
        # Calculate target camera position
        screen_center_x, screen_center_y = self.player_sprite.position

        # Enforce minimum distance from edges
        if screen_center_x < self.camera.viewport_width / 2:
            screen_center_x = self.camera.viewport_width / 2
        if screen_center_y < self.camera.viewport_height / 2:
            screen_center_y = self.camera.viewport_height / 2

        # Set target position
        user_centered = screen_center_x, screen_center_y

        # Smoothly move camera toward target
        self.camera.position = arcade.math.lerp_2d(
            self.camera.position,
            user_centered,
            panning_fraction,
        )


class PauseView(arcade.View):
    """View shown when game is paused."""

    def __init__(self, game_view):
        """Initialize pause view."""
        super().__init__()
        self.game_view = game_view

    def on_show_view(self):
        """Set up the pause screen."""
        self.window.background_color = arcade.color.WHITE_SMOKE

    def on_draw(self):
        """Draw the pause screen."""
        self.clear()

        # Draw player with orange overlay
        player_sprite = self.game_view.player_sprite
        arcade.draw_sprite(player_sprite)

        arcade.draw_lrbt_rectangle_filled(
            left=player_sprite.left,
            right=player_sprite.right,
            bottom=player_sprite.bottom,
            top=player_sprite.top,
            color=arcade.color.ORANGE[:3] + (200,)
        )

        # Draw pause text
        arcade.draw_text(
            "PAUSED",
            WINDOW_WIDTH / 2,
            WINDOW_HEIGHT / 2 + 50,
            arcade.color.BLACK,
            font_size=50,
            anchor_x="center"
        )

        # Draw instructions
        arcade.draw_text(
            "Press Esc. to return",
            WINDOW_WIDTH / 2,
            WINDOW_HEIGHT / 2,
            arcade.color.BLACK,
            font_size=20,
            anchor_x="center"
        )

    def on_key_press(self, key, _modifiers):
        """Handle key press events in pause screen."""
        if key == arcade.key.ESCAPE:  # Resume game
            self.window.show_view(self.game_view)


def main():
    """Main function to start the game."""
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    game = GameView()
    window.show_view(game)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()