# -*- coding: utf-8 -*-
import pygame

s_width = 800 #display_size
s_height = 700 #display_size
play_width = 300 #play_size 360//30 = 10 blocks
play_height = 600 #play_size 660//30 = 20 blocks
block_size = 30
top_left_x = (s_width - play_width) / 2 #play_sizeの左上x座標
top_left_y = (s_height - play_height) / 2 #play_sizeの左上y座標

#ミノの絶対座標を取得する関数
def get_mino_positions(mino):
    mino_pos = []
    for i in range(4):
        for j in range(4):#4x4
            if mino.shape[mino.rotation][i][j] == 1:#相対座標上にminoが存在すれば
                mino_pos.append((mino.x+j,mino.y+i))#minoの絶対座標(x,y)をappend
    return mino_pos

#play画面内にグリッド線を引く関数
def draw_gridlines(surface):
    for i in range(int(play_width/block_size)):
        pygame.draw.line(surface,(128,128,128),(top_left_x+i*block_size,top_left_y),(top_left_x+i*block_size,top_left_y+play_height),1)
    for i in range(int(play_height/block_size)):
        pygame.draw.line(surface,(128,128,128),(top_left_x,top_left_y+i*block_size),(top_left_x+play_width,top_left_y+i*block_size),1)

def update_score(score):
    score += 100
    return score
