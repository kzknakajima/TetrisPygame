# -*- coding: utf-8 -*-
import pygame
import random
import datetime
import copy
from Tetris_module import draw_gridlines,draw_window,clear_rows,get_mino_positions,valid_space

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
        self.rotation = 0 #number from 0-3

#盤面を作成
def create_grid(locked_pos):
    # grid = [[(0,0,0) for _ in range(int(play_width/block_size))] for _ in range(int(play_height/block_size))]#width,height = 10,20
    grid = copy.deepcopy(locked_pos)

    return grid


def get_shape():
    global shapes
    return Mino(3,0,random.choice(shapes))#starting position and shape


def draw_next_shape(mino,mino2,mino3,surface):
    label_x = s_width-play_width/2 -40
    label_y = s_height/2-200
    font = pygame.font.SysFont('comicsans',30)
    label = font.render('Next Shape',1,(255,255,255))
    surface.blit(label,(label_x,label_y))

    next_top_left_x = s_width-play_width/2 -60
    next_top_left_y = s_height/2 - 150
    for i in range(len(mino.shape[mino.rotation])):#4
        for j in range(len(mino.shape[mino.rotation][i])):#4
            if mino.shape[mino.rotation][i][j] == 1:
                pygame.draw.rect(surface,mino.color,(next_top_left_x+j*30,next_top_left_y+i*30,block_size,block_size),0)

    next_top_left_x = s_width-play_width/2 -60
    next_top_left_y = s_height/2
    for i in range(len(mino2.shape[mino.rotation])):#4
        for j in range(len(mino2.shape[mino.rotation][i])):#4
            if mino2.shape[mino2.rotation][i][j] == 1:
                pygame.draw.rect(surface,mino2.color,(next_top_left_x+j*30,next_top_left_y+i*30,block_size,block_size),0)

    next_top_left_x = s_width-play_width/2 -60
    next_top_left_y = s_height/2 + 150
    for i in range(len(mino3.shape[mino.rotation])):#4
        for j in range(len(mino3.shape[mino.rotation][i])):#4
            if mino3.shape[mino3.rotation][i][j] == 1:
                pygame.draw.rect(surface,mino3.color,(next_top_left_x+j*30,next_top_left_y+i*30,block_size,block_size),0)





def lock_mino(locked_pos,mino):
    mino_pos = get_mino_positions(mino)
    for m in mino_pos:
        locked_pos[m[1]][m[0]] = mino.color # m[0]=x, m[1]=y

    return locked_pos

def keyOparation(run,key,grid,current_mino):
    if key == pygame.K_ESCAPE:
        run = False
        pygame.display.quit()
    elif key == pygame.K_LEFT:
        current_mino.x -= 1
        if not valid_space(grid,current_mino):
            current_mino.x += 1
    elif key == pygame.K_RIGHT:
        current_mino.x += 1
        if not valid_space(grid,current_mino):
            current_mino.x -= 1
    elif key == pygame.K_DOWN:
        current_mino.y += 1
        if not valid_space(grid,current_mino):
            current_mino.y -= 1
    elif key == pygame.K_UP:
        current_mino.rotation += 1
        current_mino.rotation %= 4
        if not valid_space(grid,current_mino):
            current_mino.rotation += 3
            current_mino.rotation %= 4
    elif key == pygame.K_RSHIFT:
        flag = True
        while flag:
            current_mino.y += 1
            if not valid_space(grid,current_mino):
                current_mino.y -= 1
                flag = False

    return run,current_mino

def check_lost(locked_pos):
    for t in locked_pos[0]:
        if not t == (0,0,0):
            return True
    return False


def main():
    #ゲーム画面生成
    surface = pygame.display.set_mode((s_width,s_height))#displayを定義
    pygame.display.set_caption('Tetris')#Top bar_title

    #固定ミノの情報を保持する配列の初期値（0埋めなので、全部黒になる）
    locked_positions = [[(0,0,0) for _ in range(int(play_width/block_size))] for _ in range(int(play_height/block_size))]

    #初期値となるmino取得
    current_mino = get_shape()
    next_mino = get_shape()
    next_mino2 = get_shape()
    next_mino3 = get_shape()

    run = True #While関数を走らせるためのフラグ

    time_t = (datetime.datetime.now()).second #秒数取得
    while run:
        grid = create_grid(locked_positions)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: #ESC key
                run = False
                pygame.display.quit()

            if event.type == pygame.KEYDOWN: #ESC以外のキー入力
                run,current_mino = keyOparation(run,event.key,grid,current_mino)

        second = (datetime.datetime.now()).second #秒数取得
        if time_t != second: #1秒経過した場合
            time_t = second
            current_mino.y += 1 #ミノを1マス落下
            if not valid_space(grid,current_mino):#当たり判定で重なってしまう場合
                current_mino.y -= 1#ミノを重ならない状態に戻す
                locked_positions = lock_mino(locked_positions,current_mino)#現在ミノを固定ミノにする
                current_mino = copy.deepcopy(next_mino)
                next_mino = copy.deepcopy(next_mino2)
                next_mino2 = copy.deepcopy(next_mino3)
                next_mino3 = get_shape()
                clear_rows(locked_positions)#ライン消し関数


        #draw current_mino in grid
        for i in range(len(current_mino.shape[current_mino.rotation])):#4
            for j in range(len(current_mino.shape[current_mino.rotation][i])):#4
                if current_mino.shape[current_mino.rotation][j][i] == 1:
                    grid[j+current_mino.y][i+current_mino.x] = current_mino.color

        draw_window(surface,grid)
        draw_next_shape(next_mino,next_mino2,next_mino3,surface)
        pygame.display.update()

        if check_lost(locked_positions):
            print('you lost')
            # draw_text_middle(surface,'YOU LOST!',80,(255,255,255))
            pygame.display.update()
            run = False


if __name__ == "__main__":
    main()
