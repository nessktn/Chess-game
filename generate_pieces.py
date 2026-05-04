import pygame
import os
import math

def create_piece_image(piece_type, color):
    # Create a surface with alpha channel
    size = 80
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    
    # Colors
    white_piece = (240, 240, 240)  # Light gray for white pieces
    black_piece = (40, 40, 40)     # Dark gray for black pieces
    outline_color = (20, 20, 20)    # Dark outline
    piece_color = white_piece if color == 'white' else black_piece
    
    # Draw different shapes based on piece type with better designs
    if piece_type == 'p':  # Pawn - Simple sphere on cylinder
        # Base cylinder
        pygame.draw.rect(surface, piece_color, (size//3, size//2, size//3, size//3))
        pygame.draw.rect(surface, outline_color, (size//3, size//2, size//3, size//3), 2)
        # Sphere on top
        pygame.draw.circle(surface, piece_color, (size//2, size//3), size//6)
        pygame.draw.circle(surface, outline_color, (size//2, size//3), size//6, 2)
        
    elif piece_type == 'n':  # Knight - Horse head shape
        # Body
        pygame.draw.rect(surface, piece_color, (size//4, size//2, size//2, size//3))
        pygame.draw.rect(surface, outline_color, (size//4, size//2, size//2, size//3), 2)
        # Head
        pygame.draw.circle(surface, piece_color, (size//2, size//3), size//5)
        pygame.draw.circle(surface, outline_color, (size//2, size//3), size//5, 2)
        # Mane
        pygame.draw.polygon(surface, piece_color, [
            (size//2 - size//8, size//4),
            (size//2 + size//8, size//4),
            (size//2 + size//6, size//3),
            (size//2 - size//6, size//3)
        ])
        pygame.draw.polygon(surface, outline_color, [
            (size//2 - size//8, size//4),
            (size//2 + size//8, size//4),
            (size//2 + size//6, size//3),
            (size//2 - size//6, size//3)
        ], 2)
        
    elif piece_type == 'b':  # Bishop - Mitre shape
        # Base
        pygame.draw.rect(surface, piece_color, (size//3, size//2, size//3, size//3))
        pygame.draw.rect(surface, outline_color, (size//3, size//2, size//3, size//3), 2)
        # Mitre
        pygame.draw.polygon(surface, piece_color, [
            (size//2, size//6),
            (size//3, size//3),
            (2*size//3, size//3)
        ])
        pygame.draw.polygon(surface, outline_color, [
            (size//2, size//6),
            (size//3, size//3),
            (2*size//3, size//3)
        ], 2)
        # Cross on top
        pygame.draw.line(surface, outline_color, (size//2 - size//12, size//8), (size//2 + size//12, size//8), 3)
        pygame.draw.line(surface, outline_color, (size//2, size//8 - size//12), (size//2, size//8 + size//12), 3)
        
    elif piece_type == 'r':  # Rook - Castle shape
        # Base
        pygame.draw.rect(surface, piece_color, (size//4, size//2, size//2, size//3))
        pygame.draw.rect(surface, outline_color, (size//4, size//2, size//2, size//3), 2)
        # Towers
        pygame.draw.rect(surface, piece_color, (size//5, size//4, size//6, size//3))
        pygame.draw.rect(surface, outline_color, (size//5, size//4, size//6, size//3), 2)
        pygame.draw.rect(surface, piece_color, (4*size//5 - size//6, size//4, size//6, size//3))
        pygame.draw.rect(surface, outline_color, (4*size//5 - size//6, size//4, size//6, size//3), 2)
        # Battlements
        for i in range(3):
            pygame.draw.rect(surface, piece_color, (size//5 + i*size//15, size//6, size//20, size//12))
            pygame.draw.rect(surface, outline_color, (size//5 + i*size//15, size//6, size//20, size//12), 1)
            pygame.draw.rect(surface, piece_color, (4*size//5 - size//6 + i*size//15, size//6, size//20, size//12))
            pygame.draw.rect(surface, outline_color, (4*size//5 - size//6 + i*size//15, size//6, size//20, size//12), 1)
        
    elif piece_type == 'q':  # Queen - Crown shape
        # Base
        pygame.draw.rect(surface, piece_color, (size//4, size//2, size//2, size//3))
        pygame.draw.rect(surface, outline_color, (size//4, size//2, size//2, size//3), 2)
        # Crown points
        crown_points = [
            (size//2, size//6),
            (size//3, size//4),
            (size//2 - size//12, size//3),
            (size//2, size//5),
            (size//2 + size//12, size//3),
            (2*size//3, size//4)
        ]
        pygame.draw.polygon(surface, piece_color, crown_points)
        pygame.draw.polygon(surface, outline_color, crown_points, 2)
        # Jewels
        pygame.draw.circle(surface, (255, 0, 0), (size//2 - size//12, size//3), 3)
        pygame.draw.circle(surface, (255, 0, 0), (size//2 + size//12, size//3), 3)
        
    elif piece_type == 'k':  # King - Crown with cross
        # Base
        pygame.draw.rect(surface, piece_color, (size//4, size//2, size//2, size//3))
        pygame.draw.rect(surface, outline_color, (size//4, size//2, size//2, size//3), 2)
        # Crown
        pygame.draw.polygon(surface, piece_color, [
            (size//2, size//6),
            (size//3, size//4),
            (size//2 - size//8, size//3),
            (size//2, size//5),
            (size//2 + size//8, size//3),
            (2*size//3, size//4)
        ])
        pygame.draw.polygon(surface, outline_color, [
            (size//2, size//6),
            (size//3, size//4),
            (size//2 - size//8, size//3),
            (size//2, size//5),
            (size//2 + size//8, size//3),
            (2*size//3, size//4)
        ], 2)
        # Cross on top
        pygame.draw.line(surface, outline_color, (size//2 - size//12, size//8), (size//2 + size//12, size//8), 3)
        pygame.draw.line(surface, outline_color, (size//2, size//8 - size//12), (size//2, size//8 + size//12), 3)
    
    return surface
    
    return surface

def main():
    # Initialize Pygame
    pygame.init()
    
    # Create assets directory if it doesn't exist
    if not os.path.exists('assets'):
        os.makedirs('assets')
    
    # Generate all pieces
    pieces = ['p', 'n', 'b', 'r', 'q', 'k']
    colors = ['white', 'black']
    
    for piece in pieces:
        for color in colors:
            surface = create_piece_image(piece, color)
            filename = f'assets/{piece}_{color}.png'
            pygame.image.save(surface, filename)
            print(f'Generated {filename}')
    
    pygame.quit()

if __name__ == '__main__':
    main() 