# Implementierung des Spiels "Ski Shakira"

Hier berichtet der Lead-Developer Koustav Agrawal.

## Codestruktur

* **Wurde der Prototyp weiterentwickelt oder "from Scratch" begonnen?**  
  Mehrere Arcade-Beispiele wurden mit eigenen (von Grund auf entwickelten) Konzepten kombiniert. Diese Kombination ermöglichte es uns, bewährte Praktiken zu nutzen und gleichzeitig innovative Spielmechaniken zu implementieren.

* **Wie ist der Code organisiert?**  
  Der Code ist objektorientiert aufgebaut und folgt dem View-Pattern der Arcade-Bibliothek:
  - Ein Konstantenbereich am Anfang für einfache Anpassungen aller Spielparameter
  - Die Hauptklasse `GameView` verwaltet das Spielgeschehen, die Physik und alle Spielelemente
  - Eine separate `PauseView`-Klasse übernimmt die Darstellung des Pause-Bildschirms
  - Die `main()`-Funktion initialisiert das Spielfenster und startet die Anwendung
  - Verschiedene Setup- und Update-Methoden sind für bessere Lesbarkeit und Wartbarkeit getrennt implementiert

* **Welche wichtigen Klassen und Funktionen gibt es?**
  - **GameView**: Hauptspielklasse, verwaltet das gesamte Spielgeschehen
    - `setup()`: Initialisiert alle Spielelemente
    ```python
    def setup(self):
        """Set up the game and initialize variables."""
        self._stop_all_music(immediate=True)
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
    ```
    - `_load_level()`: Lädt Level aus Tiled-Karten
    - `_update_player_state()`: Steuert die Spielerphysik und -bewegung
    - `_handle_collisions()`: Erkennt und verarbeitet Kollisionen
    - `_update_dance_animation()`: Animiert den Spieler bei Level-Abschluss
    - `pan_camera_to_user()`: Bewegt die Kamera mit dem Spieler durch Interpolation
    ```python
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
    ```
  - **PauseView**: Zeigt den Pausebildschirm an
  - Verschiedene Handler für Tastatureingaben und Kollisionen
  - Zustandsmanagement für den Spieler (SKIING, JUMPING, GAME_OVER, LEVEL_COMPLETE, DANCING)

## Implementierte Features

* **Welche technischen Features wurden umgesetzt?**
  - Physikbasierte Bewegung mit der Pymunk-Engine
  - Raycasting für präzise Terrainkollisionserkennung
  - Interpolation für flüssige Kamerabewegungen und Animation
  - Dynamische Kameraführung, die dem Spieler folgt
  - Mehrere Level mit unterschiedlichem Schwierigkeitsgrad
  - Dynamisches Beleuchtungssystem im zweiten Level, realisiert durch die Lichtfunktionen der Arcade-Bibliothek und nicht durch die Tiled-Map
  - Flüssige Animation des Spielercharakters
  - Kollisionserkennung mit Terrain, Münzen und Hindernissen
  - Terrrainabhängige Spielerbewegung (Skifahren)
  - Ausgefeiltes Spielerzustandssystem (SKIING, JUMPING, GAME_OVER, LEVEL_COMPLETE, DANCING)
  - Punktesystem mit Bonus für Saltos
  - Musik mit sanftem Ein- und Ausblenden
  - Tilemap-Integration für Level-Design
  ```python
  # Spielerzustände
  SKIING = 0
  JUMPING = 1
  GAME_OVER = 2
  LEVEL_COMPLETE = 3
  DANCING = 4
  ```

* **Welche besonderen Herausforderungen gab es dabei?**
  - Die Implementierung der Sprung- und Salto-Mechanik war komplex, da wir die richtige Balance zwischen Spielbarkeit und realistischer Physik finden mussten
  - Das Beleuchtungssystem im zweiten Level erforderte eine sorgfältige Abstimmung
  - Die Kollisionserkennung zwischen Spieler und Terrain musste präzise sein, um das Gleiten auf verschiedenen Winkeln zu ermöglichen
  - Das sanfte Ein- und Ausblenden der Musik bei Levelwechseln und Spielzuständen erforderte ein komplexes Audiosystem
  - Die Integration der neueren Arcade-Version mit Pymunk stellte eine besondere Herausforderung dar, da viele Dokumentationen und Beispiele noch für ältere Versionen konzipiert waren

