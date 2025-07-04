# Level Design Documentation

Level Design by: Abdulloh Khakimov

---

## Level Concept

Our game consists of **two levels**:

- **Level 1** is an introductory level where the player learns the controls and game mechanics. The map is relatively simple, with a few obstacles and clearly visible elements.
- **Level 2** is significantly more difficult: The map is larger, contains more obstacles, and is visually limited by darkness – visibility is only possible through a cone of light.

The transition is achieved by pressing a key:
- After completing Level 1: Press **N** → Start Level 2.
- After completing Level 2, the game ends with a victory animation and a score display.

The two levels differ not only in their **names**, but also in their **map structure** and the **tilesets** used.

---

## Game Mechanics in Level Design

Our level mechanics are based on realistic physics principles:

- The player clearly recognizes the difference between snow, coins, stones, and water.
- The character moves on **undulating ground**, adapting to the **angle of inclination** and rotating accordingly.
- The jumping mechanics ensure **smooth jumping and realistic landings**.
- Collisions with obstacles (e.g., stones or water) result in the game ending.
- Coins can be collected by touching them.
- The player can perform **tricks (somersaults)** using the arrow keys – a risky landing (headfirst) also ends the game.

The physics mechanics were implemented using the **Pymunk library** and are active in both levels.

---

## Maps and Tilesets

To create the maps and tilesets, we used:

- **Piskel** for custom tilesets (e.g., snow and rock)
- **Tiled Map Editor** for visual map creation
- Export formats: `.tmj` (Tiled JSON) and `.tmx` (Tilemap XML for tileset collections)

We used different resources for the two levels:

- **Level 1:** Default tilesets from the Arcade library
- **Level 2:** Custom tilesets created with Piskel

Tileset examples:

**Snow:**
<img src="../assets/Tiles/snow.png" width="64">

**Rock:**
<img src="../assets/Tiles/rock.png" width="64">

The size of each tile is **128x128 pixels**.

---

## Technical Implementation

The maps were integrated into Arcade as follows:

```python
map_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"map/Level{level_number}.tmj")
self.tile_map = arcade.load_tilemap(
map_path, layer_options=layer_options, scaling=TILE_SCALING
)
```

### Layer structure:

- **Terrain**: Ground (e.g., snow)
- **Obstacles**: Obstacles (e.g., rock, water)
- **Collectibles**: Coins

### Challenge:

The only problem was the **path specification**, as team members were working with different operating systems. This was solved by using the **`os` library**.

---

## Balancing

### Difficulty Level

The difficulty level depends on:

- Map size
- Number and placement of obstacles
- Visibility (Level 2 is dark)

### Testing Methods

After each level design, the map was uploaded to the repository and tested by each team member. Based on feedback, maps were improved and optimized.

### Adjustments

Each test run resulted in meaningful improvements in layout, obstacle placement, and playability.

### Rating

- **Level 1** is the best balanced – with flat terrain and a clear structure.
- **Level 2** contains uneven terrain that was originally intended to be more complex but was limited by the arcade library's limitations.
