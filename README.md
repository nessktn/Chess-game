# Chess Game

A simple chess game with a graphical interface built using Python, pygame, and python-chess.

## Setup Instructions

1. Make sure you have Python installed on your system (Python 3.7 or higher recommended)

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Chess piece images are automatically generated when you run the game (no manual setup required):
   - The game will create high-quality flat 2D chess piece icons if they don't exist
   - You can also run `python generate_pieces.py` manually to regenerate them
   - Each piece has a distinctive design:
     - Pawns: Sphere on cylinder base
     - Knights: Horse head with flowing mane
     - Bishops: Mitre shape with cross
     - Rooks: Castle towers with battlements
     - Queens: Crown with decorative jewels
     - Kings: Crown with cross
   - White pieces use light gray, black pieces use dark gray with black outlines

## Running the Game

Run the following command in your terminal:
```
python chess_engine.py
```

## How to Play

1. Click on a piece to select it
2. Valid moves will be highlighted in yellow
3. Click on a highlighted square to make a move
4. The game will alternate between white and black moves
5. The game will detect checkmate, stalemate, and insufficient material conditions 
