import pygame

s_width = 800 #display_size
s_height = 700 #display_size
play_width = 300 #play_size 360//30 = 10 blocks
play_height = 600 #play_size 660//30 = 20 blocks
block_size = 30
top_left_x = (s_width - play_width) / 2 #play_sizeの左上x座標
top_left_y = (s_height - play_height) / 2 #play_sizeの左上y座標

def draw_gridlines(surface):
    for i in range(int(play_width/block_size)):
        pygame.draw.line(surface,(128,128,128),(top_left_x+i*block_size,top_left_y),(top_left_x+i*block_size,top_left_y+play_height),1)
    for i in range(int(play_height/block_size)):
        pygame.draw.line(surface,(128,128,128),(top_left_x,top_left_y+i*block_size),(top_left_x+play_width,top_left_y+i*block_size),1)
