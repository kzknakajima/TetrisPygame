# -*- coding: utf-8 -*-
"""
Tetris game constants
Display sizes, play area dimensions, and other game constants
"""

# Display size
S_WIDTH = 800
S_HEIGHT = 700

# Play area size
PLAY_WIDTH = 300  # 300/30 = 10 blocks
PLAY_HEIGHT = 600  # 600/30 = 20 blocks

# Block size
BLOCK_SIZE = 30

# Play area top-left coordinates
TOP_LEFT_X = (S_WIDTH - PLAY_WIDTH) / 2
TOP_LEFT_Y = (S_HEIGHT - PLAY_HEIGHT) / 2

# Grid dimensions
GRID_WIDTH = int(PLAY_WIDTH / BLOCK_SIZE)  # 10
GRID_HEIGHT = int(PLAY_HEIGHT / BLOCK_SIZE)  # 20

# Game constants
MINO_ROTATION_STATES = 4
MINO_GRID_SIZE = 5
MINO_INNER_GRID = 4  # ミノの実際の描画サイズ（5x5グリッドの中の4x4）
SCORE_PER_LINE = 100

# Time control
FALL_INTERVAL = 1000  # ミノの自動落下間隔（ミリ秒）
FPS = 60  # フレームレート

# Mino starting position
MINO_START_X = 3
MINO_START_Y = 0

# UI constants
FONT_NAME = 'comicsans'
FONT_SIZE = 30
BORDER_WIDTH = 3

# Score display position
SCORE_LABEL_X = 110
SCORE_LABEL_Y = 30

# End message position
END_MSG_X = 110
END_MSG_Y = 650

# Next mino display constants
NEXT_LABEL_OFFSET_X = -10
NEXT_LABEL_OFFSET_Y = -200
NEXT_FRAME_OFFSET_X = -40
NEXT_FRAME_OFFSET_Y = 20
NEXT_FRAME_WIDTH = 130
NEXT_FRAME_HEIGHT = 480
NEXT_MINO_OFFSET_X = -60
NEXT_MINO_1_OFFSET_Y = -150
NEXT_MINO_2_OFFSET_Y = 0
NEXT_MINO_3_OFFSET_Y = 150

# Colors
COLOR_BACKGROUND = (0, 0, 100)
COLOR_GRID_LINE = (128, 128, 128)
COLOR_BORDER = (0, 255, 255)
COLOR_TEXT = (255, 255, 255)
COLOR_NEXT_FRAME = (255, 255, 255)
