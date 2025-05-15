import arcade
import os
import time
import math

# Game Constants
class GameConstants:
    """Constants for the ski platformer game."""
    # Window and sprite scaling
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
    LEVEL_COMPLETE = 3
    DANCING = 4

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
    PLAYER_JUMP_IMPULSE = 2500

    # Animation and scoring constants
    DANCE_ANIMATION_SPEED = 0.3
    FLIP_SPEED = 360  # Degrees per second
    FLIP_THRESHOLD = 315  # Degrees for a flip
    POINTS_PER_FLIP = 10
    BONUS_MESSAGE_DURATION = 1.5  # Seconds for bonus message

class GameView(arcade.View):
    """Main game view for the ski platformer."""

    def __init__(self):
        """Initialize game state and components."""
        super().__init__()

        # Game state
        self.score = 0
        self.game_over = False
        self.level_complete = False
        self.current_level = 1
        self.max_level = 3

        # Player properties
        self.player_sprite = None
        self.player_visual_angle = 0
        self.player_state = GameConstants.SKIING
        self.was_on_ground = False
        self.flip_rotation = 0

        # Animation properties
        self.dance_textures = []
        self.current_dance_frame = 0
        self.dance_timer = 0
        self.dance_start_time = None

        # Bonus message
        self.bonus_message = None
        self.bonus_timer = 0

        # Input tracking
        self.left_pressed = False
        self.right_pressed = False

        # Map and sprite lists
        self.tile_map = None
        self.end_of_map = 0
        self.player_list = None
        self.terrain_list = None
        self.coin_list = None
        self.obstacle_list = None

        # Physics and cameras
        self.physics_engine = None
        self.camera = None
        self.camera_bounds = None
        self.gui_camera = None

        # UI elements
        self.score_text = None
        self.level_text = None

        self.background_color = arcade.color.SKY_BLUE

    def setup(self):
        """Set up the game environment."""
        self.player_list = arcade.SpriteList()
        self._setup_ui()
        self._load_dance_textures()
        self._load_level(self.current_level)
        self._setup_cameras()
        self._setup_physics_engine()
        self._reset_game_state()

    def _reset_game_state(self):
        """Reset game state for a new level or restart."""
        self.game_over = False
        self.level_complete = False
        self.player_state = GameConstants.SKIING
        self.was_on_ground = False
        self.player_visual_angle = 0
        self.flip_rotation = 0
        self.bonus_message = None
        self.bonus_timer = 0

    def _load_dance_textures(self):
        """Load textures for dance animation."""
        self.dance_textures = []
        for i in range(1, 5):
            texture_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                f"assets/Sprites/shakira_dance{i}.png"
            )
            self.dance_textures.append(arcade.load_texture(texture_path))

    def _setup_ui(self):
        """Initialize UI text elements."""
        self.score_text = arcade.Text(
            "Score: 0",
            x=GameConstants.WINDOW_WIDTH - 10,
            y=GameConstants.WINDOW_HEIGHT - 50,
            color=arcade.color.BLACK,
            font_size=20,
            anchor_x="right"
        )
        self.level_text = arcade.Text(
            f"Level: {self.current_level}/{self.max_level}",
            x=GameConstants.WINDOW_WIDTH - 10,
            y=GameConstants.WINDOW_HEIGHT - 20,
            color=arcade.color.BLACK,
            font_size=15,
            anchor_x="right"
        )

    def _load_level(self, level_number):
        """Load a level from a tilemap file."""
        map_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"map/Level{level_number}.tmj")
        layer_options = {
            "Platforms": {"use_spatial_hash": True},
            "Obstacles": {"use_spatial_hash": True},
            "Coins": {"use_spatial_hash": True}
        }
        self.tile_map = arcade.load_tilemap(map_path, layer_options=layer_options, scaling=GameConstants.TILE_SCALING)
        self.end_of_map = self.tile_map.width * GameConstants.GRID_PIXEL_SIZE

        self.terrain_list = self.tile_map.sprite_lists.get("Terrain")
        self.coin_list = self.tile_map.sprite_lists.get("Collectibles")
        self.obstacle_list = self.tile_map.sprite_lists.get("Obstacles")

        player_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets/Sprites/shakira.png")
        self.player_sprite = arcade.Sprite(player_path, scale=GameConstants.PLAYER_SCALING)
        self.player_sprite.center_x = GameConstants.GRID_PIXEL_SIZE * 2
        self.player_sprite.center_y = (self.tile_map.height * GameConstants.GRID_PIXEL_SIZE -
                                      GameConstants.GRID_PIXEL_SIZE * 2 + 128)
        self.player_sprite.angle = 0
        self.player_list.append(self.player_sprite)

        if hasattr(self, 'level_text'):
            self.level_text.text = f"Level: {self.current_level}/{self.max_level}"

    def _setup_cameras(self):
        """Initialize game and GUI cameras."""
        self.camera = arcade.Camera2D()
        self.gui_camera = arcade.Camera2D()

        max_x = GameConstants.GRID_PIXEL_SIZE * self.tile_map.width if self.tile_map else 5000
        max_y = GameConstants.GRID_PIXEL_SIZE * self.tile_map.height if self.tile_map else 2000

        self.camera_bounds = arcade.LRBT(
            self.window.width / 2.0, max_x - self.window.width / 2.0,
            self.window.height / 2.0, max_y
        )

        if self.tile_map:
            left_edge = self.window.width / 2.0
            top_edge = max_y - self.window.height / 2.0
            self.camera.position = (left_edge, top_edge)

        self.pan_camera_to_user(1.0)

    def _setup_physics_engine(self):
        """Initialize physics engine with player and environment."""
        self.physics_engine = arcade.PymunkPhysicsEngine(
            damping=GameConstants.DEFAULT_DAMPING,
            gravity=(0, -GameConstants.GRAVITY)
        )
        self.physics_engine.add_sprite(
            self.player_sprite,
            friction=GameConstants.PLAYER_FRICTION,
            mass=GameConstants.PLAYER_MASS,
            moment_of_inertia=arcade.PymunkPhysicsEngine.MOMENT_INF,
            collision_type="player",
            max_horizontal_velocity=GameConstants.PLAYER_MAX_HORIZONTAL_SPEED,
            max_vertical_velocity=GameConstants.PLAYER_MAX_VERTICAL_SPEED,
        )
        if self.terrain_list:
            self.physics_engine.add_sprite_list(
                self.terrain_list,
                friction=GameConstants.WALL_FRICTION,
                collision_type="wall",
                body_type=arcade.PymunkPhysicsEngine.STATIC,
            )
        if self.obstacle_list:
            self.physics_engine.add_sprite_list(
                self.obstacle_list,
                friction=GameConstants.DYNAMIC_ITEM_FRICTION,
                collision_type="item"
            )

    def on_update(self, delta_time):
        """Update game state each frame."""
        if self.game_over:
            return
        if self.level_complete:
            self._update_dance_animation(delta_time)
            return

        self._check_end_conditions()
        if self.game_over or self.level_complete:
            self._handle_level_end()
            return

        self._update_player_state(delta_time)
        self._handle_collisions()
        self.pan_camera_to_user(GameConstants.CAMERA_PAN_SPEED)

        if self.bonus_timer > 0:
            self.bonus_timer -= delta_time
            if self.bonus_timer <= 0:
                self.bonus_message = None

    def _update_player_state(self, delta_time):
        """Update player movement and state."""
        is_on_ground = self.physics_engine.is_on_ground(self.player_sprite)
        if not is_on_ground and self.player_state != GameConstants.GAME_OVER:
            self.player_state = GameConstants.JUMPING

        self._handle_rotation(delta_time, is_on_ground)
        self._handle_landing(is_on_ground)
        self._apply_physics(is_on_ground)

        self.was_on_ground = is_on_ground

    def _handle_rotation(self, delta_time, is_on_ground):
        """Update player rotation while airborne."""
        if is_on_ground or self.player_state != GameConstants.JUMPING:
            return

        rotation = 0
        if self.left_pressed:
            rotation -= GameConstants.FLIP_SPEED * delta_time  # Clockwise
        if self.right_pressed:
            rotation += GameConstants.FLIP_SPEED * delta_time  # Counterclockwise

        self.player_visual_angle += rotation
        self.flip_rotation += rotation

        self.player_visual_angle %= 360
        if self.player_visual_angle < 0:
            self.player_visual_angle += 360

    def _handle_landing(self, is_on_ground):
        """Check landing conditions and award flip points."""
        if not is_on_ground or self.was_on_ground:
            return

        angle = self.player_visual_angle % 360
        if 135 <= angle <= 225:  # Landing on head
            self.game_over = True
            self.player_state = GameConstants.GAME_OVER
            self.flip_rotation = 0
            return

        flips = math.floor(abs(self.flip_rotation) / GameConstants.FLIP_THRESHOLD)
        if flips > 0:
            bonus_points = flips * GameConstants.POINTS_PER_FLIP
            self.score += bonus_points
            self._show_bonus_message(bonus_points)

        self.player_visual_angle = 0
        self.flip_rotation = 0
        self.player_state = GameConstants.SKIING

    def _show_bonus_message(self, points):
        """Display bonus message for flip points."""
        self.bonus_message = arcade.Text(
            f"Flipping Bonus: +{points} points",
            x=GameConstants.WINDOW_WIDTH - 10,
            y=GameConstants.WINDOW_HEIGHT - 80,
            color=arcade.color.GREEN,
            font_size=20,
            anchor_x="right"
        )
        self.bonus_timer = GameConstants.BONUS_MESSAGE_DURATION

    def _apply_physics(self, is_on_ground):
        """Apply movement forces and update physics."""
        force = (GameConstants.PLAYER_MOVE_FORCE_ON_GROUND if is_on_ground else
                 GameConstants.PLAYER_MOVE_FORCE_IN_AIR, 0)
        self.physics_engine.apply_force(self.player_sprite, force)
        self.physics_engine.set_friction(self.player_sprite, 0)
        self.physics_engine.step()

    def _handle_collisions(self):
        """Process collisions with coins and obstacles."""
        if self.coin_list:
            for coin in arcade.check_for_collision_with_list(self.player_sprite, self.coin_list):
                coin.remove_from_sprite_lists()
                self.score += 1

        if self.obstacle_list and arcade.check_for_collision_with_list(self.player_sprite, self.obstacle_list):
            self.game_over = True
            self.player_state = GameConstants.GAME_OVER

    def _check_end_conditions(self):
        """Check for level completion or game over."""
        if self.player_sprite.right >= self.end_of_map:
            self.level_complete = True
            return
        if self.player_sprite.center_y < -100:
            self.game_over = True
            self.player_state = GameConstants.GAME_OVER

    def _handle_level_end(self):
        """Handle level completion setup."""
        if not self.level_complete:
            return
        self.player_state = GameConstants.DANCING
        self.dance_start_time = time.time()
        self.current_dance_frame = 0
        self.dance_timer = 0
        if self.dance_textures:
            self.player_sprite.texture = self.dance_textures[0]

    def _update_dance_animation(self, delta_time):
        """Update dance animation for level completion."""
        if self.player_state != GameConstants.DANCING:
            return
        self.dance_timer += delta_time
        if self.dance_timer >= GameConstants.DANCE_ANIMATION_SPEED:
            self.dance_timer = 0
            self.current_dance_frame = (self.current_dance_frame + 1) % len(self.dance_textures)
            if self.dance_textures:
                self.player_sprite.texture = self.dance_textures[self.current_dance_frame]

    def on_draw(self):
        """Render the game screen."""
        self.clear()
        arcade.set_background_color(arcade.color.SKY_BLUE)
        self.camera.use()
        self._draw_game_elements()
        self.gui_camera.use()
        self._draw_ui()

    def _draw_game_elements(self):
        """Draw sprites for terrain, coins, obstacles, and player."""
        if self.terrain_list:
            self.terrain_list.draw()
        if self.coin_list:
            self.coin_list.draw()
        if self.obstacle_list:
            self.obstacle_list.draw()
        self.player_sprite.angle = self.player_visual_angle
        self.player_list.draw()

    def _draw_ui(self):
        """Draw HUD and game state messages."""
        self._draw_hud()
        self._draw_game_state_messages()

    def _draw_hud(self):
        """Draw score, level, and bonus message."""
        self.score_text.text = f"Score: {self.score}"
        self.score_text.draw()
        self.level_text.draw()

        if self.bonus_message and self.bonus_timer > 0:
            alpha = int(255 * (self.bonus_timer / GameConstants.BONUS_MESSAGE_DURATION))
            self.bonus_message.color = (arcade.color.GREEN[0], arcade.color.GREEN[1], arcade.color.GREEN[2], alpha)
            self.bonus_message.draw()

    def _draw_game_state_messages(self):
        """Draw level complete or game over messages."""
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
        if self.game_over and key == arcade.key.R:
            self.current_level = 1
            self.score = 0
            self.setup()
            return
        if self.level_complete and key == arcade.key.N and self.current_level < self.max_level:
            self.current_level += 1
            self.player_list = arcade.SpriteList()
            self.setup()
            return
        if key == arcade.key.SPACE and self.physics_engine.is_on_ground(self.player_sprite):
            self.physics_engine.apply_impulse(self.player_sprite, (0, GameConstants.PLAYER_JUMP_IMPULSE))
            self.player_state = GameConstants.JUMPING
        elif key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True
        elif key == arcade.key.ESCAPE:
            self.window.show_view(PauseView(self))

    def on_key_release(self, key, modifiers):
        """Handle key release events."""
        if key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False

    def pan_camera_to_user(self, panning_fraction: float = 1.0):
        """Pan camera to follow the player."""
        screen_center_x, screen_center_y = self.player_sprite.position
        screen_center_x = max(screen_center_x, self.camera.viewport_width / 2)
        screen_center_y = max(screen_center_y, self.camera.viewport_height / 2)
        self.camera.position = arcade.math.lerp_2d(
            self.camera.position,
            (screen_center_x, screen_center_y),
            panning_fraction,
        )

