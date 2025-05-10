# Tetris Game Collection

This repository contains two implementations of the classic Tetris game:

1. **Classic Tetris (2D)**: A traditional Tetris game built with Pygame.
2. **3D Tetris**: An advanced 3D version of Tetris using PyOpenGL and Pygame.

## Requirements

- Python 3.x
- Pygame
- PyOpenGL (for 3D version)
- NumPy (for 3D version)

You can install the required packages using:

```bash
pip install -r requirements.txt
```

## How to Play

### Classic Tetris (2D)
Run the game with:
```bash
python tetris.py
```

Controls:
- Left/Right Arrow: Move piece horizontally
- Down Arrow: Soft drop
- Up Arrow: Rotate piece
- Space: Hard drop

### 3D Tetris
Run the game with:
```bash
python tetris3d.py
```

Controls:
- Left/Right Arrow: Move piece left/right
- Up/Down Arrow: Move piece forward/backward
- W: Rotate piece around X-axis
- A: Rotate piece around Y-axis
- S: Rotate piece around Z-axis
- Space: Hard drop

## Features

- Score tracking
- Level progression
- Next piece preview (2D version)
- Game over detection
- 3D rotation and perspective (3D version)

## License

This project is open source and available under the MIT License. 