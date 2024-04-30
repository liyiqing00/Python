import pygame
from dataclasses import dataclass
import time
import random

pygame.init()

white=(255,255,255)
black=(0,0,0)

screen_width=600
screen_height=700

screen=pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('ポケ〇ンピンボール')
start_screen=pygame.Surface(screen.get_size()).convert()  #ゲーム終了
start_screen.fill((255,255,255))
end_screen=pygame.Surface(screen.get_size()).convert()  #ゲーム終了
end_screen.fill((255,255,255))
clock=pygame.time.Clock()
font=pygame.font.SysFont('comicsansms',18)
font1=pygame.font.SysFont('comicsansms',40)
font2=pygame.font.SysFont('arialblack',70)

FPS=60
g=0

ballImg=pygame.image.load('pokeball.jpg')

@dataclass
class Ball:
    x: int
    y: int
    dx: int
    dy: int
    vx: int
    vy: int
    image: pygame.Surface

    def move(self):
        self.x += self.vx
        self.y += self.vy

    def draw(self, to_image):
        to_image.blit(self.image, (self.x, self.y))


@dataclass
class Paddle:
    x: int
    y: int
    dx: int
    dy: int
    vx: int

    def move(self):
        self.x += self.vx

    def draw(self):
        pygame.draw.rect(screen,(0,0,0),(self.x,self.y,self.dx,self.dy))

@dataclass
class Block:
    x:int
    y:int

    def draw(self):
        pygame.draw.rect(screen,(0,0,0),(self.x,self.y,40,20))

@dataclass
class Score:
    points:int

    def draw(self,text,x,y):
        screen.blit(text, (x,y))


@dataclass
class Box:
    west: int
    north: int
    east: int
    south: int
    def __init__(self, x, y, w, h):
        self.west, self.north = (x, y)
        self.east, self.south = (x + w, y + h)

    def draw_box(self):
        pygame.draw.rect(screen, (255, 255, 255), (50, 50, 400, 600))
        pygame.draw.rect(screen, (0, 0, 0), (380, 120, 2, 530))

    def draw_energy_bottom(self):
        self.rect=pygame.draw.circle(screen, (255, 25, 112), (520, 600), 30)

#===============================check==================================
    def start_check_wall(self, ball):
        if (ball.x<=380 or ball.x+ball.dx>=450) and ball.y>120:
            ball.vx = -ball.vx
        if ball.y <= 50 or ball.y + ball.dy >= 650:
            ball.vy = -ball.vy                #ボールが右のスタートのところにある
        if ball.x>=450 and 50<=ball.y<=120:
            ball.vx=-ball.vx

    def after_check_wall(self):
        if self.ball.x+self.ball.dx<=380:
            pygame.draw.rect(screen,(0,0,0),(380,50,2,100))
        if self.ball.x<=50 or self.ball.x+self.ball.dx>=380:
            self.ball.vx=-self.ball.vx
        if self.ball.y<=50 or self.ball.y+self.ball.dy>=650:
            self.ball.vy=-self.ball.vy     #ボールがスタート場所から出た

    def check_paddle(self):
        if self.paddle.y <= self.ball.y + self.ball.dy <= self.paddle.y + self.paddle.dy:
            if self.paddle.x <= self.ball.x <= self.paddle.x + self.paddle.dx:
                self.ball.vy = -self.ball.vy

    def check_block(self):
        for self.block in self.blocks:
            if self.block.y<=self.ball.y+self.ball.dy<=self.block.y+20:
                if self.block.x<=self.ball.x<=self.block.x+40:
                    self.ball.vy=-self.ball.vy
                    self.blocks.remove(self.block)
                    self.score.points+=100