class PauseView(arcade.View):
    """View for the pause screen."""

    def __init__(self, game_view):
        """Initialize pause view with reference to game view."""
        super().__init__()
        self.game_view = game_view

    def on_show_view(self):
        """Set up the pause screen appearance."""
        self.window.background_color = arcade.color.WHITE_SMOKE

    def on_draw(self):
        """Draw the pause screen."""
        self.clear()
        player_sprite = self.game_view.player_sprite
        player_sprite.angle = self.game_view.player_visual_angle
        arcade.draw_sprite(player_sprite)
        arcade.draw_lrbt_rectangle_filled(
            left=player_sprite.left,
            right=player_sprite.right,
            bottom=player_sprite.bottom,
            top=player_sprite.top,
            color=arcade.color.ORANGE[:3] + (200,)
        )
        arcade.draw_text(
            "PAUSED",
            GameConstants.WINDOW_WIDTH / 2,
            GameConstants.WINDOW_HEIGHT / 2 + 50,
            arcade.color.BLACK,
            font_size=50,
            anchor_x="center"
        )
        arcade.draw_text(
            "Press Esc. to return",
            GameConstants.WINDOW_WIDTH / 2,
            GameConstants.WINDOW_HEIGHT / 2,
            arcade.color.BLACK,
            font_size=20,
            anchor_x="center"
        )

    def on_key_press(self, key, _modifiers):
        """Handle key presses in pause screen."""
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.game_view)

def main():
    """Entry point for the game."""
    window = arcade.Window(GameConstants.WINDOW_WIDTH, GameConstants.WINDOW_HEIGHT, GameConstants.WINDOW_TITLE)
    game = GameView()
    window.show_view(game)
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()