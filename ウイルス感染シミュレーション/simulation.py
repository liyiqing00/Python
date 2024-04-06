from tkinter import *
import time,random
from dataclasses import dataclass,field
import numpy as np


FIELD_X,FIELD_Y=250,100
GROUND_X,GROUND_Y=50,0
GROUND_W,GROUND_H=200,70
HOME_X,HOME_Y=GROUND_X,GROUND_Y+GROUND_H
HOME_W,HOME_H=(FIELD_X-GROUND_X)/2,FIELD_Y-GROUND_H
DOOR_X,DOOR_Y=(FIELD_X-HOME_X)/2,GROUND_H
HOSPITAL_X,HOSPITAL_Y=HOME_X+HOME_W,HOME_Y
HOSPITAL_W,HOSPITAL_H=(FIELD_X-GROUND_X)/2,FIELD_Y-GROUND_H
HOSPITAL_DOOR_X,HOSPITAL_DOOR_Y=(200,GROUND_H)
DURATION=0.02
u=4

tk=Tk()
tk.attributes('-topmost',True)
canvas=Canvas(tk,width=FIELD_X*u, height=FIELD_Y*u)
canvas.pack()

class Person:
    def __init__(self,x=10,y=10,dx=1,dy=1,w=1,h=1,play_outside=0,gohome=False,gohospital=False,athome=False,athospital=False,time_to_out=0,virus="Health",latency=0,world=None,color='green'):
        self.x,self.y=x,y
        self.dx,self.dy=dx,dy
        self.w,self.h=w,h
        self.play_outside=play_outside
        self.gohome = gohome
        self.gohospital=gohospital
        self.athome=athome
        self.athospital = athospital
        self.time_to_out=time_to_out
        self.virus=virus
        self.latency=latency
        self.world=world
        self.id=canvas.create_rectangle(self.x*u, self.y*u, (self.x + self.w)*u, (self.y + self.h)*u,
                                        outline=color,fill=color)

    def __str__(self):
        return f'({self.x},{self.y})'

    def redraw(self):
        canvas.coords(self.id, self.x*u, self.y*u,
                      (self.x + self.w)*u, (self.y + self.h)*u)

    def check_wall(self):
        if self.x + self.w > GROUND_X+GROUND_W-1 or self.x < GROUND_X+1:
            self.dx = -self.dx
        if self.y + self.h > GROUND_Y+GROUND_H or self.y < GROUND_Y+1:
            self.dy = -self.dy

    def virus_state(self):
        if self.virus=="Carry":
            c = "orange"
            canvas.itemconfigure(self.id, fill=c)
            canvas.itemconfigure(self.id, outline=c)
        if self.virus=="Carry" and self.latency==50:
            self.virus="Sick"
            c = "red"
            canvas.itemconfigure(self.id, fill=c)
            canvas.itemconfigure(self.id, outline=c)
        if self.virus=="Recover":
            c = "blue"
            canvas.itemconfigure(self.id, fill=c)
            canvas.itemconfigure(self.id, outline=c)

    def exploring(self):
        self.change_dir(-1,0.1)

    def change_dir(self, r0, p):
        self.dirs = [(1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0)]
        ind = self.dirs.index((self.dx, self.dy))
        r = random.uniform(r0, 1)
        newInd = (ind + int(np.sign(r))) % 8 if abs(r) < p else ind
        self.dx, self.dy = self.dirs[newInd]

    def go_back_home_state(self):
        if self.play_outside>=100:
            self.gohome=True
            self.time_to_out=0
        if self.gohome==True and (self.x,self.y)==(DOOR_X,DOOR_Y):
            self.play_outside=0
            self.gohome=False
            self.athome=True

    def go_out_state(self,y1):
        if self.y<y1:
            self.athome = False
        if self.time_to_out>=20:
            self.athome = False
            self.time_to_out=0
            self.dy=-1

    def stay(self):
        self.dx=0
        self.dy=0

    def go_back(self,x1,y1):
        x2,y2=(self.x,self.y)
        if x1-x2<0:
            self.dx=-1
        elif x1-x2==0:
            self.dx=0
        else:
            self.dx=1

        if y1-y2<0:
            self.dy=-1
        elif y1-y2==0:
            self.dy=0
        else:
            self.dy=1

    def search_virus(self):
        to_check=[(1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0)]
        if self.virus=="Health":
            for d in to_check:
                for n in range(3):
                    x=self.x+n*d[0]
                    y=self.y+n*d[1]
                    if self.world.check_virus(x,y):
                        self.virus="Carry"

    def go_to_hosipital_state(self):
        if self.virus=="Sick" and self.athospital==False and self.gohospital==False:
            self.gohome=False
            self.gohospital=True
        if self.gohospital==True and (self.x,self.y)==(HOSPITAL_DOOR_X,HOSPITAL_DOOR_Y):
            self.play_outside=0
            self.gohospital = False
            self.gohome=False
            self.athospital=True
        if self.virus == "Recover" and self.athospital == True:
            self.athospital=False
            self.gohospital=False

    def recover(self):
        self.gohospital = False
        r = random.uniform(-1, 1)
        if abs(r) < 0.1:
            self.virus="Recover"
            self.athospital = False
            self.dy=-1

