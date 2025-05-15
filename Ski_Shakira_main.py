import arcade
import os
import time
import math
from arcade.future.light import Light, LightLayer

# Game constants
TILE_SCALING = 0.5
PLAYER_SCALING = 0.8

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

# Gravity
GRAVITY = 2000

# Damping - Amount of speed lost per second
DEFAULT_DAMPING = 0.06
PLAYER_DAMPING = 0.03

# Friction between objects
PLAYER_FRICTION = 0.00
WALL_FRICTION = 0.2
DYNAMIC_ITEM_FRICTION = 0.3

# Mass (defaults to 1)
PLAYER_MASS = 1

# Keep player from going too fast
PLAYER_MAX_HORIZONTAL_SPEED = 1500
PLAYER_MAX_VERTICAL_SPEED = 1800

# Force applied while on the ground
PLAYER_MOVE_FORCE_ON_GROUND = 1500

# Force applied when moving left/right in the air
PLAYER_MOVE_FORCE_IN_AIR = 1000

# Strength of a jump
PLAYER_JUMP_IMPULSE = 1300

# Animation constants
DANCE_ANIMATION_SPEED = 0.3
FLIP_SPEED = 360
FLIP_THRESHOLD = 315
POINTS_PER_FLIP = 10
BONUS_MESSAGE_DURATION = 2.0

# Lighting constants for level 2
SPOTLIGHT_RADIUS = 350
AMBIENT_LIGHT_COLOR = (20, 20, 20, 255)
SPOTLIGHT_COLOR = arcade.csscolor.WHITE

# Fade constants
FADE_OUT_DURATION = 2.0
FADE_IN_DURATION = 2.2

