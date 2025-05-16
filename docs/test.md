# Test Dokumentation

## Teststrategie
Es war uns sehr wichtig, das Spiel intensiv zu testen. Besonders mit der Integration von PyMunk musste sichergestellt werden, dass alle
    Physikkonstante so eingestellt sind, dass ein problemloser Durchlauf vom Spiel gewaehrleistet wird. Zu testen hat unser Testmanager
    Aanjneya das Spiel seht intensiv mit verschiedenen Spielstrategien gespielt. Alle Konstanten waren auf dem Bildschirm gezeigt, um zu verstehen, wo das Problem lag. Kleine Fehler wurden miteinander 
    per WhatsApp kommuniziert, aber grosse Probleme wie die Einstellung von der Physik-Engine waren durch GitLab in Issues dokumentiert.


## Debugging
Nach Debugging war zu sehen, dass paar Variable definiert sind und nie geruft sind, was das Spiel beeinflusst hat. Die Variable waren
    dann geruft, und die die zusaetzlich waren, waren geloescht, um das Code verstaendlicher zu machen. Das Spiel war natuerlich erneut getestet, und Verbesserung waren zu merken. 
    Ein Problem gibt es immer noch im Spiel, naemlich das ploetzliche Stoppen vom Sprite, nachdem er gesprungen hat oder von einer schiefen Ebene zu einer
    horizontalen Ebene gekommen ist.

## Bekannte Fehler
Es gibt kein echter "Fehler", sonder nur Bemerkungen und Probleme. Das Physik-Engine PyMunk ist die Grenze von Arcade-Bibliothek, und die Kalibrierung davon tut uns immer noch weh. An dem Punkt wenn diese Datei geschriebem wird, wird das Spiel immer noch getestet und es wird versucht, die Werte so einzustellen, sodass das Spiel noch besser wird.
    Es gibt schon eine bestimmte Kombination von Werten, womit das Problem vermindert werden kann. Das Spiel kann mit den in testfile.py geschriebenen Werten gespielt werden, um das Problem 99% aufzuheben.

## KI-Einsatz beim Debugging
Es wurde vergeblich vesucht, die Hilfe von KI zu nehmen. KI-Tools wie ChatGPT, Grok und Claude waren alle nicht erfolgreich, das genaue Problem zu erkennen. 
    
Beispiel fuer Grok: 
    
    When there's a slant surface, and when after that a flat surface comes, the sprite stops moving and freezes. Sometimes on all surfaces it jumps on its own, as if there was an obstacle in the map, but there isn't. Identify the issue and recommend solutions.
    
Antwort: 

        Issue: In your ski platformer game, the sprite freezes when transitioning from slanted to flat surfaces and sometimes jumps unexpectedly on all surfaces, despite no obstacles, with tile_scaling = 0.5 and player_scaling = 1.

        Root Causes:

        Freezing: Likely due to the player’s rectangular collision shape catching on tile edges, exacerbated by smaller tiles (tile_scaling = 0.5). Excessive damping or friction may also cause momentum loss.
        Unexpected Jumping: Pymunk’s collision resolution may apply unintended upward impulses, or the is_on_ground check may be unreliable, causing erratic state changes.
        Solutions:

        Use Circle Shape: Change the player’s collision shape to a circle (radius = 32 pixels) to slide smoothly over tile edges.
        Adjust Physics Constants:
        DEFAULT_DAMPING = 0.01: Reduce speed loss.
        PLAYER_MASS = 2.0: Increase to resist collision impacts.
        PLAYER_MOVE_FORCE_ON_GROUND = 2000, PLAYER_MOVE_FORCE_IN_AIR = 1400: Stronger forces for consistent movement.
        GRAVITY = 1500: Lower to soften collisions.
        WALL_FRICTION = 0.0: Ensure no terrain friction.
        Verify Tilemap: Check LevelX.tmj for misaligned or overlapping tiles, ensuring smooth slant-to-flat transitions.
        Improve Ground Detection: Add a custom check using velocity and terrain proximity to stabilize is_on_ground.
        Apply Continuous Force: Ensure a minimum forward velocity to prevent freezing during collisions.
        Implementation: Update the GameConstants class with the new values and modify _setup_physics_engine to use a circle shape. Add debug logging and visualize collision shapes if needed.

        Testing: Test transitions and monitor for jumping. Adjust radius (e.g., 24 or 40) or inspect tilemap if issues persist.

Finden Sie einen Fehler, dann [schreiben Sie uns eine E-Mail](mailto:moudgil@campus.tu-berlin.de)