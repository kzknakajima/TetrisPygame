# -*- coding: utf-8 -*-

def get_mino_positions(mino):
    mino_pos = []
    for i in range(4):
        for j in range(4):#4x4
            if mino.shape[mino.rotation][i][j] == 1:#相対座標上にminoが存在すれば
                mino_pos.append((mino.x+j,mino.y+i))#minoの絶対座標(x,y)をappend
    return mino_pos
