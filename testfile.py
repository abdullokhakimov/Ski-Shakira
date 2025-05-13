import arcade
import os
import time

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


# --- Physics forces. Higher number, faster accelerating.

# Gravity
GRAVITY = 2500

# Damping - Amount of speed lost per second
DEFAULT_DAMPING = 0.05
PLAYER_DAMPING = 0.03

# Friction between objects
PLAYER_FRICTION = 0.01
WALL_FRICTION = 0.2
DYNAMIC_ITEM_FRICTION = 0.3

# Mass (defaults to 1)
PLAYER_MASS = 1.5

# Keep player from going too fast
PLAYER_MAX_HORIZONTAL_SPEED = 1500
PLAYER_MAX_VERTICAL_SPEED = 1800

# Force applied while on the ground
PLAYER_MOVE_FORCE_ON_GROUND = 1500

# Force applied when moving left/right in the air
PLAYER_MOVE_FORCE_IN_AIR = 1000

# Strength of a jump
PLAYER_JUMP_IMPULSE = 1600

class GameView(arcade.View):
    """Main application class."""

    def __init__(self):
        """
        Initializer
        """
        super().__init__()

        # Tilemap Object
        self.tile_map = None

        # Sprite lists
        self.player_list = None
        self.terrain_list = None
        self.coin_list = None
        self.obstacle_list = None

        # Set up the player
        self.score = 0
        self.player_sprite = None
        self.player_rotation = 0  # Tracks rotation in degrees
        self.player_state = SKIING

        # Control keys
        self.left_pressed = False
        self.right_pressed = False
        self.jump_needs_reset = False

        self.end_of_map = 0
        self.game_over = False
        self.last_time = None
        self.frame_count = 0

        # Cameras
        self.camera = None
        self.camera_bounds = None
        self.gui_camera = None

        # Text
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

        # Track the current state of what key is pressed
        self.left_pressed: bool = False
        self.right_pressed: bool = False

        # Physics engine
        self.physics_engine: arcade.PymunkPhysicsEngine | None = None

        # Set background color
        self.background_color = arcade.color.SKY_BLUE

    def setup(self):
        """Set up the game and initialize the variables."""

        # Sprite lists
        self.player_list = arcade.SpriteList()

        # Try to load your map file - use current directory path instead of hardcoded
        try:
            map_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Probe.tmj")

            layer_options = {
                "Platforms": {"use_spatial_hash": True},
                "Obstacles": {"use_spatial_hash": True},
                "Coins": {"use_spatial_hash": True}
            }

            # Read in the tiled map
            self.tile_map = arcade.load_tilemap(
                map_name, layer_options=layer_options, scaling=TILE_SCALING
            )
            self.end_of_map = self.tile_map.width * GRID_PIXEL_SIZE

            # Set up the terrain, obstacles, and collectibles layers
            self.terrain_list = self.tile_map.sprite_lists.get("Terrain")
            self.coin_list = self.tile_map.sprite_lists.get("Collectibles")
            self.obstacle_list = self.tile_map.sprite_lists.get("Obstacles")

            # Set up the player - use built-in resource instead of file
            self.player_sprite = arcade.Sprite(
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets/Sprites/shakira.png"),
                scale=PLAYER_SCALING,
            )

            # Position player at top left of the map with a small offset
            # The player should be positioned on top of terrain
            self.player_sprite.center_x = GRID_PIXEL_SIZE * 2  # Small offset from left edge
            self.player_sprite.center_y = self.tile_map.height * GRID_PIXEL_SIZE - GRID_PIXEL_SIZE * 2 +128  # Near top edge

            self.player_rotation = 0
            self.player_state = SKIING
            self.player_list.append(self.player_sprite)

            # Set up physics engine
            if self.terrain_list:
                self.physics_engine = arcade.PhysicsEnginePlatformer(
                    self.player_sprite,
                    gravity_constant=GRAVITY,
                    walls=self.terrain_list
                )
            else:
                print("Warning: No terrain layer found in the map")
                # Create a basic physics engine with no walls
                self.physics_engine = arcade.PhysicsEnginePlatformer(
                    self.player_sprite,
                    gravity_constant=GRAVITY,
                    walls=arcade.SpriteList()
                )

        except Exception as e:
            print(f"Error loading map: {e}")
            # Create a basic scene if map loading fails
            self.terrain_list = arcade.SpriteList(use_spatial_hash=True)
            self.coin_list = arcade.SpriteList(use_spatial_hash=True)
            self.obstacle_list = arcade.SpriteList(use_spatial_hash=True)

            # Create basic player
            self.player_sprite = arcade.Sprite(
                ":resources:images/animated_characters/female_person/femalePerson_idle.png",
                scale=PLAYER_SCALING,
            )
            self.player_sprite.center_x = GRID_PIXEL_SIZE * 2
            self.player_sprite.center_y = WINDOW_HEIGHT - GRID_PIXEL_SIZE * 2
            self.player_list.append(self.player_sprite)

            # Create a basic physics engine with no walls
            self.physics_engine = arcade.PhysicsEnginePlatformer(
                self.player_sprite,
                gravity_constant=GRAVITY,
                walls=arcade.SpriteList()
            )

        # Set up the camera and camera bounds
        self.camera = arcade.Camera2D()
        self.gui_camera = arcade.Camera2D()

        # Use the tilemap to limit the camera's position, or use default values if tilemap isn't loaded
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

        # Set initial camera position to top left of map
        if self.tile_map:
            # Calculate position for top-left view
            left_edge = self.window.width / 2.0  # Half window from left edge
            top_edge = max_y - self.window.height / 2.0  # Top edge minus half window height

            # Set camera position directly instead of panning
            self.camera.position = (left_edge, top_edge)

        # After setting the initial camera position, call pan to player
        self.pan_camera_to_user(1.0)  # Use full panning to quickly move to player
        self.game_over = False

        # --- Pymunk Physics Engine Setup ---

        # The default damping for every object controls the percent of velocity
        # the object will keep each second. A value of 1.0 is no speed loss,
        # 0.9 is 10% per second, 0.1 is 90% per second.
        # For top-down games, this is basically the friction for moving objects.
        # For platformers with gravity, this should probably be set to 1.0.
        # Default value is 1.0 if not specified.
        damping = DEFAULT_DAMPING

        # Set the gravity. (0, 0) is good for outer space and top-down.
        gravity = (0, -GRAVITY)

        # Create the physics engine
        self.physics_engine = arcade.PymunkPhysicsEngine(damping=damping, gravity=gravity)

        # Add the player.
        # For the player, we set the damping to a lower value, which increases
        # the damping rate. This prevents the character from traveling too far
        # after the player lets off the movement keys.
        # Setting the moment of inertia to PymunkPhysicsEngine.MOMENT_INF prevents it from
        # rotating.
        # Friction normally goes between 0 (no friction) and 1.0 (high friction)
        # Friction is between two objects in contact. It is important to remember
        # in top-down games that friction moving along the 'floor' is controlled
        # by damping.
        self.physics_engine.add_sprite(
            self.player_sprite,
            friction=PLAYER_FRICTION,
            mass=PLAYER_MASS,
            moment_of_inertia=arcade.PymunkPhysicsEngine.MOMENT_INF,
            collision_type="player",
            max_horizontal_velocity=PLAYER_MAX_HORIZONTAL_SPEED,
            max_vertical_velocity=PLAYER_MAX_VERTICAL_SPEED,
        )

        # Create the walls.
        # By setting the body type to PymunkPhysicsEngine.STATIC the walls can't
        # move.
        # Movable objects that respond to forces are PymunkPhysicsEngine.DYNAMIC
        # PymunkPhysicsEngine.KINEMATIC objects will move, but are assumed to be
        # repositioned by code and don't respond to physics forces.
        # Dynamic is default.
        self.physics_engine.add_sprite_list(
            self.terrain_list,
            friction=WALL_FRICTION,
            collision_type="wall",
            body_type=arcade.PymunkPhysicsEngine.STATIC,
        )

        # Create the items
        self.physics_engine.add_sprite_list(
            self.obstacle_list, friction=DYNAMIC_ITEM_FRICTION, collision_type="item"
        )

    def on_draw(self):
        """
        Render the screen.
        """

        # Set background color to blue
        arcade.set_background_color(arcade.color.SKY_BLUE)

        # This command has to happen before we start drawing
        self.camera.use()
        self.clear()

        # Start counting frames
        self.frame_count += 1

        # Draw all the sprites
        if self.terrain_list:
            self.terrain_list.draw()
        if self.coin_list:
            self.coin_list.draw()
        if self.obstacle_list:
            self.obstacle_list.draw()
        self.player_list.draw()

        # Activate GUI camera for FPS, distance and hit boxes
        self.gui_camera.use()

        # Calculate FPS if conditions are met
        if self.last_time and self.frame_count % 60 == 0:
            fps = round(1.0 / (time.time() - self.last_time) * 60)
            self.fps_text.text = f"FPS: {fps:3d}"

        # Draw FPS text
        self.fps_text.draw()

        # Get time for every 60 frames
        if self.frame_count % 60 == 0:
            self.last_time = time.time()

        # Get distance and draw text
        distance = self.player_sprite.right
        self.distance_text.text = f"Distance: {distance:.1f}"
        self.distance_text.draw()

        # Draw score
        self.score_text.text = f"Score: {self.score}"
        self.score_text.draw()

        # Draw game over text if condition met
        if self.game_over:
            arcade.draw_text(
                "Game Over - Press R to Restart",
                self.window.width // 2,
                self.window.height // 2,
                arcade.color.RED,
                30,
                anchor_x="center"
            )

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""
        if self.game_over:
            if key == arcade.key.R:
                self.setup()
                self.score = 0
                return

        elif key == arcade.key.SPACE:
            # find out if player is standing on ground
            if self.physics_engine.is_on_ground(self.player_sprite):
                # She is! Go ahead and jump
                impulse = (0, PLAYER_JUMP_IMPULSE)
                self.physics_engine.apply_impulse(self.player_sprite, impulse)

        if key == arcade.key.ESCAPE:
            # pass self, the current view, to preserve this view's state
            pause = PauseView(self)
            self.window.show_view(pause)

    def on_key_release(self, key, modifiers):
        """Called whenever a key is released."""
        if key == arcade.key.SPACE:
            self.jump_needs_reset = False

    # def update_player_rotation(self):
    #     """Update player rotation based on keys and state."""
    #     if self.player_state == JUMPING:
    #         # Apply rotation only when jumping
    #         if self.left_pressed:
    #             self.player_rotation -= ROTATION_SPEED
    #         if self.right_pressed:
    #             self.player_rotation += ROTATION_SPEED
    #
    #         # Keep rotation between 0 and 360 degrees
    #         self.player_rotation %= 360
    #
    #         # Update the sprite's rotation
    #         self.player_sprite.angle = self.player_rotation
    #     elif self.player_state == SKIING and self.physics_engine.can_jump():
    #         # Check if landing was bad (not upright)
    #         # We consider "upright" to be within 45 degrees of 0 or 360
    #         upright_angle = (self.player_rotation % 360)
    #         if not (upright_angle < 45 or upright_angle > 315):
    #             # Bad landing - game over!
    #             self.game_over = True
    #         else:
    #             # Good landing - reset rotation to zero
    #             self.player_rotation = 0
    #             self.player_sprite.angle = 0

    def on_update(self, delta_time):
        """Movement and game logic"""
        is_on_ground = self.physics_engine.is_on_ground(self.player_sprite)

        # Check for game over conditions
        if (self.player_sprite.right >= self.end_of_map or
                self.player_sprite.center_y < -100 or
                self.game_over):
            self.game_over = True
            return

        # Check if player is jumping or skiing
        # if self.physics_engine:
        #     if not self.physics_engine.can_jump():
        #         self.player_state = JUMPING
        #     else:
        #         if self.player_state == JUMPING:
        #             # Player just landed
        #             self.player_state = SKIING

        # Update player rotation
        # self.update_player_rotation()


        # Update physics engine
        # if self.physics_engine:
        #     self.physics_engine.update()

        # Check for collectible collisions
        if self.coin_list:
            coins_hit = arcade.check_for_collision_with_list(
                self.player_sprite, self.coin_list
            )

            for coin in coins_hit:
                coin.remove_from_sprite_lists()
                self.score += 1

        # Check for obstacle collisions
        if self.obstacle_list:
            obstacle_hit_list = arcade.check_for_collision_with_list(
                self.player_sprite, self.obstacle_list
            )

            if len(obstacle_hit_list) > 0:
                self.game_over = True

        # Pan to the user
        self.pan_camera_to_user(CAMERA_PAN_SPEED)

        """Movement and game logic"""
        # self.physics_engine.set_velocity(self.player_sprite, (MOVEMENT_SPEED, self.player_sprite.change_y))
        if is_on_ground:
            force = (PLAYER_MOVE_FORCE_ON_GROUND, 0)
        else:
            force = (PLAYER_MOVE_FORCE_IN_AIR, 0)
        self.physics_engine.apply_force(self.player_sprite, force)
        # Set friction to zero for the player while moving
        self.physics_engine.set_friction(self.player_sprite, 0)

        self.physics_engine.step()

    def pan_camera_to_user(self, panning_fraction: float = 1.0):
        """
        Manage Scrolling

        Args:
            panning_fraction:
                Number from 0 to 1. Higher the number, faster we
                pan the camera to the user.
        """

        # This spot would center on the user
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
    # def pan_camera_to_user(self, panning_fraction: float = 1.0):
    #     """ Manage Scrolling """
    #     # Make sure player sprite exists
    #     if not hasattr(self, 'player_sprite') or self.player_sprite is None:
    #         return
    #
    #     self.camera.position = arcade.math.smerp_2d(
    #         self.camera.position,
    #         self.player_sprite.position,
    #         self.window.delta_time,
    #         panning_fraction,
    #     )
    #
    #     if hasattr(self, 'camera_bounds') and self.camera_bounds is not None:
    #         self.camera.position = arcade.camera.grips.constrain_xy(
    #             self.camera.view_data,
    #             self.camera_bounds
    #         )

class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

    def on_show_view(self):
        self.window.background_color = arcade.color.WHITE_SMOKE

    def on_draw(self):
        self.clear()

        # Draw player, for effect, on pause screen.
        # The previous View (GameView) was passed in
        # and saved in self.game_view.
        player_sprite = self.game_view.player_sprite
        arcade.draw_sprite(player_sprite)

        # draw an orange filter over him
        arcade.draw_lrbt_rectangle_filled(left=player_sprite.left,
                                          right=player_sprite.right,
                                          bottom=player_sprite.bottom,
                                          top=player_sprite.top,
                                          color=arcade.color.ORANGE[:3] + (200,))

        arcade.draw_text("PAUSED", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 50,
                         arcade.color.BLACK, font_size=50, anchor_x="center")

        # Show tip to return or reset
        arcade.draw_text("Press Esc. to return",
                         WINDOW_WIDTH / 2,
                         WINDOW_HEIGHT / 2,
                         arcade.color.BLACK,
                         font_size=20,
                         anchor_x="center")

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:   # resume game
            self.window.show_view(self.game_view)


def main():
    """Main function"""
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    game = GameView()
    window.show_view(game)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
