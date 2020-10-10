# -*- coding: utf-8 -*-
import pygame
import random
import datetime
import copy
from Tetris_module import draw_gridlines,draw_window,clear_rows,get_mino_positions
from Tetris_module import valid_space,lock_mino,create_grid,keyOparation,check_lost
from Tetris_module import draw_next_shape

s_width = 800 #display_size
s_height = 700 #display_size
play_width = 300 #play_size 360//30 = 10 blocks
play_height = 600 #play_size 660//30 = 20 blocks
block_size = 30
top_left_x = (s_width - play_width) / 2 #play_sizeの左上x座標
top_left_y = (s_height - play_height) / 2 #play_sizeの左上y座標

# SHAPE FORMATS
J = [
# MINO_ANGLE_0
                [[0,0,0,0,0],
               [0,0,1,0,0],
               [0,0,1,0,0],
               [0,1,1,0,0],
               [0,0,0,0,0]],
# MINO_ANGLE_90
                [[0,0,0,0,0],
               [0,1,0,0,0],
               [0,1,1,1,0],
               [0,0,0,0,0],
               [0,0,0,0,0]],
# MINO_ANGLE_180
                [[0,0,0,0,0],
                [0,0,1,1,0],
               [0,0,1,0,0],
               [0,0,1,0,0],
               [0,0,0,0,0]],
# MINO_ANGLE_270
                [[0,0,0,0,0],
                [0,0,0,0,0],
               [0,1,1,1,0],
               [0,0,0,1,0],
               [0,0,0,0,0]]
               ]

L = [
# MINO_ANGLE_0
                [[0,0,0,0,0],
               [0,0,1,0,0],
               [0,0,1,0,0],
               [0,0,1,1,0],
               [0,0,0,0,0]],
# MINO_ANGLE_90
                [[0,0,0,0,0],
                [0,0,0,0,0],
               [0,1,1,1,0],
               [0,1,0,0,0],
               [0,0,0,0,0]],
# MINO_ANGLE_180
                [[0,0,0,0,0],
                [0,1,1,0,0],
               [0,0,1,0,0],
               [0,0,1,0,0],
               [0,0,0,0,0]],
# MINO_ANGLE_270
                [[0,0,0,0,0],
               [0,0,0,1,0],
               [0,1,1,1,0],
               [0,0,0,0,0],
               [0,0,0,0,0]]
               ]

S = [
# MINO_ANGLE_0
                [[0,0,0,0,0],
               [0,0,1,1,0],
               [0,1,1,0,0],
               [0,0,0,0,0],
               [0,0,0,0,0]],
# MINO_ANGLE_90
                [[0,0,0,0,0],
                [0,0,1,0,0],
               [0,0,1,1,0],
               [0,0,0,1,0],
               [0,0,0,0,0]],
# MINO_ANGLE_180
                [[0,0,0,0,0],
               [0,0,1,1,0],
               [0,1,1,0,0],
               [0,0,0,0,0],
               [0,0,0,0,0]],
# MINO_ANGLE_270
                [[0,0,0,0,0],
                [0,0,1,0,0],
               [0,0,1,1,0],
               [0,0,0,1,0],
               [0,0,0,0,0]]
               ]

Z = [
# MINO_ANGLE_0
                [[0,0,0,0,0],
               [0,1,1,0,0],
               [0,0,1,1,0],
               [0,0,0,0,0],
               [0,0,0,0,0]],
# MINO_ANGLE_90
                [[0,0,0,0,0],
               [0,0,1,0,0],
               [0,1,1,0,0],
               [0,1,0,0,0],
               [0,0,0,0,0]],
# MINO_ANGLE_180
                [[0,0,0,0,0],
               [0,1,1,0,0],
               [0,0,1,1,0],
               [0,0,0,0,0],
               [0,0,0,0,0]],
# MINO_ANGLE_270
                [[0,0,0,0,0],
               [0,0,1,0,0],
               [0,1,1,0,0],
               [0,1,0,0,0],
               [0,0,0,0,0]]
               ]

I = [
# MINO_ANGLE_0
                [[0,0,1,0,0],
               [0,0,1,0,0],
               [0,0,1,0,0],
               [0,0,1,0,0],
               [0,0,0,0,0]],
# MINO_ANGLE_90
                [[0,0,0,0,0],
               [0,0,0,0,0],
               [1,1,1,1,0],
               [0,0,0,0,0],
               [0,0,0,0,0]],
# MINO_ANGLE_180
                [[0,0,1,0,0],
               [0,0,1,0,0],
               [0,0,1,0,0],
               [0,0,1,0,0],
               [0,0,0,0,0]],
# MINO_ANGLE_270
                [[0,0,0,0,0],
               [0,0,0,0,0],
               [1,1,1,1,0],
               [0,0,0,0,0],
               [0,0,0,0,0]]
               ]

