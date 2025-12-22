# -*- coding: utf-8 -*-
import pygame
import random
import copy
from game_logic import draw_gridlines,draw_window,clear_rows,get_mino_positions
from game_logic import valid_space,lock_mino,create_grid,keyOperation,check_lost
from game_logic import draw_next_shape
from constants import (
    S_WIDTH, S_HEIGHT, PLAY_WIDTH, PLAY_HEIGHT, BLOCK_SIZE,
    GRID_WIDTH, GRID_HEIGHT, MINO_START_X, MINO_START_Y, MINO_GRID_SIZE,
    FALL_INTERVAL, FPS
)
from shapes import SHAPES, SHAPE_COLORS

class Mino(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = SHAPE_COLORS[SHAPES.index(shape)]
        self.rotation = 0  # 回転角度の初期値は常に0度

# ランダムにミノを取得
def get_shape():
    return Mino(MINO_START_X, MINO_START_Y, random.choice(SHAPES))  # 開始位置と形状

def init_game():
    """ゲームの初期化：画面設定とグリッド生成"""
    surface = pygame.display.set_mode((S_WIDTH, S_HEIGHT))
    pygame.display.set_caption('Tetris')
    locked_positions = [[(0, 0, 0) for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    return surface, locked_positions

def init_minos():
    """ミノの初期化：現在のミノと次の3つのミノを生成"""
    current_mino = get_shape()
    next_minos = [get_shape() for _ in range(3)]
    return current_mino, next_minos

def handle_events():
    """イベント処理：QUIT、キー入力を処理"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False, None
        if event.type == pygame.KEYDOWN:
            return True, event.key
    return True, None

def handle_auto_fall(current_mino, locked_positions, next_minos, score, last_fall_time, current_time):
    """自動落下処理：ミノの落下、固定、次ミノへの切り替え"""
    if current_time - last_fall_time < FALL_INTERVAL:
        return current_mino, locked_positions, next_minos, score, last_fall_time

    # ミノを1マス落下
    current_mino.y += 1
    grid = create_grid(locked_positions)

    if not valid_space(grid, current_mino):
        # 当たり判定で重なる場合、ミノを固定
        current_mino.y -= 1
        locked_positions = lock_mino(locked_positions, current_mino)

        # 次ミノを現在ミノに、新しいミノを生成
        current_mino = copy.deepcopy(next_minos[0])
        next_minos = next_minos[1:] + [get_shape()]

        # ライン消去
        score = clear_rows(locked_positions, score)

    return current_mino, locked_positions, next_minos, score, current_time

def draw_current_mino_on_grid(grid, current_mino):
    """現在のミノをgridに描画"""
    for i in range(MINO_GRID_SIZE):
        for j in range(MINO_GRID_SIZE):
            if current_mino.shape[current_mino.rotation][j][i] == 1:
                grid[j+current_mino.y][i+current_mino.x] = current_mino.color
    return grid

def render_game(surface, grid, current_mino, next_minos, score):
    """ゲーム画面全体の描画"""
    grid = draw_current_mino_on_grid(grid, current_mino)
    draw_window(surface, grid, score)
    draw_next_shape(next_minos[0], next_minos[1], next_minos[2], surface)
    pygame.display.update()

def cleanup_game():
    """ゲーム終了時のクリーンアップ処理を一元管理"""
    pygame.display.quit()
    pygame.quit()

def main():
    """メインゲームループ"""
    # 初期化
    surface, locked_positions = init_game()
    current_mino, next_minos = init_minos()
    score = 0
    clock = pygame.time.Clock()
    last_fall_time = pygame.time.get_ticks()
    game_running = True

    # ゲームループ
    while game_running:
        clock.tick(FPS)
        grid = create_grid(locked_positions)

        # イベント処理
        game_running, key = handle_events()
        if not game_running:
            break  # 終了条件1: ×ボタン

        if key:
            if key == pygame.K_ESCAPE:
                game_running = False  # 終了条件2: ESCキー
            else:
                game_running, current_mino = keyOperation(game_running, key, grid, current_mino)

        # 自動落下処理
        current_time = pygame.time.get_ticks()
        current_mino, locked_positions, next_minos, score, last_fall_time = handle_auto_fall(
            current_mino, locked_positions, next_minos, score, last_fall_time, current_time
        )

        # 描画
        render_game(surface, grid, current_mino, next_minos, score)

        # ゲームオーバー判定
        if check_lost(locked_positions):
            print('you lost')
            pygame.display.update()
            game_running = False  # 終了条件3: ゲームオーバー

    # 終了処理（どの終了方法でも必ずここを通る）
    cleanup_game()

if __name__ == "__main__":
    main()
