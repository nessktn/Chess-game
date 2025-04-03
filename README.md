# Chess Engine

A simple chess game with a graphical interface built using Python, pygame, and python-chess.

## Setup Instructions

1. Make sure you have Python installed on your system (Python 3.7 or higher recommended)

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Create an `assets` folder in the project directory and add chess piece images:
   - You'll need images for both white and black pieces
   - Required images: p_white.png, p_black.png (pawns), n_white.png, n_black.png (knights),
     b_white.png, b_black.png (bishops), r_white.png, r_black.png (rooks),
     q_white.png, q_black.png (queens), k_white.png, k_black.png (kings)
   - The images should be square and will be automatically scaled to fit the board

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