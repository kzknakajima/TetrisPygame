# -*- coding: utf-8 -*-
import pygame
from constants import (
    PLAY_WIDTH, PLAY_HEIGHT, BLOCK_SIZE,
    TOP_LEFT_X, TOP_LEFT_Y, SCORE_PER_LINE,
    MINO_INNER_GRID, COLOR_GRID_LINE
)

#ミノの絶対座標を取得する関数
def get_mino_positions(mino):
    mino_pos = []
    for i in range(MINO_INNER_GRID):
        for j in range(MINO_INNER_GRID):
            if mino.shape[mino.rotation][i][j] == 1:#相対座標上にminoが存在すれば
                mino_pos.append((mino.x+j,mino.y+i))#minoの絶対座標(x,y)をappend
    return mino_pos

#play画面内にグリッド線を引く関数
def draw_gridlines(surface):
    for i in range(int(PLAY_WIDTH/BLOCK_SIZE)):
        pygame.draw.line(surface,COLOR_GRID_LINE,(TOP_LEFT_X+i*BLOCK_SIZE,TOP_LEFT_Y),(TOP_LEFT_X+i*BLOCK_SIZE,TOP_LEFT_Y+PLAY_HEIGHT),1)
    for i in range(int(PLAY_HEIGHT/BLOCK_SIZE)):
        pygame.draw.line(surface,COLOR_GRID_LINE,(TOP_LEFT_X,TOP_LEFT_Y+i*BLOCK_SIZE),(TOP_LEFT_X+PLAY_WIDTH,TOP_LEFT_Y+i*BLOCK_SIZE),1)

def update_score(score):
    score += SCORE_PER_LINE
    return score