* **Lösungen, auf die Sie besonders stolz sind:**
  - Die Implementierung von Raycasting für präzise Terrainkollision:
  ```python
  def terrain_collision_handler(self, sprite_a, sprite_b, arbiter, space, data):
      """Handle collisions between player and terrain."""
      normal = arbiter.normal
      self.terrain_angle = math.degrees(math.atan2(-normal.x, normal.y))
      return True
  ```
  - Die Interpolation für flüssige Kamerabewegungen durch die Verwendung von `lerp_2d`
  - Die Integration der Pymunk-Physik-Engine, die weit über die Projektanforderungen hinausging:
  ```python
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
  ```
  - Die Verwendung der os-Bibliothek für plattformunabhängige Dateipfade:
  ```python
  map_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"map/Level{level_number}.tmj")
  ```
  - Das System zur Erkennung und Bewertung von Saltos während des Sprungs:
  ```python
  if is_on_ground and not self.was_on_ground:
      angle = self.player_visual_angle % 360
      if 135 <= angle <= 225:
          self.game_over = True
          self.player_state = GAME_OVER
      else:
          flips = math.floor(abs(self.flip_rotation) / FLIP_THRESHOLD)
          if flips > 0:
              bonus_points = flips * POINTS_PER_FLIP
              self.score += bonus_points
              self.bonus_message = arcade.Text(...)
  ```
  - Das fortschrittliche Lichtsystem im zweiten Level, das die Spielatmosphäre drastisch verändert. Es ist wichtig zu betonen, dass die Tiled-Map für Level 2 strukturell identisch mit der von Level 1 war - der Nachteffekt wurde vollständig durch die Beleuchtungsfunktionen der Arcade-Bibliothek erzeugt:
  ```python
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
  ```

## Zusammenarbeit im Entwickler:innenteam, Tools

* **Wie wurde die Arbeit unter den Entwickler:innen aufgeteilt?**
  - Als Lead-Developer war ich hauptverantwortlich für die Programmierung des Spiels
  - Enge Zusammenarbeit mit dem Level-Designer und der Grafik-Managerin für die Integration der Spielmechanik mit den erstellten Levels
  - Kontinuierliche Abstimmung mit dem Grafik-Team, um sicherzustellen, dass Sprites und visuelle Elemente korrekt im Code implementiert wurden
  - Zusammenarbeit mit dem Test- und Fehlermanager, um Bugs zu identifizieren, zu beheben und den Code lesbarer zu gestalten
  - Implementierung eines Debug-Modus, um Konstanten und Werte während der Entwicklung zu visualisieren und anzupassen, besonders für Probleme wie ungleichmäßige Spielerbewegungen oder unerwartete Zustandsänderungen
  ```python
  # Debugging-Code (nicht im finalen Build enthalten)
  if self.debug_mode:
      arcade.draw_text(
          f"State: {self.player_state}\nAngle: {self.player_visual_angle:.1f}\n"
          f"Flip: {self.flip_rotation:.1f}\nOn Ground: {is_on_ground}",
          self.player_sprite.center_x - 70,
          self.player_sprite.center_y + 100,
          arcade.color.WHITE,
          12
      )
  ```

* **Welche Werkzeuge (Editoren, IDEs) wurden genutzt?**
  - PyCharm als Hauptentwicklungsumgebung
  - GitLab für die Versionskontrolle, um simultanes Arbeiten im Team zu ermöglichen
## KI-Einsatz für Entwicklung

* **Welche KI-Tools wurden verwendet?**
  - Claude für die Code-Strukturierung und komplexere Funktionen
  - Grok für spezifische Implementierungsdetails und Debugging-Hilfe
  - Gemini für konzeptionelle Ideen und Logikansätze

