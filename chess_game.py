import chess
import chess.engine
import pygame
import sys
from typing import Tuple, Optional, List
import time
import os
import generate_pieces

class ChessEngine:
    def __init__(self):
        # Initialize the chess board
        self.board = chess.Board()
        
        # Initialize Pygame
        pygame.init()
        pygame.mixer.init()  # Initialize mixer for sound effects
        
        # Constants
        self.SQUARE_SIZE = 80
        self.BOARD_SIZE = self.SQUARE_SIZE * 8
        self.SIDEBAR_WIDTH = 200
        self.WINDOW_SIZE = (self.BOARD_SIZE + self.SIDEBAR_WIDTH, self.BOARD_SIZE)
        
        # Colors
        self.WHITE = (255, 255, 255)  # Pure white
        self.BLACK = (0, 0, 0)  # Pure black
        self.HIGHLIGHT = (255, 255, 0, 50)
        self.SIDEBAR_COLOR = (240, 240, 240)
        self.TEXT_COLOR = (0, 0, 0)
        
        # Setup display
        self.screen = pygame.display.set_mode(self.WINDOW_SIZE)
        pygame.display.set_caption("Chess Engine")
        
        # Initialize font
        self.font = pygame.font.SysFont('Arial', 16)
        
        # Load pieces
        self.pieces = {}
        self.load_pieces()
        
        # Load sound effects
        self.sounds = {}
        self.load_sounds()
        
        # Game state
        self.selected_square = None
        self.valid_moves = []
        self.player_just_moved = False
        self.move_time = 0
        self.move_history = []
        self.current_move_number = 1
        
        # Initialize AI engine
        try:
            # Try to find Stockfish in common locations
            stockfish_paths = [
                "stockfish.exe",  # Current directory
                os.path.join(os.path.dirname(__file__), "stockfish.exe"),  # Same directory as script
                r"C:\Program Files\Stockfish\stockfish.exe",  # Common installation path
                r"C:\Program Files (x86)\Stockfish\stockfish.exe",  # Alternative installation path
            ]
            
            stockfish_found = False
            for path in stockfish_paths:
                if os.path.exists(path):
                    self.engine = chess.engine.SimpleEngine.popen_uci(path)
                    stockfish_found = True
                    print(f"Found Stockfish at: {path}")
                    break
            
            if not stockfish_found:
                print("Stockfish not found. Please download it from https://stockfishchess.org/download/windows/")
                print("Then place stockfish.exe in the same directory as this script.")
                sys.exit(1)
                
            self.ai_thinking = False
        except Exception as e:
            print(f"Error initializing AI engine: {e}")
            print("Please make sure Stockfish is installed correctly.")
            sys.exit(1)
        
    def load_pieces(self):
        # Ensure assets directory exists
        if not os.path.exists('assets'):
            os.makedirs('assets')
        
        pieces = ['p', 'n', 'b', 'r', 'q', 'k']
        for piece in pieces:
            white_path = f'assets/{piece}_white.png'
            black_path = f'assets/{piece}_black.png'
            
            # Generate pieces if they don't exist
            if not os.path.exists(white_path) or not os.path.exists(black_path):
                print(f"Generating missing piece images for {piece}...")
                generate_pieces.main()  # This will generate all pieces
                break  # Only need to generate once
            
            self.pieces[f'w{piece}'] = pygame.image.load(white_path)
            self.pieces[f'b{piece}'] = pygame.image.load(black_path)
            # Scale images to fit squares
            self.pieces[f'w{piece}'] = pygame.transform.scale(
                self.pieces[f'w{piece}'], 
                (self.SQUARE_SIZE, self.SQUARE_SIZE)
            )
            self.pieces[f'b{piece}'] = pygame.transform.scale(
                self.pieces[f'b{piece}'], 
                (self.SQUARE_SIZE, self.SQUARE_SIZE)
            )

    def load_sounds(self):
        try:
            self.sounds['move'] = pygame.mixer.Sound('assets/move.wav')
            self.sounds['check'] = pygame.mixer.Sound('assets/check.wav')
        except FileNotFoundError:
            print("Sound files not found. Please add 'move.wav' and 'check.wav' to the assets folder.")
            self.sounds = {}  # Empty dict if sounds not found

    def play_sound(self, sound_name: str):
        if sound_name in self.sounds:
            self.sounds[sound_name].play()

    def get_square_from_coords(self, pos: Tuple[int, int]) -> Optional[chess.Square]:
        x, y = pos
        # Only process clicks on the board, not the sidebar
        if x >= self.BOARD_SIZE:
            return None
            
        file = x // self.SQUARE_SIZE
        rank = 7 - (y // self.SQUARE_SIZE)
        if 0 <= file <= 7 and 0 <= rank <= 7:
            return chess.square(file, rank)
        return None

    def get_coords_from_square(self, square: chess.Square) -> Tuple[int, int]:
        file = chess.square_file(square)
        rank = chess.square_rank(square)
        x = file * self.SQUARE_SIZE
        y = (7 - rank) * self.SQUARE_SIZE
        return (x, y)

    def draw_board(self):
        # Draw the chess board
        for rank in range(8):
            for file in range(8):
                color = self.WHITE if (rank + file) % 2 == 0 else self.BLACK
                pygame.draw.rect(
                    self.screen,
                    color,
                    (file * self.SQUARE_SIZE, rank * self.SQUARE_SIZE, 
                    self.SQUARE_SIZE, self.SQUARE_SIZE)
                )
        
        # Draw the sidebar
        pygame.draw.rect(
            self.screen,
            self.SIDEBAR_COLOR,
            (self.BOARD_SIZE, 0, self.SIDEBAR_WIDTH, self.BOARD_SIZE)
        )
        
        # Draw sidebar title
        title_text = self.font.render("Move History", True, self.TEXT_COLOR)
        self.screen.blit(title_text, (self.BOARD_SIZE + 10, 10))
        
        # Draw a line under the title
        pygame.draw.line(
            self.screen,
            self.TEXT_COLOR,
            (self.BOARD_SIZE, 40),
            (self.BOARD_SIZE + self.SIDEBAR_WIDTH, 40)
        )

    def draw_move_history(self):
        # Display move history
        y_offset = 60
        line_height = 25
        
        for i, move in enumerate(self.move_history):
            # Calculate position for this move
            row = i // 2
            col = i % 2
            
            # Move number
            if col == 0:
                move_num_text = self.font.render(f"{row + 1}.", True, self.TEXT_COLOR)
                self.screen.blit(move_num_text, (self.BOARD_SIZE + 10, y_offset + row * line_height))
            
            # Move text
            move_text = self.font.render(move, True, self.TEXT_COLOR)
            self.screen.blit(move_text, (self.BOARD_SIZE + 40 + col * 80, y_offset + row * line_height))

    def draw_pieces(self):
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                color = 'w' if piece.color else 'b'
                piece_key = f'{color}{piece.symbol().lower()}'
                x, y = self.get_coords_from_square(square)
                self.screen.blit(self.pieces[piece_key], (x, y))

    def highlight_square(self, square: chess.Square):
        x, y = self.get_coords_from_square(square)
        highlight_surface = pygame.Surface((self.SQUARE_SIZE, self.SQUARE_SIZE), pygame.SRCALPHA)
        highlight_surface.fill(self.HIGHLIGHT)
        self.screen.blit(highlight_surface, (x, y))

    def highlight_moves(self):
        for move in self.valid_moves:
            self.highlight_square(move.to_square)

    def add_move_to_history(self, move: chess.Move):
        # Convert the move to standard chess notation
        move_san = self.board.san(move)
        
        # Add to move history
        self.move_history.append(move_san)
        
        # Update move number
        if len(self.move_history) % 2 == 0:
            self.current_move_number += 1

    def make_ai_move(self):
        if not self.ai_thinking and not self.board.is_game_over():
            self.ai_thinking = True
            # Get AI move with a time limit of 1 second
            result = self.engine.play(self.board, chess.engine.Limit(time=1.0))
            
            # Get the move in SAN notation before applying it
            move_san = self.board.san(result.move)
            
            # Apply the move
            self.board.push(result.move)
            
            # Play move sound
            self.play_sound('move')
            
            # Check if king is in check and play sound
            if self.board.is_check():
                self.play_sound('check')
            
            # Add move to history
            self.move_history.append(move_san)
            
            # Update move number
            if len(self.move_history) % 2 == 0:
                self.current_move_number += 1
            
            self.ai_thinking = False
            
            # Check for game end conditions
            if self.board.is_checkmate():
                print("Checkmate! AI wins!")
            elif self.board.is_stalemate():
                print("Stalemate!")
            elif self.board.is_insufficient_material():
                print("Draw due to insufficient material!")

    def run(self):
        clock = pygame.time.Clock()
        while True:
            current_time = time.time()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.engine.quit()
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN and not self.ai_thinking:
                    pos = pygame.mouse.get_pos()
                    square = self.get_square_from_coords(pos)
                    
                    if square is not None:
                        if self.selected_square is None:
                            # First click - select piece
                            piece = self.board.piece_at(square)
                            if piece and piece.color == self.board.turn:
                                self.selected_square = square
                                self.valid_moves = [
                                    move for move in self.board.legal_moves
                                    if move.from_square == square
                                ]
                        else:
                            # Second click - make move
                            move = chess.Move(self.selected_square, square)
                            if move in self.valid_moves:
                                # Get the move in SAN notation before applying it
                                move_san = self.board.san(move)
                                
                                # Apply the move
                                self.board.push(move)
                                
                                # Play move sound
                                self.play_sound('move')
                                
                                # Check if king is in check and play sound
                                if self.board.is_check():
                                    self.play_sound('check')
                                
                                # Add move to history
                                self.move_history.append(move_san)
                                
                                # Update move number
                                if len(self.move_history) % 2 == 0:
                                    self.current_move_number += 1
                                
                                self.player_just_moved = True
                                self.move_time = current_time
                                
                                # Check for game end conditions
                                if self.board.is_checkmate():
                                    print("Checkmate! You win!")
                                elif self.board.is_stalemate():
                                    print("Stalemate!")
                                elif self.board.is_insufficient_material():
                                    print("Draw due to insufficient material!")
                            
                            self.selected_square = None
                            self.valid_moves = []

            # Make AI move if it's black's turn and enough time has passed
            if (self.board.turn == chess.BLACK and not self.ai_thinking and 
                (not self.player_just_moved or current_time - self.move_time >= 3.0)):
                self.make_ai_move()
                self.player_just_moved = False

            # Draw the current state
            self.draw_board()
            if self.selected_square is not None:
                self.highlight_square(self.selected_square)
                self.highlight_moves()
            self.draw_pieces()
            self.draw_move_history()
            
            pygame.display.flip()
            clock.tick(60)  # Limit to 60 FPS

if __name__ == "__main__":
    engine = ChessEngine()
    engine.run() 