class HybridPeople(Person):
    def move(self):
        if self.gohome==False and self.play_outside<=100 and self.athome==False and self.gohospital==False:
            self.exploring()
            self.play_outside+=1
        elif self.athome==True and self.gohome==False:
            self.stay()
            self.time_to_out+=1
        elif self.athospital==True and self.virus=="Sick":
            self.stay()
        elif self.athome==False and self.gohome==True and self.gohospital==False:
            self.go_back(DOOR_X,DOOR_Y)
        elif self.athospital==False and self.gohospital==True and self.virus=="Sick":
            self.go_back(HOSPITAL_DOOR_X,HOSPITAL_DOOR_Y)
        else:
            print("what")
            self.exploring()
        if self.virus=="Carry":
            self.latency+=1
        self.x += self.dx
        self.y += self.dy


class Home:
    def __init__(self,x=HOME_X,y=HOME_Y,w=HOME_W,h=HOME_H,world=None,color='pink'):
        self.x,self.y=x,y
        self.w,self.h=w,h
        self.world=world
        self.id=canvas.create_rectangle(self.x*u, self.y*u, (self.x + self.w)*u, (self.y + self.h)*u,outline=color,fill=color)

class Hospital:
    def __init__(self,x=HOSPITAL_X,y=HOSPITAL_Y,w=HOSPITAL_W,h=HOSPITAL_H,world=None,color='deepskyblue'):
        self.x,self.y=x,y
        self.w,self.h=w,h
        self.world=world
        self.id=canvas.create_rectangle(self.x*u, self.y*u, (self.x + self.w)*u, (self.y + self.h)*u,outline=color,fill=color)

class Tag:
    def __init__(self,id=None,state=''):
        self.id=id
        self.state=state

@dataclass
class World:
    people:list=field(default_factory=list)
    home: Home = None
    hospital: Hospital=None
    tag_health: Tag=None
    tag_carry: Tag=None
    tag_sick: Tag=None
    tag_recover: Tag = None
    health: int=0
    carry: int=0
    sick: int=0
    recover: int = 0

    def draw_wall(self,x,y,w,h,u):
        canvas.create_rectangle(x * u, y * u, (x + w) * u, (y + h) * u)

    def set_people(self,n,x,y):
        for a in range(n):
            r = random.randint(-50, 50)
            p=HybridPeople(x=x+r,y=y,world=self)
            self.people.append(p)

    def set_sick_people(self,n,x,y):
        for a in range(n):
            p=HybridPeople(x=x,y=y,virus="Carry",world=self,color='red')
            self.people.append(p)

    def set_home(self):
        self.home=Home()
        canvas.create_text(100*u, 85*u, text="Home", font=('FixedSys', 2))

    def set_hospital(self):
        self.hospital=Hospital()
        canvas.create_text(200 * u, 85 * u, text="Hospital", font=('FixedSys', 2))

    def count_people(self):
        self.sick =0
        self.health=0
        self.carry=0
        self.recover=0
        for p in self.people:
            if p.virus=="Sick":
                self.sick+=1
            elif p.virus=="Carry":
                self.carry+=1
            elif p.virus=="Health":
                self.health+=1
            else:
                self.recover+=1

    def set_four_tag(self):
        self.tag_health=self.which_tag("Health",self.health,100,50)
        self.tag_carry = self.which_tag("Carry", self.carry, 100, 70)
        self.tag_sick = self.which_tag("Sick", self.sick, 100, 90)
        self.tag_recover = self.which_tag("Recover", self.recover, 100, 110)
        tk.update()

    def which_tag(self,state,n,x,y):
        id = canvas.create_text(x, y, text=f"{state}の人は:{n}", font=('FixedSys', 2))
        return Tag(id,state)

    def delete_tag(self):
        canvas.delete(self.tag_health.id)
        canvas.delete(self.tag_carry.id)
        canvas.delete(self.tag_sick.id)
        canvas.delete(self.tag_recover.id)
        tk.update()

    def animation_step(self,people):
        for h in people:
            h.go_back_home_state()
            h.go_to_hosipital_state()
            h.go_out_state(DOOR_Y)
            h.move()
            h.redraw()
            tk.update()
            h.virus_state()
            if h.athome==False and h.athospital==False:
                h.search_virus()
            if h.athome==False and h.gohome==False:
                h.check_wall()
            if h.athospital==True:
                h.recover()
        self.count_people()
        self.delete_tag()
        self.set_four_tag()
        tk.update()
        time.sleep(DURATION)

    def step(self):
        self.animation_step(self.people)

    def start(self,n_steps):
        self.set_people(50,200,50)
        self.set_sick_people(2, 200, 50)
        self.sick = 0
        self.health = 0
        self.set_four_tag()
        self.draw_wall(GROUND_X,GROUND_Y,GROUND_W,GROUND_H,u)
        self.set_home()
        self.set_hospital()
        for x in range(n_steps):
            self.step()

    def check_virus(self,x,y):
        if self.check_different_list(x,y,self.people):
            return True
        return False

    def check_different_list(self,x,y,people):
        for p in people:
            if p.athome==False:
                if (p.x,p.y)==(x,y):
                    if p.virus=="Carry":
                        r = random.uniform(-1, 1)
                        if abs(r) < 0.1:
                            return True
                    elif p.virus=="Sick":
                        r = random.uniform(-1, 1)
                        if abs(r) < 0.2:
                            return True
        return False




World().start(1000)

tk.mainloop()
