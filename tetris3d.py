import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random
import numpy as np

# Initialize Pygame and OpenGL
pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
pygame.display.set_caption("3D Tetris")

# Set up the perspective
gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, -30)

# Colors
COLORS = {
    'I': (0, 1, 1),    # Cyan
    'O': (1, 1, 0),    # Yellow
    'T': (1, 0, 1),    # Magenta
    'L': (1, 0.5, 0),  # Orange
    'J': (0, 0, 1),    # Blue
    'S': (0, 1, 0),    # Green
    'Z': (1, 0, 0)     # Red
}

# 3D Tetromino shapes (4x4x4 matrices)
SHAPES = {
    'I': np.array([
        [[0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]],
        [[1, 1, 1, 1],
         [0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]],
        [[0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]],
        [[0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]]
    ]),
    'O': np.array([
        [[0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]],
        [[0, 1, 1, 0],
         [0, 1, 1, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]],
        [[0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]],
        [[0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]]
    ]),
    'T': np.array([
        [[0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]],
        [[0, 1, 0, 0],
         [1, 1, 1, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]],
        [[0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]],
        [[0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]]
    ]),
    'L': np.array([
        [[0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]],
        [[1, 0, 0, 0],
         [1, 1, 1, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]],
        [[0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]],
        [[0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]]
    ]),
    'J': np.array([
        [[0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]],
        [[0, 0, 1, 0],
         [1, 1, 1, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]],
        [[0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]],
        [[0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]]
    ]),
    'S': np.array([
        [[0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]],
        [[0, 1, 1, 0],
         [1, 1, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]],
        [[0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]],
        [[0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]]
    ]),
    'Z': np.array([
        [[0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]],
        [[1, 1, 0, 0],
         [0, 1, 1, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]],
        [[0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]],
        [[0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]]
    ])
}

