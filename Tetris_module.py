# -*- coding: utf-8 -*-
import pygame

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
    surface.fill((0, 0, 0))#initialize

    pygame.font.init()
    font = pygame.font.SysFont('comicsans',60)#Font, Size
    label = font.render('Score',1,(255,255,255))#Top title, Color
    surface.blit(label,(110 - label.get_width()/2, 30))#Location

    for i in range(len(grid)):#20
        for j in range(len(grid[i])):#10
            #gridの情報から固定ミノを描画
            pygame.draw.rect(surface,grid[i][j],(top_left_x + j*30,top_left_y + i*30,block_size,block_size),0)

    draw_gridlines(surface)

    #play画面の外枠を描画
    pygame.draw.rect(surface,(255,255,0),(top_left_x,top_left_y,play_width,play_height),5)