class GameView(arcade.View):
    def __init__(self):
        """Initialize the game view."""
        super().__init__()

        # Game state
        self.score = 0
        self.game_over = False
        self.level_complete = False

        # Level management
        self.current_level = 1
        self.max_level = 2

        # Player properties
        self.player_sprite = None
        self.player_visual_angle = 0
        self.player_state = SKIING
        self.was_on_ground = False
        self.flip_rotation = 0
        self.terrain_angle = 0

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

        # Cameras
        self.camera = None
        self.camera_bounds = None
        self.gui_camera = None

        # UI elements
        self.score_text = None
        self.level_text = None

        # Lighting setup
        self.light_layer = None
        self.player_light = None

        # Sound properties
        self.background_music = None
        self.dance_music = None
        self.background_music_player = None
        self.dance_music_player = None
        self.background_music_files = {
            1: os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets/audio/music1.mp3"),
            2: os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets/audio/music2.mp3")
        }
        self.dance_music_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets/audio/dancemusic.mp3")
        self.background_music_volume = 0.5
        self.dance_music_volume = 0.7

        # Fade properties
        self.fade_out_player = None
        self.fade_out_timer = 0
        self.fade_out_duration = FADE_OUT_DURATION
        self.fade_in_player = None
        self.fade_in_timer = 0
        self.fade_in_duration = FADE_IN_DURATION
        self.fade_in_target_volume = 0

        # Set background color
        self.background_color = arcade.color.SKY_BLUE

    def setup(self):
        """Set up the game and initialize variables."""
        # Ensure all music is stopped before setting up
        self._stop_all_music(immediate=True)
        # Reset fade states
        self.fade_out_player = None
        self.fade_out_timer = 0
        self.fade_in_player = None
        self.fade_in_timer = 0
        self.fade_in_target_volume = 0

        self.player_list = arcade.SpriteList()
        self._setup_ui()
        self._load_dance_textures()
        self._load_level(self.current_level)
        self._setup_cameras()
        self._setup_physics_engine()
        self._setup_lighting()
        self.game_over = False
        self.level_complete = False
        self.player_state = SKIING
        self.was_on_ground = False
        self.player_visual_angle = 0
        self.flip_rotation = 0
        self.bonus_message = None
        self.bonus_timer = 0
        self._setup_sounds()

    def _setup_sounds(self):
        """Load and start background music with fade-in."""
        # Ensure no existing music players
        if self.background_music_player:
            arcade.stop_sound(self.background_music_player)
            self.background_music_player = None
        if self.dance_music_player:
            arcade.stop_sound(self.dance_music_player)
            self.dance_music_player = None

        if not self.dance_music:
            try:
                self.dance_music = arcade.load_sound(self.dance_music_file)
            except Exception as e:
                print(f"Error loading dance music: {e}")
        if self.current_level in self.background_music_files:
            try:
                self.background_music = arcade.load_sound(self.background_music_files[self.current_level])
                self.background_music_player = arcade.play_sound(self.background_music, volume=0.0, loop=True)
                self.fade_in_player = self.background_music_player
                self.fade_in_timer = self.fade_in_duration
                self.fade_in_target_volume = self.background_music_volume
            except Exception as e:
                print(f"Error loading background music for level {self.current_level}: {e}")

    def _stop_all_music(self, immediate=False):
        """Stop all currently playing music, with optional immediate stop."""
        if immediate:
            # Immediately stop all sounds, bypassing fade
            if self.background_music_player:
                arcade.stop_sound(self.background_music_player)
                self.background_music_player = None
            if self.dance_music_player:
                arcade.stop_sound(self.dance_music_player)
                self.dance_music_player = None
            if self.fade_out_player:
                arcade.stop_sound(self.fade_out_player)
                self.fade_out_player = None
            self.fade_out_timer = 0
        else:
            # Initiate fade-out
            if self.background_music_player:
                self.fade_out_player = self.background_music_player
                self.fade_out_timer = self.fade_out_duration
                self.background_music_player = None
            if self.dance_music_player:
                self.fade_out_player = self.dance_music_player
                self.fade_out_timer = self.fade_out_duration
                self.dance_music_player = None

    def _setup_lighting(self):
        """Set up lighting for level 2."""
        if self.current_level == 2:
            self.light_layer = LightLayer(WINDOW_WIDTH, WINDOW_HEIGHT)
            self.light_layer.set_background_color(arcade.color.BLACK)
            self.player_light = Light(
                0, 0,
                radius=SPOTLIGHT_RADIUS,
                color=SPOTLIGHT_COLOR,
                mode='soft'
            )
            self.light_layer.add(self.player_light)
        else:
            self.light_layer = None
            self.player_light = None

    def _load_dance_textures(self):
        """Load the dance animation textures."""
        self.dance_textures = []
        for i in range(1, 5):
            texture_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                f"assets/Sprites/shakira_dance{i}.png"
            )
            texture = arcade.load_texture(texture_path)
            self.dance_textures.append(texture)

    def _setup_ui(self):
        """Set up UI text elements."""
        self.score_text = arcade.Text(
            "Score: 0",
            x=WINDOW_WIDTH - 10,
            y=WINDOW_HEIGHT - 50,
            color=arcade.color.BLACK,
            font_size=20,
            anchor_x="right"
        )

    def _load_level(self, level_number):
        """Load a specific level by number."""
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
        self.terrain_list = self.tile_map.sprite_lists.get("Terrain")
        self.coin_list = self.tile_map.sprite_lists.get("Collectibles")
        self.obstacle_list = self.tile_map.sprite_lists.get("Obstacles")
        player_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   "assets/Sprites/shakira.png")
        self.player_sprite = arcade.Sprite(player_path, scale=PLAYER_SCALING)
        self.player_sprite.center_x = GRID_PIXEL_SIZE * 2
        self.player_sprite.center_y = (self.tile_map.height * GRID_PIXEL_SIZE -
                                       GRID_PIXEL_SIZE * 2 + 128)
        self.player_visual_angle = 0
        self.player_sprite.angle = 0
        self.player_state = SKIING
        self.flip_rotation = 0
        self.bonus_message = None
        self.bonus_timer = 0
        self.player_list.append(self.player_sprite)
        self._setup_lighting()
        self._setup_sounds()

    def _setup_cameras(self):
        """Set up game cameras."""
        self.camera = arcade.Camera2D()
        self.gui_camera = arcade.Camera2D()
        if self.tile_map:
            max_x = GRID_PIXEL_SIZE * self.tile_map.width
            max_y = GRID_PIXEL_SIZE * self.tile_map.height
        else:
            max_x = 5000
            max_y = 2000
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
        """Set up the Pymunk physics engine."""
        self.physics_engine = arcade.PymunkPhysicsEngine(
            damping=DEFAULT_DAMPING,
            gravity=(0, -GRAVITY)
        )
        self.physics_engine.add_sprite(
            self.player_sprite,
            friction=PLAYER_FRICTION,
            mass=PLAYER_MASS,
            moment_of_inertia=arcade.PymunkPhysicsEngine.MOMENT_INF,
            collision_type="player",
            max_horizontal_velocity=PLAYER_MAX_HORIZONTAL_SPEED,
            max_vertical_velocity=PLAYER_MAX_VERTICAL_SPEED,
        )
        if self.terrain_list:
            self.physics_engine.add_sprite_list(
                self.terrain_list,
                friction=WALL_FRICTION,
                collision_type="wall",
                body_type=arcade.PymunkPhysicsEngine.STATIC,
            )
        if self.obstacle_list:
            self.physics_engine.add_sprite_list(
                self.obstacle_list,
                friction=DYNAMIC_ITEM_FRICTION,
                collision_type="item"
            )
        self.physics_engine.add_collision_handler("player", "wall", post_handler=self.terrain_collision_handler)

    def terrain_collision_handler(self, sprite_a, sprite_b, arbiter, space, data):
        """Handle collisions between player and terrain."""
        normal = arbiter.normal
        self.terrain_angle = math.degrees(math.atan2(-normal.x, normal.y))
        return True

    def on_draw(self):
        """Render the screen."""
        self.clear()
        self.camera.use()
        if self.current_level == 2 and self.light_layer:
            with self.light_layer:
                self._draw_game_elements()
            self.light_layer.draw(ambient_color=AMBIENT_LIGHT_COLOR)
        else:
            arcade.set_background_color(arcade.color.SKY_BLUE)
            self._draw_game_elements()
        self.gui_camera.use()
        self._draw_ui_elements()

    def _draw_game_elements(self):
        """Draw all game elements."""
        if self.terrain_list:
            self.terrain_list.draw()
        if self.coin_list:
            self.coin_list.draw()
        if self.obstacle_list:
            self.obstacle_list.draw()
        self.player_sprite.angle = self.player_visual_angle
        self.player_list.draw()

    def _draw_ui_elements(self):
        """Draw all UI elements."""
        self.score_text.text = f"Score: {self.score}"
        self.score_text.draw()
        if self.bonus_message and self.bonus_timer > 0:
            alpha = int(255 * (self.bonus_timer / BONUS_MESSAGE_DURATION))
            self.bonus_message.color = (arcade.color.GREEN[0], arcade.color.GREEN[1], arcade.color.GREEN[2], alpha)
            self.bonus_message.draw()
        if self.level_complete:
            if self.current_level < self.max_level:
                arcade.draw_text(
                    "Nailed it! Level complete.",
                    self.window.width // 2,
                    self.window.height // 2,
                    arcade.color.GREEN,
                    40,
                    anchor_x="center"
                )
                arcade.draw_text(
                    "Press N to continue the journey!",
                    self.window.width // 2,
                    self.window.height // 2 - 75,
                    arcade.color.GREEN,
                    25,
                    anchor_x="center"
                )
            else:
                arcade.draw_text(
                    "Whenever, wherever, you're a skiing champion!",
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
                "Looks like your hips don't lie... about needing another try! Game Over.",
                self.window.width // 2,
                self.window.height // 2,
                arcade.color.RED,
                25,
                anchor_x="center"
            )
            arcade.draw_text(
                "Press R to restart",
                self.window.width // 2,
                self.window.height // 2 - 27,
                arcade.color.RED,
                20,
                anchor_x="center"
            )

    def on_key_press(self, key, modifiers):
        """Handle key press events."""
        if self.game_over:
            if key == arcade.key.R:
                self.score = 0
                self.setup()
                return
        elif self.level_complete:
            if key == arcade.key.N and self.current_level < self.max_level:
                self.current_level += 1
                self.player_list = arcade.SpriteList()
                self.setup()
                return
        else:
            if key == arcade.key.SPACE:
                if self.physics_engine.is_on_ground(self.player_sprite):
                    impulse = (0, PLAYER_JUMP_IMPULSE)
                    self.physics_engine.apply_impulse(self.player_sprite, impulse)
                    self.player_state = JUMPING
            elif key == arcade.key.LEFT:
                self.left_pressed = True
            elif key == arcade.key.RIGHT:
                self.right_pressed = True
        if key == arcade.key.ESCAPE:
            pause_view = PauseView(self)
            self.window.show_view(pause_view)

    def on_key_release(self, key, modifiers):
        """Handle key release events."""
        if key == arcade.key.SPACE:
            self.jump_needs_reset = False
        elif key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False

    def on_update(self, delta_time):
        """Update game state and logic."""
        # Handle fade-out
        if self.fade_out_player and self.fade_out_timer > 0:
            self.fade_out_timer -= delta_time
            if self.fade_out_timer <= 0:
                arcade.stop_sound(self.fade_out_player)
                self.fade_out_player = None
                self.fade_out_timer = 0
            else:
                volume = (self.fade_out_timer / self.fade_out_duration)
                self.fade_out_player.volume = volume * (self.background_music_volume if self.fade_out_player == self.background_music_player else self.dance_music_volume)

        # Handle fade-in
        if self.fade_in_player and self.fade_in_timer > 0:
            self.fade_in_timer -= delta_time
            if self.fade_in_timer <= 0:
                self.fade_in_player.volume = self.fade_in_target_volume
                self.fade_in_player = None
                self.fade_in_timer = 0
            else:
                volume = 1 - (self.fade_in_timer / self.fade_in_duration)
                self.fade_in_player.volume = volume * self.fade_in_target_volume

        if self.game_over:
            return
        if self.level_complete:
            self._update_dance_animation(delta_time)
            return
        self._check_end_conditions()
        if self.game_over or self.level_complete:
            if self.level_complete:
                self.player_state = DANCING
                self.dance_start_time = time.time()
                self.current_dance_frame = 0
                self.dance_timer = 0
                if self.dance_textures and len(self.dance_textures) > 0:
                    self.player_sprite.texture = self.dance_textures[0]
            return
        self._update_player_state(delta_time)
        self._handle_collisions()
        self._update_lighting()
        self.pan_camera_to_user(CAMERA_PAN_SPEED)
        if self.bonus_timer > 0:
            self.bonus_timer -= delta_time
            if self.bonus_timer <= 0:
                self.bonus_message = None

    def _update_lighting(self):
        """Update the position of the player's spotlight."""
        if self.current_level == 2 and self.player_light:
            self.player_light.position = (self.player_sprite.center_x+200, self.player_sprite.center_y)

    def _update_dance_animation(self, delta_time):
        """Update the dance animation frames."""
        if self.player_state != DANCING:
            return
        self.dance_timer += delta_time
        if self.dance_timer >= DANCE_ANIMATION_SPEED:
            self.dance_timer = 0
            self.current_dance_frame = (self.current_dance_frame + 1) % len(self.dance_textures)
            if self.dance_textures and len(self.dance_textures) > 0:
                self.player_sprite.texture = self.dance_textures[self.current_dance_frame]

    def _check_end_conditions(self):
        """Check if any end conditions are met."""
        if self.player_sprite.right >= self.end_of_map:
            self.level_complete = True
            self.player_state = DANCING
            self.dance_start_time = time.time()
            self.current_dance_frame = 0
            self.dance_timer = 0
            if self.dance_textures and len(self.dance_textures) > 0:
                self.player_sprite.texture = self.dance_textures[0]
            self._stop_all_music()
            if self.dance_music:
                self.dance_music_player = arcade.play_sound(self.dance_music, volume=0.0, loop=True)
                self.fade_in_player = self.dance_music_player
                self.fade_in_timer = self.fade_in_duration
                self.fade_in_target_volume = self.dance_music_volume
            return
        if self.player_sprite.center_y < -100:
            self.game_over = True
            self.player_state = GAME_OVER
            self._stop_all_music()
            return

    def _update_player_state(self, delta_time):
        """Update player state and physics."""
        is_on_ground = self.physics_engine.is_on_ground(self.player_sprite)
        if not is_on_ground and self.player_state != GAME_OVER:
            self.player_state = JUMPING
        if is_on_ground and self.player_state == SKIING:
            self.player_visual_angle = 180 - self.terrain_angle
        elif not is_on_ground and self.player_state == JUMPING:
            if self.left_pressed:
                rotation = -FLIP_SPEED * delta_time
                self.player_visual_angle += rotation
                self.flip_rotation += rotation
            if self.right_pressed:
                rotation = FLIP_SPEED * delta_time
                self.player_visual_angle += rotation
                self.flip_rotation += rotation
            self.player_visual_angle %= 360
            if self.player_visual_angle < 0:
                self.player_visual_angle += 360
        if is_on_ground and not self.was_on_ground:
            angle = self.player_visual_angle % 360
            if 135 <= angle <= 225:
                self.game_over = True
                self.player_state = GAME_OVER
                self.flip_rotation = 0
                self._stop_all_music()
                return
            else:
                flips = math.floor(abs(self.flip_rotation) / FLIP_THRESHOLD)
                if flips > 0:
                    bonus_points = flips * POINTS_PER_FLIP
                    self.score += bonus_points
                    self.bonus_message = arcade.Text(
                        f"Flip Bonus: +{bonus_points} points",
                        x=WINDOW_WIDTH - 10,
                        y=WINDOW_HEIGHT - 80,
                        color=arcade.color.GREEN,
                        font_size=20,
                        anchor_x="right"
                    )
                    self.bonus_timer = BONUS_MESSAGE_DURATION
                self.player_visual_angle = 180 - self.terrain_angle
                self.flip_rotation = 0
                self.player_state = SKIING
        self.was_on_ground = is_on_ground
        if is_on_ground:
            force = (PLAYER_MOVE_FORCE_ON_GROUND, 0)
        else:
            force = (PLAYER_MOVE_FORCE_IN_AIR, 0)
        self.physics_engine.apply_force(self.player_sprite, force)
        self.physics_engine.set_friction(self.player_sprite, 0)
        self.physics_engine.step()

    def _handle_collisions(self):
        """Handle collisions with coins and obstacles."""
        if self.coin_list:
            coins_hit = arcade.check_for_collision_with_list(
                self.player_sprite, self.coin_list
            )
            for coin in coins_hit:
                coin.remove_from_sprite_lists()
                self.score += 5
        if self.obstacle_list:
            obstacle_hit_list = arcade.check_for_collision_with_list(
                self.player_sprite, self.obstacle_list
            )
            if len(obstacle_hit_list) > 0:
                self.game_over = True
                self.player_state = GAME_OVER
                self._stop_all_music()

    def pan_camera_to_user(self, panning_fraction: float = 1.0):
        """Pan camera to follow the player."""
        screen_center_x, screen_center_y = self.player_sprite.position
        if screen_center_x < self.camera.viewport_width / 2:
            screen_center_x = self.camera.viewport_width / 2
        if screen_center_y < self.camera.viewport_height / 2:
            screen_center_y = self.camera.viewport_height / 2
        user_centered = screen_center_x, screen_center_y
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
        self.window.background_color = arcade.color.WHITE
        self.game_view._stop_all_music()

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
            "Ready to waka waka back into the action?",
            WINDOW_WIDTH / 2,
            WINDOW_HEIGHT / 2 + 50,
            arcade.color.BLACK,
            font_size=50,
            anchor_x="center"
        )
        arcade.draw_text(
            "Press Esc. to Unpause",
            WINDOW_WIDTH / 2,
            WINDOW_HEIGHT / 2,
            arcade.color.BLACK,
            font_size=20,
            anchor_x="center"
        )

    def on_key_press(self, key, _modifiers):
        """Handle key press events in pause screen."""
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.game_view)
            self.game_view._setup_sounds()

def main():
    """Main function to start the game."""
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    game = GameView()
    window.show_view(game)
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()