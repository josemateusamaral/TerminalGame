import time
import os
import random
import sys
import keyboard
from threading import Thread

class Game:
    def __init__(self):
        self.teclas = []
        for i in range(128):
            try:
                if keyboard.is_pressed(str(chr(i))):
                    self.texto += str(chr(i))
                self.teclas.append(chr(i))
            except:
                pass
        self.startGame()
        Thread(target=self.loop).start()
        Thread(target=self.setKey).start()

    def startGame(self):
        self.gameOver = False
        self.score = 0
        self.playerWidth = 5
        self.keepLoop = True
        self.tx = 60
        self.ty = 44
        self.speeds = [-3,-2,-1,1,2,3]
        self.psx = range(3,self.tx - 3)
        self.psy = range(3,self.ty - 3)
        self.objs = []
        self.points = []
        for i in range(40):
            self.addPoint(self.points)
        self.pause = False

        self.player = {'px':self.tx / 2,'py':self.ty-4}

        quantidade = int(len(sys.argv))
        if quantidade == 1:
            quantidade = 1
            
        for i in range(quantidade):
            self.addObj(self.objs) 
    
    def coll(self,objs,obj):
        for index,objectColl in enumerate(self.objs):
            if index == obj['id']:
                continue
            if ( objectColl['px'] == obj['px'] ) and ( objectColl['py'] == obj['py'] ):
                return index
        return -1

    def addObj(self,objs):
        obj = {'px':random.choice(self.psx),'py':random.choice(self.psy),'fx':random.choice(self.speeds),'fy':random.choice(self.speeds),'id':len(self.objs)}
        objs.append(obj)
        return objs

    def addPoint(self,points):
        pys = range(int(self.ty/2))
        obj = {'px':random.choice(self.psx),'py':random.choice(pys) + 2}
        points.append(obj)
        return points

    def keys(self):
        pressed = []
        for i in self.teclas:
            if i.lower() in pressed or i.upper() in pressed:
                continue
            if keyboard.is_pressed(i):
                pressed.append(i)
                if i == 'O':
                    sys.exit()
                elif i == 'A':
                    self.player['px'] -= 2
                elif i == 'D':
                    self.player['px'] += 2
                elif i == 'P':
                    if self.pause:
                        self.pause = False
                    else:
                        self.pause = True
                elif i == 'R':
                    self.startGame()
        
    def loop(self):
        print('iniciando loop')
        
        while self.keepLoop:
            self.keys()
            os.system('cls')
            if not self.pause and not self.gameOver:

                if self.player['px'] < 1:
                    self.player['px'] = 1
                if self.player['px'] > self.tx - (self.playerWidth + 1):
                    self.player['px'] = self.tx - (self.playerWidth + 1)
            
                #UPDATE PHISYCS
                
                checks = []
                for index,obj in enumerate(self.objs):
                    out = -1
                    obj['px'] += obj['fx']
                    if index not in checks:
                        collX = self.coll(objs=self.objs,obj=obj)
                        if collX != -1:
                            out = collX
                            self.objs[collX]['fx'] *= -1
                            obj['fx'] *= -1
                            out = True
                        for cada in  self.points:
                            if cada['px'] == obj['px'] and cada['py'] == obj['py']:
                                obj['fx'] *= -1
                                self.points.remove(cada)
                                self.score += 1
                                
                    obj['py'] += obj['fy']
                    if index not in checks:
                        collY = self.coll(objs=self.objs,obj=obj)
                        if collY != -1:
                            out = collX
                            self.objs[collY]['fy'] *= -1
                            obj['fy'] *= -1
                        for yf in range(obj['fy']):
                            for i in range(self.playerWidth):
                                if obj['px'] == (self.player['px'] + i) and ( obj['py'] + yf ) == self.player['py']:
                                    obj['fy'] *= -1
                        for cada in  self.points:
                            if cada['px'] == obj['px'] and cada['py'] == obj['py']:
                                obj['fy'] *= -1
                                self.points.remove(cada)
                                self.score += 1
                                
                    if out != -1:
                        checks.append(out)
                        checks.append(index)
                    if obj['px'] > self.tx - 3 or obj['px'] < 2:
                        obj['fx'] *= -1
                    if obj['py'] > self.ty - 3:
                        self.gameOver = True
                    if obj['py'] < 2:
                        obj['fy'] *= -1
                


                #RENDER GAME
                for y in range(self.ty):
                    for x in range(self.tx):
                        for i in range(self.playerWidth):
                            if y == self.player['py'] and x == ( self.player['px'] + i ):
                                print('O',end='')
                                break
                        else:
                            ocupado = False
                            for obj in self.objs:
                                if y == obj['py'] and x == obj['px']:
                                    print('@',end='')
                                    ocupado = True
                            for obj in self.points:
                                if y == obj['py'] and x == obj['px']:
                                    print('+',end='')
                                    ocupado = True
                            if not ocupado:
                                if ( y == 0 ) or ( x == 0 ) or ( y == (self.ty - 1) ) or ( x == (self.tx - 1)):
                                    print('#',end='')
                                else:
                                    print(' ',end='')
                    print()

            if self.gameOver:
                print('\nGAME OVER')
                print('\n\nSCORE:',self.score)
                print('\n[O] exit\n[R] play again')
            else:
                print('\n\nSCORE:',self.score)
                print('\n[O] exit\n[A] left\n[D] right\n[P] pause\n[R] restart')
            time.sleep(1/8)
Game()
