# -*- coding: utf-8 -*-
import pygame
import copy
from helpers import get_mino_positions,draw_gridlines,update_score
from constants import (
    S_WIDTH, S_HEIGHT, PLAY_WIDTH, PLAY_HEIGHT, BLOCK_SIZE,
    TOP_LEFT_X, TOP_LEFT_Y, GRID_WIDTH, GRID_HEIGHT,
    COLOR_BACKGROUND, COLOR_BORDER, COLOR_TEXT, COLOR_NEXT_FRAME,
    FONT_NAME, FONT_SIZE, BORDER_WIDTH,
    SCORE_LABEL_X, SCORE_LABEL_Y, END_MSG_X, END_MSG_Y,
    NEXT_LABEL_OFFSET_X, NEXT_LABEL_OFFSET_Y,
    NEXT_FRAME_OFFSET_X, NEXT_FRAME_OFFSET_Y, NEXT_FRAME_WIDTH, NEXT_FRAME_HEIGHT,
    NEXT_MINO_OFFSET_X, NEXT_MINO_1_OFFSET_Y, NEXT_MINO_2_OFFSET_Y, NEXT_MINO_3_OFFSET_Y,
    MINO_ROTATION_STATES, MINO_GRID_SIZE
)


#ゲーム画面を描画する関数
def draw_window(surface,grid,score):
    surface.fill(COLOR_BACKGROUND)#initialize

    pygame.font.init()
    font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)#Font, Size

    #Score:
    label = font.render('Score:'+str(score), 1, COLOR_TEXT)#Top title, Color
    surface.blit(label, (SCORE_LABEL_X - label.get_width()/2, SCORE_LABEL_Y))#Location

    #End Game: Enter "esc"
    label = font.render('End: Enter "esc"', 1, COLOR_TEXT)#Top title, Color
    surface.blit(label, (END_MSG_X - label.get_width()/2, END_MSG_Y))#Location

    for i in range(len(grid)):#20
        for j in range(len(grid[i])):#10
            #gridの情報から固定ミノ(ミノがない背景部分も含む)を描画
            pygame.draw.rect(surface, grid[i][j], (TOP_LEFT_X + j*BLOCK_SIZE, TOP_LEFT_Y + i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    draw_gridlines(surface)

    #play画面の外枠を描画
    pygame.draw.rect(surface, COLOR_BORDER, (TOP_LEFT_X, TOP_LEFT_Y, PLAY_WIDTH, PLAY_HEIGHT), BORDER_WIDTH)

#消せるラインの判定と、そのラインを消す関数
def clear_rows(locked_pos,score):
    for i,row in enumerate(locked_pos):#i:index, row:values
        if (0,0,0) not in row: #列の中に黒色（背景色）がない（＝全てミノで埋まっている）場合
            for j in reversed(range(i)):#下の行から順番に
                locked_pos[j+1] = copy.deepcopy(locked_pos[j])#１列下に置き換えていく
            score = update_score(score)
    return score

#GameOverの判定を行う（不十分）
def check_lost(locked_pos):
    for t in locked_pos[0]:
        if not t == (0,0,0):
            return True
    return False

def valid_space(grid,mino):
    #grid = 0,0,0となる（＝ミノが存在しない）全ての座標が格納された配列を生成
    accepted_pos = [[(j,i) for j in range(GRID_WIDTH) if grid[i][j]==(0,0,0)]for i in range(GRID_HEIGHT) ]
    #3次元配列になってしまっているので、2次元配列に変更（実質的な中身の値は変わらない）
    accepted_pos = [_ for sub in accepted_pos for _ in sub]

    #現在minoの座標を取得
    mino_pos = get_mino_positions(mino)

    #当たり判定
    for pos in mino_pos:#minoの各セルごとに
        if not pos in accepted_pos:#acceptedでない場合
            return False
    return True

#現在ミノを固定ミノにする関数
def lock_mino(locked_pos,mino):
    mino_pos = get_mino_positions(mino)
    for m in mino_pos:
        locked_pos[m[1]][m[0]] = mino.color # m[0]=x, m[1]=y
    return locked_pos

#固定ミノ座標情報から現在gridを作成
def create_grid(locked_pos):
    grid = copy.deepcopy(locked_pos)
    return grid


def keyOperation(game_running, key, grid, current_mino):
    # ESCキーの処理は main() で行うため、ここでは処理しない
    if key == pygame.K_LEFT:
        current_mino.x -= 1
        if not valid_space(grid, current_mino):
            current_mino.x += 1
    elif key == pygame.K_RIGHT:
        current_mino.x += 1
        if not valid_space(grid, current_mino):
            current_mino.x -= 1
    elif key == pygame.K_DOWN:
        current_mino.y += 1
        if not valid_space(grid, current_mino):
            current_mino.y -= 1
    elif key == pygame.K_UP:
        current_mino.rotation += 1
        current_mino.rotation %= MINO_ROTATION_STATES
        if not valid_space(grid, current_mino):
            current_mino.rotation += 3
            current_mino.rotation %= MINO_ROTATION_STATES
    elif key == pygame.K_RSHIFT:
        is_falling = True
        while is_falling:
            current_mino.y += 1
            if not valid_space(grid, current_mino):
                current_mino.y -= 1
                is_falling = False
    return game_running, current_mino

#1つのミノを指定座標に描画する関数
def _draw_single_mino(mino, surface, x, y):
    """指定された位置に1つのミノを描画する"""
    for i in range(MINO_GRID_SIZE):
        for j in range(MINO_GRID_SIZE):
            if mino.shape[mino.rotation][i][j] == 1:
                pygame.draw.rect(surface, mino.color,
                               (x + j*BLOCK_SIZE, y + i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

#画面に次のミノを表示する関数
def draw_next_shape(mino, mino2, mino3, surface):
    label_x = S_WIDTH - PLAY_WIDTH/2 + NEXT_LABEL_OFFSET_X
    label_y = S_HEIGHT/2 + NEXT_LABEL_OFFSET_Y
    font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
    label = font.render('Next', 1, COLOR_TEXT)
    surface.blit(label, (label_x, label_y))

    #next_minoを表示する外枠を表示
    pygame.draw.rect(surface, COLOR_NEXT_FRAME,
                    (label_x + NEXT_FRAME_OFFSET_X, label_y + NEXT_FRAME_OFFSET_Y,
                     NEXT_FRAME_WIDTH, NEXT_FRAME_HEIGHT), BORDER_WIDTH)

    # 3つのミノを順番に描画
    next_minos = [mino, mino2, mino3]
    y_offsets = [NEXT_MINO_1_OFFSET_Y, NEXT_MINO_2_OFFSET_Y, NEXT_MINO_3_OFFSET_Y]
    base_x = S_WIDTH - PLAY_WIDTH/2 + NEXT_MINO_OFFSET_X
    base_y = S_HEIGHT/2

    for next_mino, y_offset in zip(next_minos, y_offsets):
        _draw_single_mino(next_mino, surface, base_x, base_y + y_offset)
