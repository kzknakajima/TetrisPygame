# -*- coding: utf-8 -*-
import pygame
import copy
from Tetris_sub_module import get_mino_positions,draw_gridlines

s_width = 800 #display_size
s_height = 700 #display_size
play_width = 300 #play_size 360//30 = 10 blocks
play_height = 600 #play_size 660//30 = 20 blocks
block_size = 30
top_left_x = (s_width - play_width) / 2 #play_sizeの左上x座標
top_left_y = (s_height - play_height) / 2 #play_sizeの左上y座標


#ゲーム画面を描画する関数
def draw_window(surface,grid):
    surface.fill((0, 0, 100))#initialize

    #Score:
    pygame.font.init()
    font = pygame.font.SysFont('comicsans',30)#Font, Size
    label = font.render('Score:',1,(255,255,255))#Top title, Color
    surface.blit(label,(110 - label.get_width()/2, 30))#Location

    #End Game: Enter "esc"
    pygame.font.init()
    font = pygame.font.SysFont('comicsans',30)#Font, Size
    label = font.render('End: Enter "esc"',1,(255,255,255))#Top title, Color
    surface.blit(label,(110 - label.get_width()/2, 650))#Location

    for i in range(len(grid)):#20
        for j in range(len(grid[i])):#10
            #gridの情報から固定ミノ(ミノがない背景部分も含む)を描画
            pygame.draw.rect(surface,grid[i][j],(top_left_x + j*30,top_left_y + i*30,block_size,block_size),0)

    draw_gridlines(surface)

    #play画面の外枠を描画
    pygame.draw.rect(surface,(0,255,255),(top_left_x,top_left_y,play_width,play_height),3)

#消せるラインの判定と、そのラインを消す関数
def clear_rows(locked_pos):
    for i,row in enumerate(locked_pos):#i:index, row:values
        if (0,0,0) not in row: #列の中に黒色（背景色）がない（＝全てミノで埋まっている）場合
            for j in reversed(range(i)):#下の行から順番に
                locked_pos[j+1] = copy.deepcopy(locked_pos[j])#１列下に置き換えていく

#GameOverの判定を行う（不十分）
def check_lost(locked_pos):
    for t in locked_pos[0]:
        if not t == (0,0,0):
            return True
    return False

def valid_space(grid,mino):
    #grid = 0,0,0となる（＝ミノが存在しない）全ての座標が格納された配列を生成
    accepted_pos = [[(j,i) for j in range(10) if grid[i][j]==(0,0,0)]for i in range(20) ]
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

#画面に次のミノを表示する関数
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
