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
CAMERA_PAN_SPEED = 0.30

# Physics
MOVEMENT_SPEED = 5
JUMP_SPEED = 20
ROTATION_SPEED = 5
GRAVITY = 0.8

# Player states
SKIING = 0
JUMPING = 1
GAME_OVER = 2


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

        self.physics_engine = None
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

    def setup(self):
        """Set up the game and initialize the variables."""

        # Sprite lists
        self.player_list = arcade.SpriteList()

        # Try to load your map file - use current directory path instead of hardcoded
        try:
            map_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "map/Level1.tmj")

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
                ":resources:images/animated_characters/female_person/femalePerson_idle.png",
                scale=PLAYER_SCALING,
            )

            # Position player at top left of the map with a small offset
            # The player should be positioned on top of terrain
            self.player_sprite.center_x = GRID_PIXEL_SIZE * 2  # Small offset from left edge
            self.player_sprite.center_y = self.tile_map.height * GRID_PIXEL_SIZE - GRID_PIXEL_SIZE * 2  # Near top edge

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

        if key == arcade.key.SPACE:
            if self.physics_engine and self.physics_engine.can_jump() and not self.jump_needs_reset:
                self.player_sprite.change_y = JUMP_SPEED
                self.player_state = JUMPING
                self.jump_needs_reset = True
        elif key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True

        if key == arcade.key.ESCAPE:
            # pass self, the current view, to preserve this view's state
            pause = PauseView(self)
            self.window.show_view(pause)

    def on_key_release(self, key, modifiers):
        """Called whenever a key is released."""
        if key == arcade.key.SPACE:
            self.jump_needs_reset = False
        elif key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False

    def update_player_rotation(self):
        """Update player rotation based on keys and state."""
        if self.player_state == JUMPING:
            # Apply rotation only when jumping
            if self.left_pressed:
                self.player_rotation -= ROTATION_SPEED
            if self.right_pressed:
                self.player_rotation += ROTATION_SPEED

            # Keep rotation between 0 and 360 degrees
            self.player_rotation %= 360

            # Update the sprite's rotation
            self.player_sprite.angle = self.player_rotation
        elif self.player_state == SKIING and self.physics_engine.can_jump():
            # Check if landing was bad (not upright)
            # We consider "upright" to be within 45 degrees of 0 or 360
            upright_angle = (self.player_rotation % 360)
            if not (upright_angle < 45 or upright_angle > 315):
                # Bad landing - game over!
                self.game_over = True
            else:
                # Good landing - reset rotation to zero
                self.player_rotation = 0
                self.player_sprite.angle = 0

    def on_update(self, delta_time):
        """Movement and game logic"""
        # Check for game over conditions
        if (self.player_sprite.right >= self.end_of_map or
                self.player_sprite.center_y < -100 or
                self.game_over):
            self.game_over = True
            return

        # Check if player is jumping or skiing
        if self.physics_engine:
            if not self.physics_engine.can_jump():
                self.player_state = JUMPING
            else:
                if self.player_state == JUMPING:
                    # Player just landed
                    self.player_state = SKIING

        # Update player rotation
        self.update_player_rotation()

        # Automatic forward movement
        self.player_sprite.change_x = MOVEMENT_SPEED

        # Update physics engine
        if self.physics_engine:
            self.physics_engine.update()

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

    def pan_camera_to_user(self, panning_fraction: float = 1.0):
        """ Manage Scrolling """
        # Make sure player sprite exists
        if not hasattr(self, 'player_sprite') or self.player_sprite is None:
            return

        self.camera.position = arcade.math.smerp_2d(
            self.camera.position,
            self.player_sprite.position,
            self.window.delta_time,
            panning_fraction,
        )

        if hasattr(self, 'camera_bounds') and self.camera_bounds is not None:
            self.camera.position = arcade.camera.grips.constrain_xy(
                self.camera.view_data,
                self.camera_bounds
            )

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