* **Beispiele für Prompts und deren Ergebnisse**

  **Prompt für Camera2D-Migration:**
  ```
  I need to update my Arcade game to use the newer Camera2D system instead of the deprecated camera methods. Here's my current camera setup code:
  
  ```python
  # Current setup
  self.camera_sprites = arcade.Camera(WINDOW_WIDTH, WINDOW_HEIGHT)
  self.camera_gui = arcade.Camera(WINDOW_WIDTH, WINDOW_HEIGHT)
  
  def on_draw(self):
      self.camera_sprites.use()
      # Draw game elements
      self.camera_gui.use()
      # Draw UI elements
  ```
  
  How should I update this to use Camera2D properly? I'm using Arcade 3.2.0.
  ```

  **Ergebnis:**
  ```python
  # Updated camera setup
  self.camera = arcade.Camera2D()
  self.gui_camera = arcade.Camera2D()
  
  # In setup method
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
  
  def on_draw(self):
      self.camera.use()
      # Draw game elements
      self.gui_camera.use()
      # Draw UI elements
  ```

  **Prompt für Debug-Statements-Analyse:**
  ```
  I'm having trouble with my player physics. Here's the debug output I'm getting when the player is supposed to be sliding down a slope:
  
  ```
  State: 0 (SKIING)
  Angle: 27.3
  Terrain Angle: 25.2
  Velocity: (232.1, -87.4)
  On Ground: True
  
  State: 0 (SKIING)
  Angle: 27.3
  Terrain Angle: 32.8
  Velocity: (253.6, -92.9)
  On Ground: True
  
  State: 1 (JUMPING)
  Angle: 27.3
  Terrain Angle: 32.8
  Velocity: (267.2, -22.4)
  On Ground: False
  ```
  
  The player suddenly transitions from skiing to jumping even though I didn't press the jump key. What could be causing this and how can I fix the physics to keep the player on the ground when on slopes?
  ```

  **Ergebnis:**
  ```
  Based on your debug output, I can see the issue. The player is transitioning to JUMPING state because the physics engine is reporting that the player is no longer on the ground, even though they should be sliding down the slope.

  This often happens with physics engines when:
  1. The terrain angle changes too abruptly (from 25.2° to 32.8°)
  2. The player's velocity increases too quickly
  3. The collision detection isn't robust enough at high speeds

  Here's how to fix it:

  1. Use raycasting to more precisely detect ground contact:
  ```python
  def terrain_collision_handler(self, sprite_a, sprite_b, arbiter, space, data):
      """Handle collisions between player and terrain."""
      normal = arbiter.normal
      self.terrain_angle = math.degrees(math.atan2(-normal.x, normal.y))
      return True
  ```
  
  2. Add a small "gap" before transitioning to JUMPING state:
  ```python
  if not is_on_ground and self.player_state == SKIING:
      self.ground_contact_timer += delta_time
      if self.ground_contact_timer > 0.05:  # 50ms grace period
          self.player_state = JUMPING
          self.ground_contact_timer = 0
  else:
      self.ground_contact_timer = 0
  ```
  
  3. Adjust your physics constants, especially friction and damping for slopes
  ```

  **Prompt für Raycasting und Flip-Logik:**
  ```
  I want to implement a flip mechanic for my character when they jump. Requirements:
  
  1. When the player jumps and presses left/right keys, they should rotate in that direction
  2. If the player completes a full flip (360°), they should get bonus points
  3. If the player lands upside down (+ or - 45° from inverted), they should crash
  4. I need to track the cumulative rotation to award points for multiple flips
  ```

  **Ergebnis:**
  ```python
  # Constants for flip mechanics
  FLIP_SPEED = 360  # Degrees per second
  FLIP_THRESHOLD = 315  # Minimum rotation for a valid flip
  POINTS_PER_FLIP = 10
  
  # Player state tracking
  self.flip_rotation = 0  # Cumulative rotation during a jump
  self.player_visual_angle = 0  # Current visual angle of player sprite
  self.terrain_angle = 0  # Detected terrain angle
  
  def _update_player_state(self, delta_time):
      """Update player state and physics."""
      is_on_ground = self.physics_engine.is_on_ground(self.player_sprite)
      
      # Handle jumping and flipping
      if not is_on_ground and self.player_state == JUMPING:
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
      
      # Handle landing
      if is_on_ground and not self.was_on_ground:
          angle = self.player_visual_angle % 360
          if 135 <= angle <= 225:
              self.game_over = True
              self.player_state = GAME_OVER
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
  
  ```

* **Wie wurden die KI-Vorschläge in den Source-Code integriert?**
  - KI-generierte Code-Snippets wurden stets überprüft und angepasst
  - Viele Male habe ich den KI-Prompts die Dokumentation von Arcade und Pymunk sowie korrekte Beispielcodes beigefügt, um Fehler und Probleme zu umgehen
  - Ich habe in meinen Prompts immer gezielte Nachfragen für eine bessere Kalibrierung und Integration gestellt, was die Qualität der Vorschläge deutlich verbesserte
  - Zusätzlich bat ich um Erklärungen verschiedener Codeteile, um die Funktionsweise besser zu verstehen und Fehler selbst identifizieren zu können, was gelegentlich zu eigenen neuen Ideen und Lösungen führte
  - Herausforderung: Die meisten KI-Modelle hatten Probleme mit den neueren Versionen der Arcade-Bibliothek, da ihre Trainingsdaten hauptsächlich ältere Versionen enthielten
  - Die Kalibrierung der zahlreichen Physik-Konstanten in Pymunk musste durch praktisches Testen optimiert werden, da die KI-Vorschläge hier oft nicht direkt übernommen werden konnten
  - Bei komplexeren Mechaniken wie dem Raycasting und der Flip-Erkennung waren mehrere Iterationen mit der KI nötig, um die gewünschte Funktionalität zu erreichen
  - Die Lösung der Kamerabewegung mit `lerp_2d` war eine direkte Implementierung eines KI-Vorschlags, während die Zustandsmanagement-Logik erheblich angepasst werden musste