#=========================set===========================================================
    def set_ball(self):
        image = pygame.image.load("pokeball.jpg").convert()  # ボール画像を読み込む
        image.set_colorkey(image.get_at((0, 0)))
        rect = image.get_rect()
        dx, dy = (rect.width, rect.height)
        ball_x,ball_y=(405,600)
        self.ball = Ball(ball_x, ball_y, dx, dy,
                         0, 0, image)                        #初速度は（0，0）が目標

    def set_paddle(self):
        dx,dy=(100,20)
        paddle_x,paddle_y=(150,500)
        self.paddle=Paddle(paddle_x,paddle_y,dx,dy,8)       #パドル初期化

    def set_blocks(self,n):
        self.blocks=[]
        for x in range(n):
            self.block = Block(150 + random.randint(0, 10) * 10, 100 +(x+1)*100)
            self.blocks.append(self.block)

    def set_score(self):
        score=0
        self.score=Score(score)

    def move_paddle(self):
        pressed_keys = pygame.key.get_pressed()  # キー情報を取得
        if pressed_keys[pygame.K_LEFT]:
            self.paddle.x -= self.paddle.vx
        if pressed_keys[pygame.K_RIGHT]:
            self.paddle.x += self.paddle.vx

    #===============before&after===================================================
    def random_vy(self,event):
        if event.button==1 and self.rect.collidepoint(event.pos):
            self.ball.vy=random.randint(3,7)
            self.ball.vx=5

    def before_game_start(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                self.random_vy(event)
        self.game_goint()
        self.start_check_wall(self.ball)
        pygame.display.flip()  # 描画内容を画面に反映する
        screen.fill((0, 25, 25))  # 塗潰し/次のflipまで反映されない

    def after_game_start(self):
        self.game_goint()
        self.after_check_wall()
        pygame.display.flip()  # 描画内容を画面に反映する
        screen.fill((0, 25, 25))  # 塗潰し/次のflipまで反映されない

    def end_game(self):
        screen.blit(end_screen,(0,0))
        if self.score.points<=500:
            img=pygame.image.load('end_1.png')
            rank_text=font.render("Your rank is 'Poke Ball'!",True,(255,0,0))
        elif self.score.points<=1000:
            img = pygame.image.load('end_2.png')
            rank_text = font.render("Your rank is 'Great Ball'!", True, (0, 0, 255))
        elif self.score.points<=1500:
            img = pygame.image.load('end_3.png')
            rank_text = font.render("Your rank is 'Ultra Ball'!", True, (255, 255, 0))
        else:
            img = pygame.image.load('end_4.png')
            rank_text = font.render("Your rank is 'Master Ball'!", True, (186,85,211))
        screen.blit(img,(210,200))
        text = font1.render("score=" + f"{self.score.points}", True, (0, 0, 0))
        self.score.draw(text,220,500)
        screen.blit(rank_text,(215,450))
        pygame.display.update()

    def game_goint(self):
        self.draw_box()
        self.draw_energy_bottom()
        self.ball.vy += g
        for event in pygame.event.get():
            # 「閉じる」ボタンを処理する
            if event.type == pygame.QUIT: loop = False
        clock.tick(FPS)  # 毎秒の呼び出し回数に合わせて遅延
        self.check_paddle()
        self.check_block()
        self.ball.move()
        self.move_paddle()
        self.ball.draw(screen)
        self.paddle.draw()
        text = font.render("score=" + f"{self.score.points}", True, (255, 255, 255))
        self.score.draw(text,460,100)
        text = font.render("ball_vy:" + f"{self.ball.vy}", True, (255, 255, 255))
        screen.blit(text, (460, 200))
        text = font.render("Click it to start", True, (255, 255, 255))
        screen.blit(text, (460, 500))
        for self.block in self.blocks:
            self.block.draw()
        if self.blocks==[] and self.ball.y>=300:
            self.set_blocks(2)

#============================animate=========================================
    def animate(self):
        loop = True
        screen.fill((0,25,25))  # 塗潰し/次のflipまで反映されない
        while loop==True: # 無限ループ
            if self.ball.x+self.ball.dx>=382:
                self.before_game_start()
            elif self.ball.x+self.ball.dx<300 and self.ball.y>=self.paddle.y+self.paddle.dy+5:
                self.end_game()
            else:
                self.after_game_start()




box = Box(0, 0, 600, 700)
draw = pygame.draw
box.set_ball()
box.set_paddle()
box.set_blocks(2)
box.set_score()
pygame.display.flip()

box.animate()



pygame.quit()
