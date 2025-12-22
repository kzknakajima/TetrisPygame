# -*- coding: utf-8 -*-
import pygame
import random
import datetime
import copy
from Tetris_module import draw_gridlines,draw_window,clear_rows,get_mino_positions
from Tetris_module import valid_space,lock_mino,create_grid,keyOperation,check_lost
from Tetris_module import draw_next_shape
from constants import (
    S_WIDTH, S_HEIGHT, PLAY_WIDTH, PLAY_HEIGHT, BLOCK_SIZE,
    GRID_WIDTH, GRID_HEIGHT, MINO_START_X, MINO_START_Y, MINO_GRID_SIZE
)
from shapes import SHAPES, SHAPE_COLORS

class Mino(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = SHAPE_COLORS[SHAPES.index(shape)]
        self.rotation = 0  # 回転角度の初期値は常に0度

#ランダムにミノを取得
def get_shape():
    return Mino(MINO_START_X, MINO_START_Y, random.choice(SHAPES))  # starting position and shape

def main():
    #ゲーム画面生成
    surface = pygame.display.set_mode((S_WIDTH, S_HEIGHT))  # displayを定義
    pygame.display.set_caption('Tetris')  # Top bar_title

    #初期値となる固定ミノの情報を保持する配列を生成（0埋めなので、全部黒になる）
    locked_positions = [[(0, 0, 0) for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

    #初期値となるmino取得
    current_mino = get_shape()
    next_mino = get_shape()
    next_mino2 = get_shape()
    next_mino3 = get_shape()

    score = 0
    game_running = True  # ゲームループを走らせるためのフラグ
    last_fall_second = (datetime.datetime.now()).second  # 最後に落下した時刻（秒）
    #ループ
    while game_running:
        #現在gridに固定ミノ座標を登録
        grid = create_grid(locked_positions)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # ESC key
                game_running = False
                pygame.display.quit()
            if event.type == pygame.KEYDOWN:  # ESC以外のキー入力（矢印キーとシフトキー）
                game_running, current_mino = keyOperation(game_running, event.key, grid, current_mino)

        current_second = (datetime.datetime.now()).second  # 現在の秒数取得
        if last_fall_second != current_second:  # 1秒経過した場合
            last_fall_second = current_second
            current_mino.y += 1  # ミノを1マス落下
            if not valid_space(grid, current_mino):  # 当たり判定で重なってしまう場合
                current_mino.y -= 1  # ミノを重ならない状態に戻す
                locked_positions = lock_mino(locked_positions, current_mino)  # 現在ミノを固定ミノにする
                current_mino = copy.deepcopy(next_mino)  # 次ミノを現在ミノに繰りこし
                next_mino = copy.deepcopy(next_mino2)
                next_mino2 = copy.deepcopy(next_mino3)
                next_mino3 = get_shape()
                score = clear_rows(locked_positions, score)  # ライン消し関数

        #draw current_mino in grid
        for i in range(MINO_GRID_SIZE):
            for j in range(MINO_GRID_SIZE):
                if current_mino.shape[current_mino.rotation][j][i] == 1:
                    grid[j+current_mino.y][i+current_mino.x] = current_mino.color

        draw_window(surface, grid, score)  # play画面に表示
        draw_next_shape(next_mino, next_mino2, next_mino3, surface)  # 次のミノを表示
        pygame.display.update()  # 画面更新

        if check_lost(locked_positions):
            print('you lost')
            # draw_text_middle(surface,'YOU LOST!',80,(255,255,255))
            pygame.display.update()
            game_running = False

if __name__ == "__main__":
    main()
