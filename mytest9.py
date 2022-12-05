# 20150209
# v
# VP
####
# Control with arrow keys, when using full desktop 102-key keyboard
# For laptop keyboards,  controls: 'q' left, 'w' right, 'p' up, 'l' down
# Keys work for full keyboards also
# 20161214
# port to python 3
# VP
import tkinter as tk
from random import randint
from math import pi, cos, sin

def isclose(point, points):
    for p in points:
        if abs(p[0]-point[0])<30 and abs(p[1] - point[1])<30:
            return True
    return False

class Orbit():
    def __init__(self, bx, by):
        self.bx  = bx
        self.by  = by
        self.r = 100
        self.theta = 0
        self.direction = 1
        self.x, self.y = self.getpoint()
    def nextpos(self):
        self.oldx, self.oldy = self.x, self.y
        self.theta = self.theta + self.direction * pi/360 * 5
        self.x, self.y= self.getpoint()
        return  self.x - self.oldx, self.y - self.oldy
    def getpoint(self):
        return int(self.bx + self.r * cos(self.theta)), int(self.by + self.r * sin(self.theta))

class Score():
    def __init__(self):
        self.score = 0
    def get(self):
        return self.score
    def gotball(self):
        self.score = self.score + 100
    def hitsquare(self):
        self.score = self.score / 2
    def hittriangle(self):
        self.score = self.score * 2
    def report(self):
        print ("score: ", self.get())
        myscore.set('Score: '+str(self.get()))
    

def moveright(event):
    x = canvas.coords(bar)
    if x[0]<=490:
        canvas.move(bar, 10, 0)
def moveleft(event):
    x = canvas.coords(bar)
    if x[0]>=10:
         canvas.move(bar, -10, 0)
def moveup(event):
    x = canvas.coords(bar)
    if x[1]>=10:
        canvas.move(bar, 0, -10)
def movedown(event):
    x = canvas.coords(bar)
    if x[1]<=490:
        canvas.move(bar, 0, 10)
def kpressed(event):
    root.destroy()
    
class Terminate():
    def __init__(self, artlist):
        self.myitems = artlist
    def stop(self):
        for i in self.myitems:
            i.stop()
            
class Artifact():
    remaining = 0
    points = []
    def __init__(self, canvas):
        Artifact.remaining = Artifact.remaining + 1
        while True:
            point = [randint(0,500), randint(0,500)]
            if not isclose(point, Artifact.points): break
        Artifact.points.append(point)
        self.biasx, self.biasy = point
        self.direction1 = randint(-1,1)
        self.direction2 = randint(-1,1)
        self.canvas = canvas
        self.mycolor = "#"+("%06x"% randint(0,16**6-1))
        self.speed = 5*randint(5,15)
    def move(self, x):
        self.canvas.move(self.art, self.direction1*5,  self.direction2 * 5)
        coords= self.canvas.coords(self.art)
        if coords[1] > 500:
            self.direction2 = -1
        elif coords[1]<0:
            self.direction2 = 1
        elif coords[0]<0:
            self.direction1 = 1
        elif coords[0]>500:
            self.direction1 = -1
        t = self.canvas.find_overlapping(coords[0], coords[1], coords[2], coords[3])
        a = 1
        if len(t)>1:
            a= self.handlecollision(x, t)
        if a>0:
            root.after(self.speed, lambda: self.move(bar))
    def stop(self):
        self.direction1 = 0
        self.direction2 = 0
    
class Ball(Artifact):
    remaining = 0
    def __init__(self, canvas):
        Ball.remaining = Ball.remaining + 1
        Artifact.__init__(self,canvas)
        biasx = self.biasx
        biasy = self.biasy
        self.art = canvas.create_oval( biasx+10, biasy+20, biasx+30, biasy+40,
                                          outline='black',
                                          fill=self.mycolor)
    def handlecollision(self, x, t):
        self.direction1= -self.direction1
        self.direction2= -self.direction2
        if x in t:
            Ball.remaining = Ball.remaining - 1
            print ("Got a ball: remaining", Ball.remaining)
            score.gotball()
            score.report()
            self.canvas.delete(self.art)
            if Ball.remaining == 0:
                print ("DONE!")
                term.stop()
            return 0
        return 1