class Tetris3D:
    def __init__(self):
        self.grid_size = (10, 20, 10)  # width, height, depth
        self.grid = np.zeros(self.grid_size)
        self.current_piece = self.new_piece()
        self.rotation = [0, 0, 0]  # x, y, z rotation
        self.position = [0, 0, 0]  # x, y, z position
        self.score = 0
        self.game_over = False

    def new_piece(self):
        shape_name = random.choice(list(SHAPES.keys()))
        return {
            'shape': SHAPES[shape_name],
            'color': COLORS[shape_name],
            'position': [self.grid_size[0]//2, 0, self.grid_size[2]//2]
        }

    def draw_cube(self, position, color):
        vertices = [
            [1, -1, -1], [1, 1, -1], [-1, 1, -1], [-1, -1, -1],
            [1, -1, 1], [1, 1, 1], [-1, -1, 1], [-1, 1, 1]
        ]
        edges = [
            (0,1), (1,2), (2,3), (3,0),
            (4,5), (5,7), (7,6), (6,4),
            (0,4), (1,5), (2,7), (3,6)
        ]
        surfaces = [
            (0,1,2,3), (3,2,7,6), (6,7,5,4),
            (4,5,1,0), (1,5,7,2), (4,0,3,6)
        ]

        glPushMatrix()
        glTranslatef(position[0], position[1], position[2])
        
        glBegin(GL_QUADS)
        for surface in surfaces:
            glColor3fv(color)
            for vertex in surface:
                glVertex3fv(vertices[vertex])
        glEnd()

        glBegin(GL_LINES)
        glColor3f(0.5, 0.5, 0.5)
        for edge in edges:
            for vertex in edge:
                glVertex3fv(vertices[vertex])
        glEnd()
        
        glPopMatrix()

    def draw_grid(self):
        for x in range(self.grid_size[0]):
            for y in range(self.grid_size[1]):
                for z in range(self.grid_size[2]):
                    if self.grid[x,y,z] != 0:
                        self.draw_cube([x-self.grid_size[0]//2, 
                                      y-self.grid_size[1]//2, 
                                      z-self.grid_size[2]//2], 
                                     self.grid[x,y,z])

    def draw_current_piece(self):
        shape = self.current_piece['shape']
        color = self.current_piece['color']
        pos = self.current_piece['position']
        
        for x in range(4):
            for y in range(4):
                for z in range(4):
                    if shape[x,y,z] == 1:
                        self.draw_cube([pos[0]+x-self.grid_size[0]//2,
                                      pos[1]+y-self.grid_size[1]//2,
                                      pos[2]+z-self.grid_size[2]//2],
                                     color)

    def rotate_piece(self, axis):
        if axis == 'x':
            self.current_piece['shape'] = np.rot90(self.current_piece['shape'], 1, (1,2))
        elif axis == 'y':
            self.current_piece['shape'] = np.rot90(self.current_piece['shape'], 1, (0,2))
        elif axis == 'z':
            self.current_piece['shape'] = np.rot90(self.current_piece['shape'], 1, (0,1))

    def move_piece(self, dx, dy, dz):
        new_pos = [self.current_piece['position'][0] + dx,
                  self.current_piece['position'][1] + dy,
                  self.current_piece['position'][2] + dz]
        
        if self.is_valid_move(new_pos):
            self.current_piece['position'] = new_pos
            return True
        return False

    def is_valid_move(self, new_pos):
        shape = self.current_piece['shape']
        for x in range(4):
            for y in range(4):
                for z in range(4):
                    if shape[x,y,z] == 1:
                        grid_x = new_pos[0] + x
                        grid_y = new_pos[1] + y
                        grid_z = new_pos[2] + z
                        
                        if (grid_x < 0 or grid_x >= self.grid_size[0] or
                            grid_y < 0 or grid_y >= self.grid_size[1] or
                            grid_z < 0 or grid_z >= self.grid_size[2] or
                            self.grid[grid_x,grid_y,grid_z] != 0):
                            return False
        return True

    def merge_piece(self):
        shape = self.current_piece['shape']
        pos = self.current_piece['position']
        color = self.current_piece['color']
        
        for x in range(4):
            for y in range(4):
                for z in range(4):
                    if shape[x,y,z] == 1:
                        self.grid[pos[0]+x, pos[1]+y, pos[2]+z] = color

    def clear_layers(self):
        layers_cleared = 0
        for y in range(self.grid_size[1]):
            if np.all(self.grid[:,y,:] != 0):
                self.grid = np.delete(self.grid, y, axis=1)
                self.grid = np.insert(self.grid, 0, np.zeros((self.grid_size[0], 1, self.grid_size[2])), axis=1)
                layers_cleared += 1
        return layers_cleared

    def run(self):
        clock = pygame.time.Clock()
        fall_time = 0
        fall_speed = 0.5  # seconds between automatic falls

        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.move_piece(-1, 0, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.move_piece(1, 0, 0)
                    elif event.key == pygame.K_UP:
                        self.move_piece(0, 0, -1)
                    elif event.key == pygame.K_DOWN:
                        self.move_piece(0, 0, 1)
                    elif event.key == pygame.K_w:
                        self.rotate_piece('x')
                    elif event.key == pygame.K_a:
                        self.rotate_piece('y')
                    elif event.key == pygame.K_s:
                        self.rotate_piece('z')
                    elif event.key == pygame.K_SPACE:
                        while self.move_piece(0, 1, 0):
                            pass
                        self.merge_piece()
                        layers = self.clear_layers()
                        self.score += layers * 100
                        self.current_piece = self.new_piece()
                        if not self.is_valid_move(self.current_piece['position']):
                            self.game_over = True

            # Handle automatic falling
            fall_time += clock.get_rawtime()
            if fall_time >= fall_speed * 1000:
                fall_time = 0
                if not self.move_piece(0, 1, 0):
                    self.merge_piece()
                    layers = self.clear_layers()
                    self.score += layers * 100
                    self.current_piece = self.new_piece()
                    if not self.is_valid_move(self.current_piece['position']):
                        self.game_over = True

            # Clear the screen and set up the view
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glEnable(GL_DEPTH_TEST)
            
            # Rotate the view
            glRotatef(1, 3, 1, 1)

            # Draw the game elements
            self.draw_grid()
            self.draw_current_piece()

            # Draw score
            font = pygame.font.Font(None, 36)
            text = font.render(f'Score: {self.score}', True, (255, 255, 255))
            text_surface = pygame.Surface((text.get_width(), text.get_height()))
            text_surface.blit(text, (0, 0))
            text_data = pygame.image.tostring(text_surface, "RGBA", True)
            
            glRasterPos2f(-0.9, 0.9)
            glDrawPixels(text.get_width(), text.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, text_data)

            pygame.display.flip()
            clock.tick(60)

        # Game over screen
        font = pygame.font.Font(None, 48)
        text = font.render('GAME OVER', True, (255, 0, 0))
        text_surface = pygame.Surface((text.get_width(), text.get_height()))
        text_surface.blit(text, (0, 0))
        text_data = pygame.image.tostring(text_surface, "RGBA", True)
        
        glRasterPos2f(-0.2, 0)
        glDrawPixels(text.get_width(), text.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, text_data)
        pygame.display.flip()
        pygame.time.wait(2000)

if __name__ == "__main__":
    game = Tetris3D()
    game.run() 