T = [
# MINO_ANGLE_0
                [[0,0,0,0,0],
               [0,0,1,0,0],
               [0,1,1,1,0],
               [0,0,0,0,0],
               [0,0,0,0,0]],
# MINO_ANGLE_90
                [[0,0,0,0,0],
                [0,0,1,0,0],
               [0,0,1,1,0],
               [0,0,1,0,0],
               [0,0,0,0,0]],
# MINO_ANGLE_180
                [[0,0,0,0,0],
                [0,0,0,0,0],
               [0,1,1,1,0],
               [0,0,1,0,0],
               [0,0,0,0,0]],
# MINO_ANGLE_270
                [[0,0,0,0,0],
               [0,0,1,0,0],
               [0,1,1,0,0],
               [0,0,1,0,0],
               [0,0,0,0,0]]
               ]

O = [
# MINO_ANGLE_0
                [[0,0,0,0,0],
                [0,0,0,0,0],
               [0,1,1,0,0],
               [0,1,1,0,0],
               [0,0,0,0,0]],
# MINO_ANGLE_90
                [[0,0,0,0,0],
                [0,0,0,0,0],
               [0,1,1,0,0],
               [0,1,1,0,0],
               [0,0,0,0,0]],
# MINO_ANGLE_180
                [[0,0,0,0,0],
                [0,0,0,0,0],
               [0,1,1,0,0],
               [0,1,1,0,0],
               [0,0,0,0,0]],
# MINO_ANGLE_270
                [[0,0,0,0,0],
                [0,0,0,0,0],
               [0,1,1,0,0],
               [0,1,1,0,0],
               [0,0,0,0,0]]
               ]

shapes = [S,Z,I,O,J,L,T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]

class Mino(object):
    def __init__(self,x,y,shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0 #number from 0-3#回転角度の初期値は常に０度

#ランダムにミノを取得
def get_shape():
    global shapes
    return Mino(3,0,random.choice(shapes))#starting position and shape

def main():
    #ゲーム画面生成
    surface = pygame.display.set_mode((s_width,s_height))#displayを定義
    pygame.display.set_caption('Tetris')#Top bar_title

    #初期値となる固定ミノの情報を保持する配列を生成（0埋めなので、全部黒になる）
    locked_positions = [[(0,0,0) for _ in range(int(play_width/block_size))] for _ in range(int(play_height/block_size))]

    #初期値となるmino取得
    current_mino = get_shape()
    next_mino = get_shape()
    next_mino2 = get_shape()
    next_mino3 = get_shape()

    score = 0
    run = True #While関数を走らせるためのフラグ
    time_t = (datetime.datetime.now()).second #秒数取得
    #ループ
    while run:
        #現在gridに固定ミノ座標を登録
        grid = create_grid(locked_positions)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: #ESC key
                run = False
                pygame.display.quit()
            if event.type == pygame.KEYDOWN: #ESC以外のキー入力（矢印キーとシフトキー）
                run,current_mino = keyOparation(run,event.key,grid,current_mino)

        second = (datetime.datetime.now()).second #秒数取得
        if time_t != second: #1秒経過した場合
            time_t = second
            current_mino.y += 1 #ミノを1マス落下
            if not valid_space(grid,current_mino):#当たり判定で重なってしまう場合
                current_mino.y -= 1#ミノを重ならない状態に戻す
                locked_positions = lock_mino(locked_positions,current_mino)#現在ミノを固定ミノにする
                current_mino = copy.deepcopy(next_mino)#次ミノを現在ミノに繰りこし
                next_mino = copy.deepcopy(next_mino2)
                next_mino2 = copy.deepcopy(next_mino3)
                next_mino3 = get_shape()
                score = clear_rows(locked_positions,score)#ライン消し関数

        #draw current_mino in grid
        for i in range(len(current_mino.shape[current_mino.rotation])):#4
            for j in range(len(current_mino.shape[current_mino.rotation][i])):#4
                if current_mino.shape[current_mino.rotation][j][i] == 1:
                    grid[j+current_mino.y][i+current_mino.x] = current_mino.color

        draw_window(surface,grid,score)#play画面に表示
        draw_next_shape(next_mino,next_mino2,next_mino3,surface)#次のミノを表示
        pygame.display.update()#画面更新

        if check_lost(locked_positions):
            print('you lost')
            # draw_text_middle(surface,'YOU LOST!',80,(255,255,255))
            pygame.display.update()
            run = False

if __name__ == "__main__":
    main()
