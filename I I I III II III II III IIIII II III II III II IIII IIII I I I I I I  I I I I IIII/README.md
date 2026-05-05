# Super Advanced Snake Game

A highly advanced version of the classic Snake game built with Python and Pygame, featuring levels, power-ups, obstacles, particles, BOSS BATTLES, and more!

## Features

- **Levels**: Increase every 50 points, boosting speed and adding more obstacles for higher challenge
- **Power-ups**: Collect special items for bonuses (appear randomly, 50% spawn chance)
  - **Speed Boost (Blue)**: Temporarily increases snake speed for 10 seconds
  - **Shrink (Yellow)**: Removes one segment from the snake's tail
  - **Extra Points (Purple)**: Grants 20 bonus points instantly
  - **Teleport (Orange)**: Instantly moves the snake to a safe random position on the board
  - **Slow (Pink)**: Temporarily decreases snake speed for 10 seconds
  - **Multi-Food (Red)**: Spawns 3 extra food items on the board
  - **Invisible (Gray)**: Makes the snake semi-transparent and allows passing through obstacles for 15 seconds
  - **Shield (Gold)**: Blocks one obstacle collision or projectile hit for 20 seconds
  - **Obstacle Clear (Light Blue)**: Removes ALL obstacles from the board instantly
- **🔥 BOSS BATTLES**: Every 150 points, a boss spawns with:
  - Health that scales with progression (gets harder each boss)
  - Cannot attack for 1 second after spawning
  - Shoots projectiles in 4 directions every 6-12 seconds
  - Moves randomly around the board, bouncing off walls
  - Spawns a special power-up when defeated (+100 bonus points)
  - You must crash into the boss to deal damage!
- **Projectile Defense**: Dodge boss projectiles or block them with shield power-up
- **Obstacles**: White blocks that increase with levels; hitting them ends the game unless protected by shield
- **Particles**: Green particle effects when eating food and defeating boss
- **Sounds**: Audio feedback for eating food, collecting power-ups, and game over
- **High Score List**: Top 5 scores saved and displayed
- **Pause Functionality**: Press P to pause/unpause during gameplay
- **Menu and Game Over Screens**: Start screen with options, end screen showing scores and restart

## Game Elements

- **Snake**: Green segments that grow when eating food. Becomes semi-transparent when invisible. Dies hitting walls, itself, or obstacles (unless shielded/invisible).
- **Food**: Red square that appears randomly. Eating it grows the snake (+10 points).
- **Extra Food**: Red squares from Multi-Food power-up, same as regular food.
- **Boss**: Large red circle spawning every 150 points. Defeat by crashing into it multiple times. Dodge its projectiles!
- **Projectiles**: Red circles fired by boss in cross pattern. Game over if hit (unless shielded/invisible).
- **Obstacles**: White blocks. More appear per level. Can be cleared with Obstacle Clear power-up.
- **Score**: Displays top-left. Increases from food (+10), power-ups (+20), and boss defeats (+100).
- **Level**: Shows top-left. Affects speed and obstacle spawning.
- **Shield**: Displayed top-right when active. Blocks one collision.
- **High Scores**: Top 5 displayed on game over screen.

## How to Run

1. Ensure Python 3.x is installed.
2. Install dependencies: `pip install -r requirements.txt`
3. Run the game: `python main.py` or double-click `run_game.bat`

## Controls

- **Arrow Keys**: Move the snake (up, down, left, right)
- **P**: Pause/Unpause the game
- **SPACE**: Start the game from the menu
- **R**: Restart after game over
- **Q**: Quit the game (from menu or game over)

## Game Mechanics

- The snake moves continuously in the chosen direction.
- Eat red food to grow, score points, and potentially spawn power-ups.
- Collect power-ups for various effects (see Features).
- Avoid white obstacles that increase with levels.
- Levels advance every 50 points, increasing speed and adding more obstacles.
- Game ends if the snake hits the edge, itself, or an obstacle.
- Particles appear as visual effects when eating food.
- Sounds play for key events.
- High scores are saved and displayed.