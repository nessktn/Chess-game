import pygame
import os
import math

def create_piece_image(piece_type, color):
    # Create a surface with alpha channel
    size = 80
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    
    # Colors
    gold = (255, 255, 0)  # Gold color for white pieces
    dark_gray = (64, 64, 64)  # Dark gray for black pieces
    piece_color = gold if color == 'white' else dark_gray
    
    # Draw different shapes based on piece type
    if piece_type == 'p':  # Pawn
        pygame.draw.circle(surface, piece_color, (size//2, size//2), size//3)
        pygame.draw.rect(surface, piece_color, (size//4, size//2, size//2, size//3))
    elif piece_type == 'n':  # Knight
        pygame.draw.circle(surface, piece_color, (size//2, size//2), size//3)
        pygame.draw.polygon(surface, piece_color, [
            (size//2, size//4),
            (size//2, size//2),
            (size//4, size//2),
            (size//2, size//4)
        ])
    elif piece_type == 'b':  # Bishop
        pygame.draw.circle(surface, piece_color, (size//2, size//2), size//3)
        pygame.draw.polygon(surface, piece_color, [
            (size//2, size//4),
            (size//2, size//2),
            (size//4, size//2),
            (size//2, size//4)
        ])
        pygame.draw.circle(surface, piece_color, (size//2, size//4), size//6)
    elif piece_type == 'r':  # Rook
        pygame.draw.rect(surface, piece_color, (size//4, size//4, size//2, size//2))
        pygame.draw.rect(surface, piece_color, (size//3, size//3, size//3, size//3))
    elif piece_type == 'q':  # Queen
        pygame.draw.circle(surface, piece_color, (size//2, size//2), size//3)
        pygame.draw.circle(surface, piece_color, (size//2, size//4), size//6)
        pygame.draw.circle(surface, piece_color, (size//4, size//2), size//6)
        pygame.draw.circle(surface, piece_color, (3*size//4, size//2), size//6)
    elif piece_type == 'k':  # King - Star shape
        # Draw a 5-pointed star
        center_x, center_y = size//2, size//2
        outer_radius = size//3
        inner_radius = outer_radius * 0.4
        points = []
        
        for i in range(10):
            # Alternate between outer and inner radius
            radius = outer_radius if i % 2 == 0 else inner_radius
            angle = math.pi * 2 * i / 10 - math.pi / 2  # Start from top
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            points.append((x, y))
        
        pygame.draw.polygon(surface, piece_color, points)
    
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