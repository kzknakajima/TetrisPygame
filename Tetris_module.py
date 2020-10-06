# -*- coding: utf-8 -*-
import pygame
import copy

s_width = 800 #display_size
s_height = 700 #display_size
play_width = 300 #play_size 360//30 = 10 blocks
play_height = 600 #play_size 660//30 = 20 blocks
block_size = 30
top_left_x = (s_width - play_width) / 2 #play_sizeの左上x座標
top_left_y = (s_height - play_height) / 2 #play_sizeの左上y座標

#play画面内にグリッド線を引く関数
def draw_gridlines(surface):
    for i in range(int(play_width/block_size)):
        pygame.draw.line(surface,(128,128,128),(top_left_x+i*block_size,top_left_y),(top_left_x+i*block_size,top_left_y+play_height),1)
    for i in range(int(play_height/block_size)):
        pygame.draw.line(surface,(128,128,128),(top_left_x,top_left_y+i*block_size),(top_left_x+play_width,top_left_y+i*block_size),1)

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

def get_mino_positions(mino):
    mino_pos = []
    for i in range(4):
        for j in range(4):#4x4
            if mino.shape[mino.rotation][i][j] == 1:#相対座標上にminoが存在すれば
                mino_pos.append((mino.x+j,mino.y+i))#minoの絶対座標(x,y)をappend
    return mino_pos

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
