import pygame
from dataclasses import dataclass,field
import time
import random

pygame.init()
screen=pygame.display.set_mode((620,420))
clock=pygame.time.Clock()
font=pygame.font.SysFont('comicscansms',14)

@dataclass
class MazeGame:
    height: int=field(init=False,default=None)
    width: int=field(init=False,default=None)
    floormap:list=field(init=False,default=None)


    def set_floormap(self,height,width,floormap):
        self.height=height
        self.width=width
        self.floormap=floormap

    def from_file(self, filename):
        self.floormap = []
        with open(filename) as file:
            first_line = file.readline().rsplit(",")
            self.height = int(first_line[0])
            self.width = int(first_line[1])
            for line in file:
                self.floormap.append(line.rstrip("\n"))
            if len(self.floormap) != self.height:
                raise Exception("mismatch map data (height)")


    def draw(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.floormap[y][x]=="1":
                    pygame.draw.rect(screen,(238,130,238),(30*x+40,30*y+40,30,30))
                elif self.floormap[y][x]=="8":
                    text = font.render("start", True, (255,0,0))
                    screen.blit(text, (30*x+40,30*y+55))
                elif self.floormap[y][x]=="9":
                    text = font.render("Goal", True, (255, 0, 0))
                    screen.blit(text, (30*x+50,30*y+50))

    def random_visit(self,i,j):
        s=[]
        if i<=self.width and j<=self.height:
            if self.floormap[i-1][j]=="0" :
                s.append((i-1,j))
            if self.floormap[i][j-1]=="0":
                s.append((i,j-1))
            if self.floormap[i][j-1]=="9":
                text = font.render("Win!!", True, (0, 0, 0))
                screen.blit(text, (200,450))
            if self.floormap[i][j+1]=="0":
                s.append((i,j+1))
            if self.floormap[i][j+1]=="9":
                text = font.render("Win!!", True, (0, 0, 0))
                screen.blit(text, (200, 450))
            if self.floormap[i+1][j]=="0":
                s.append((i+1,j))
            if self.floormap[i+1][j]=="9":
                text = font.render("Win!!", True, (0, 0, 0))
                screen.blit(text, (200, 450))
            if s!=[]:
                r=random.choice(s)
                a=list(self.floormap[r[0]])
                a[r[1]]="5"
                self.floormap[r[0]]=''.join(a)
                i2=r[0]
                j2=r[1]
                pygame.draw.rect(screen,(148,0,211),(30 * j2 + 40, 30 * i2 + 40, 30,30))
                time.sleep(0.05)
                pygame.display.flip()
                self.random_visit(i2,j2)


    def start(self):
        self.from_file(r"C:\Users\admin\PycharmProjects\untitled\ex11\ex11-2-move.txt")
        self.draw()
        loop=True
        while loop==True:
            self.animation()

    def animation(self):
        self.random_visit(0,1)

game=MazeGame()
game.start()

pygame.quit()
