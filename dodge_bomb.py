import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))
DELTA = {pg.K_UP:(0, -5),
         pg.K_DOWN:(0, 5),
         pg.K_LEFT:(-5, 0),
         pg.K_RIGHT:(5, 0),
         }

def cheak_bound(rct: pg.Rect):
    """
    引数で与えられたRectが画面の中か外かを判定する
    引数：こうかとんRect or 爆弾Rect
    戻り値：真理値タプル（横，縦）／画面内：True，画面外：False
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate


def gameover(screen: pg.Surface):
    black_img = pg.Surface((1100, 650))
    pg.draw.rect(black_img, 0, (0, 0, 1100, 650))
    black_rct = black_img.get_rect()
    black_rct.center = WIDTH/2, HEIGHT/2
    black_img.set_alpha(128)
    screen.blit(black_img, black_rct)

    text_gameover = pg.font.Font(None, 80)
    text = text_gameover.render("Game Over", True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center=(WIDTH/2, HEIGHT/2)
    screen.blit(text, text_rect)

    kk_cry = pg.image.load("fig/8.png")      
    kk_cry_rct_1 = kk_cry.get_rect()
    kk_cry_rct_2 = kk_cry.get_rect()
    kk_cry_rct_1.center =WIDTH/2-200, HEIGHT/2
    kk_cry_rct_2.center =WIDTH/2+200, HEIGHT/2
    screen.blit(kk_cry, kk_cry_rct_1)
    screen.blit(kk_cry, kk_cry_rct_2)

    print("ゲームオーバー")
    pg.display.update()
    time.sleep(5)
    return black_rct


def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    lst_1=[]
    accs = [a for a in range(1, 11)]
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        lst_1.append(bb_img)
    return lst_1, accs


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bb_img = pg.Surface((20, 20))  # 爆弾用の空Surface
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 爆弾円を描く
    bb_img.set_colorkey((0, 0, 0))  # 四隅の黒を透過させる
    bb_rct = bb_img.get_rect()  # 爆弾Rectの抽出
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    vx, vy = +5, +5  # 爆弾速度ベクトル

    clock = pg.time.Clock()
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        
        if kk_rct.colliderect(bb_rct):
            return gameover(screen)

        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, tpl in DELTA.items():#keyと値をを取り出せる
            if key_lst[key]:
                sum_mv[0] = tpl[0]
                sum_mv[1] = tpl[1]

                # if key_lst[pg.K_UP]:
                #     sum_mv[1] -= 5
                # if key_lst[pg.K_DOWN]:
                #     sum_mv[1] += 5
                # if key_lst[pg.K_LEFT]:
                #     sum_mv[0] -= 5
                # if key_lst[pg.K_RIGHT]:
                #     sum_mv[0] += 5
        kk_rct.move_ip(sum_mv)
        if cheak_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)

        bb_rct.move_ip(vx, vy)  # 爆弾動く
        yoko, tate = cheak_bound(bb_rct)
        if not yoko:  # 横にはみ出てる
            vx *= -1
        if not tate:  # 縦にはみ出てる
            vy *= -1

        bb_imgs, bb_accs = init_bb_imgs()
        avx = vx*bb_accs[min(tmr//500, 9)]
        bb_img = bb_imgs[min(tmr//500, 9)]

        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