class Square(Artifact):
    remaining = 0
    def __init__(self, canvas):
        Square.remaining = Square.remaining + 1
        Artifact.__init__(self,canvas)
        biasx, biasy = self.biasx, self.biasy
        self.art = canvas.create_rectangle( biasx+10, biasy+20, biasx+30, biasy+40,
                                          outline='black',
                                          fill=self.mycolor)
    def handlecollision(self, x, t):
        self.direction1= -self.direction1
        self.direction2= -self.direction2
        if x in t:
            print ("You run into a square.")
            score.hitsquare()
            score.report()
        return 1


class Triangle(Artifact):
    def __init__(self, canvas):
        Artifact.__init__(self,canvas)
        biasx, biasy = self.biasx, self.biasy
        self.art = canvas.create_polygon( biasx+10, biasy+20,
                                          biasx+30,biasy+20,
                                          biasx+20, biasy,
                            fill = self.mycolor)
    def handlecollision(self, x, t):
        if x in t:
            print ("You got a triangle.")
            score.hittriangle()
            score.report()
            self.canvas.delete(self.art)
            return 0
        return 1
    

class Star(Artifact):
    def __init__(self, canvas):
        Artifact.__init__(self,canvas)
        self.biasx, self.biasy = 250,250
        self.orb = Orbit(self.biasx, self.biasy)
        biasx = self.biasx+ self.orb.nextpos()[0]
        biasy = self.biasy+ self.orb.nextpos()[1]
        print (biasx, biasy)
        self.art = canvas.create_polygon( biasx+10, biasy+20,
                                          biasx+30,biasy+20,
                                          biasx+20, biasy,
                            fill = self.mycolor)
    def handlecollision(self, x, t):
        self.orb.direction = -self.orb.direction
        if x in t:
            print ("You got a star.")
            score.hittriangle()
            score.report()
            self.canvas.delete(self.art)
            return 0
        return 1
    def move(self, x):
        self.canvas.move(self.art, self.orb.nextpos()[0],
                                                     self.orb.nextpos()[1])
        coords= self.canvas.coords(self.art)
        if coords[1] > 500:
            self.direction2 = -1
        elif coords[1]<0:
            self.direction2 = 1
        elif coords[0]<0:
            self.direction1 = 1
        elif coords[0]>500:
            self.direction1 = -1
        t = self.canvas.find_overlapping(coords[0], coords[1], coords[2], coords[3])
        a = 1
        if len(t)>1:
            a= self.handlecollision(x, t)
        if a>0:
            root.after(self.speed, lambda: self.move(bar))
    def stop(self):
        self.direction1 = 0
        self.direction2 = 0
    

root = tk.Tk()
canvas = tk.Canvas(root, width = 640, height = 640)

items = []
for i in range(10):
     items.append(Ball(canvas))

for i in range(10):
    items.append(Square(canvas))

items.append(Triangle(canvas))
items.append(Star(canvas))

term = Terminate(items)

score = Score()
myscore = tk.StringVar()
bar = canvas.create_rectangle(200, 480, 240, 500)
canvas.create_line(0,540,500,540)


for i in items:
        i.move(bar)

root.bind("k", kpressed)
root.bind('<Left>', moveleft)
root.bind('<Right>', moveright)
root.bind('<Up>', moveup)
root.bind('<Down>', movedown)
root.bind('q', moveleft)
root.bind('w', moveright)
root.bind('p', moveup)
root.bind('l', movedown)
canvas.pack()
tk.Label(root, textvariable = myscore, font = ("Times", 18)).pack()
root.mainloop()
