# 'Fly up' game
#
# [A] [B] to move
# "face down" to quit

import math, random

import microbit as M
import time, audio, music


ICON = M.Image("00000:80808:00000:00400:00900")  # used by shell on choosing an app


#------------------------------------------------------

def split_coord(x):
    "2.7 -> ((2, 0.3), (3, 0.7))"
    F = math.floor(x)
    C = math.ceil(x)
    if F == C:
        return ((F, 1.0),)
    else:
        k = x - F  # (0..1)
        return ((F, 1-k), (C, k))


#------------------------------------------------------
# generated by _generate_next_wall_indices.py

_wall_nexts = (
 ((0,), (1,2,4,8,16), (6,9,10,12,17,18), (3,5,14,20,21,24), (11,13,19,22,25,26,27), (7,28), (23,29), (15,30), (), ()),
 ((0,), (1,2,4), (5,6,8,9,16), (3,10,12,13,17,18,19,20), (7,11,14,21,22,24,25), (23,26,27), (15,28,29), (30,), (), ()),
 ((0,), (1,2,4,8), (5,6,9,10,16,17), (3,12,13,14,18,19,20,21,24), (11,22,25), (7,23,26,27,28), (15,29), (30,), (), ()),
 ((), (0,1), (2,3,4,5,8), (6,9,10,11,16,17), (7,12,13,14,18,19,20,21,23,24), (22,25), (15,26,27,28), (29,), (30,), ()),
 ((0,), (1,2,4,8,16), (6,9,10,12,17,18), (3,5,14,20,21,24), (11,13,19,22,25,26,27), (7,28), (23,29), (15,30), (), ()),
 ((0,), (1,2), (3,4,5,6,8,9,16), (10,12,13,17,18,19), (7,11,14,20,21,24), (22,23,25,26,27), (15,28,29), (), (30,), ()),
 ((0,), (1,2,4,8), (5,6,9,10,16,17), (3,12,13,18,19,20), (11,14,21,22,24,25), (7,23,26,27,28), (15,29), (30,), (), ()),
 ((), (0,), (1,2), (3,4,5,6,7,8,9,16), (10,11,12,13,17,18,19), (14,15,20,21,23,24), (22,25,26,27), (28,29), (), (30,)),
 ((0,), (2,4,8,16), (1,10,12,17,18,20), (3,5,6,9,14,21,22,24,25), (13,19,26), (7,11,27,28,29), (23,30), (15,), (), ()),
 ((0,), (1,2,4,8), (5,6,9,10,16,17), (3,12,13,18,19,20), (11,14,21,22,24,25), (7,23,26,27,28), (15,29), (30,), (), ()),
 ((0,), (1,2,4,8,16), (6,9,10,12,17,18), (3,5,14,20,21,24), (11,13,19,22,25,26,27), (7,28), (23,29), (15,30), (), ()),
 ((), (0,1), (2,3,4,5,8), (6,9,10,11,16,17), (7,12,13,14,18,19,20,21,23,24), (22,25), (15,26,27,28), (29,), (30,), ()),
 ((0,), (2,4,8,16), (1,10,12,17,18,20), (5,6,9,22,24,25), (3,13,14,19,21,26), (7,11,27,28,29), (23,30), (15,), (), ()),
 ((0,), (1,2,4), (5,6,8,9,16), (3,10,12,13,17,18,19,20), (7,11,14,21,22,24,25), (23,26,27), (15,28,29), (30,), (), ()),
 ((0,), (1,2,4,8,16), (6,9,10,12,17,18), (3,5,14,20,21,24), (11,13,19,22,25,26,27), (7,28), (23,29), (15,30), (), ()),
 ((), (), (0,), (1,2,3,4,8), (5,6,7,9,10,11,15,16,17), (12,13,18,19,20), (14,21,22,23,24,25), (26,27,28), (29,), (30,)),
 ((0,), (4,8,16), (1,2,12,18,20), (5,6,9,10,17,22,24,25), (3,13,14,19,21,26,28), (11,27,29), (7,23,30), (15,), (), ()),
 ((0,), (1,2,4,8,16), (6,9,10,12,17,18), (3,5,14,20,21,24), (11,13,19,22,25,26,27), (7,28), (23,29), (15,30), (), ()),
 ((0,), (2,4,8,16), (1,10,12,17,18,20), (5,6,9,22,24,25), (3,13,14,19,21,26), (7,11,27,28,29), (23,30), (15,), (), ()),
 ((0,), (1,2,4), (5,6,8,9,16), (3,10,12,13,17,18,19,20), (7,11,14,21,22,24,25), (23,26,27), (15,28,29), (30,), (), ()),
 ((0,), (8,16), (1,2,4,12,18,20,24), (6,9,10,17,22,25), (3,5,14,21,26,28), (11,13,19,27,29), (7,23,30), (), (15,), ()),
 ((0,), (1,2,4,8,16), (6,9,10,12,17,18), (3,5,14,20,21,24), (11,13,19,22,25,26,27), (7,28), (23,29), (15,30), (), ()),
 ((0,), (4,8,16), (1,2,12,18,20), (5,6,9,10,17,22,24,25), (3,13,14,19,21,26,28), (11,27,29), (7,23,30), (15,), (), ()),
 ((), (0,1), (2,3,4,5,8), (6,9,10,11,16,17), (7,12,13,14,18,19,20,21,23,24), (22,25), (15,26,27,28), (29,), (30,), ()),
 ((), (0,16), (2,4,8,20,24), (1,10,12,17,18,26), (3,5,6,9,14,21,22,25,28,29), (13,19), (7,11,27,30), (23,), (15,), ()),
 ((0,), (4,8,16), (1,2,12,18,20), (5,6,9,10,17,22,24,25), (3,13,14,19,21,26,28), (11,27,29), (7,23,30), (15,), (), ()),
 ((), (0,16), (2,4,8,20,24), (1,10,12,17,18,26), (3,5,6,9,14,21,22,25,28,29), (13,19), (7,11,27,30), (23,), (15,), ()),
 ((0,), (1,2,4,8,16), (6,9,10,12,17,18), (3,5,14,20,21,24), (11,13,19,22,25,26,27), (7,28), (23,29), (15,30), (), ()),
 ((), (0,), (8,16), (1,2,4,12,18,20,24,28), (6,9,10,17,22,25,26), (3,5,14,21,29,30), (11,13,19,27), (7,23), (), (15,)),
 ((), (0,16), (2,4,8,20,24), (1,10,12,17,18,26), (3,5,6,9,14,21,22,25,28,29), (13,19), (7,11,27,30), (23,), (15,), ()),
 ((), (), (0,), (2,4,8,16,24), (1,10,12,17,18,20,26,28,30), (5,6,9,22,25), (3,13,14,19,21,29), (7,11,27), (23,), (15,)),
)

def wall_index_to_tuple(i):
    t = ()
    for _ in range(5):
        t = (i & 1,) + t
        i >>= 1
    return t

def get_next_wall(prevWallIndex, complexity):
    variants = []  # list of pairs (wall index, complexity)
    for c,k in zip(range(complexity-2, complexity+3), (1,1,5,1,1)):
        if 0 <= c and c < 10:
            variants += [(i,c) for i in _wall_nexts[prevWallIndex][c]] * k
    #print(prevWallIndex, complexity, "variants", variants)
    return random.choice(variants)

#------------------------------------------------------

class Sound:
    Counter          = 1
    Start            = 2
    NextComplexity   = 3
    Crash            = 4
    Finish           = 5

def start_sound(Id, arg=0):
    if Id == Sound.Counter:
        music.pitch(880, duration=100, wait=False)
    elif Id == Sound.Start:
        audio.play(M.Sound.GIGGLE, wait=False)
    elif Id == Sound.NextComplexity:
        n = ['a5','b5','c6','d6','e6','f6','g6','a6','b6','c7'][arg]
        music.play(n, wait=False)
    elif Id == Sound.Crash:
        audio.play(M.Sound.SLIDE, wait=False)
    elif Id == Sound.Finish:
        music.play(music.POWER_UP, wait=False)
    

#------------------------------------------------------

class Wall:
    def __init__(self, y, wallIndex):
        self.y = y
        self.wallIndex = wallIndex
        self.wallTuple = wall_index_to_tuple(wallIndex)


class Level:
    def __init__(self):
        self.phase = 0  # 0 starting; 1 flying; 2 crash; 3 score; 4 farewell
        self.buffer = bytearray(25)  # last frame image buffer

        self.speed = 2.5  # px/sec
        
        self.reset_level()

    
    def reset_level(self):
        "called before (re)starting the level"

        # starting vars
        self.flying_start_time = 0  # also the time to finish countdown; 0 if countdown is not started
        self.countdown_number = 0  # 3,2,1
        
        # flying vars
        self.complexity = 0  # [0..9]
        self.ship_pos = 2  # horizontal position
        self.walls = []
        self.add_walls()

        # crash vars
        self.crash_start_time = 0  # 0 if not started
        self.crash_radius = 0  # int

        # score vars
        self.score = 0

        # finish vars
        self.farewell_start_time = 0
        self.farewell_radius = 0
        
    
    def add_walls(self):
        "add next walls according to self.complexity"
        
        lastY = 0.0
        lastIndex = 0
        if self.walls:
            w = self.walls[-1]
            lastY, lastIndex = w.y, w.wallIndex
            
        while lastY < 6:
            newIndex, complexity = get_next_wall(lastIndex, self.complexity)
            newY = lastY + 4 + (complexity - self.complexity) * 0.7  # !!! float here?
            
            self.walls.append(Wall(newY, newIndex))
            
            lastY = newY
            lastIndex = newIndex


    def hitting_wall(self):
        for w in self.walls:
            if 0 <= w.y:
                if w.y <= 1:
                    if w.wallTuple[self.ship_pos] == 1:
                        return True  # hit
                else:  # skip the walls above
                    break
        return False
        

    #------------------------------------------------
    # Drawing
    
    def draw_walls(self, buffer):
        for w in self.walls:
            for Y,k in split_coord(w.y):
                if 0 <= Y and Y < 5:
                    p = (4-Y)*5  # line pointer; flip y
                    c = int(k * 9)  # "color"
                    for j,b in enumerate(w.wallTuple):
                        if b:
                            buffer[int(p+j)] = c
    
    def draw_ship(self, buffer):
        j = self.ship_pos
        buffer[15 + j] = 4  # head
        buffer[20 + j] = 9  # body

    def draw_crash(self, buffer):
        "draw the crash according to increased self.crash_radius"
        for i,p in enumerate((20,15,10,5,0)):
            for j in range(5):
                a = i + abs(self.ship_pos - j)  # absolute value
                if a < self.crash_radius:
                    #buffer[p + j] = 0
                    buffer[p + j] = random.randint(0, 7)
                elif a == self.crash_radius:
                    buffer[p + j] = 9

    def draw_farewell(self, buffer):
        for i,p in enumerate((20,15,10,5,0)):
            for j in range(5):
                a = i + abs(self.ship_pos - j)  # absolute value
                if a <= self.farewell_radius:
                    b = self.farewell_radius - a
                    buffer[p + j] = (0, 3, 6, 9)[b % 4]
        self.draw_ship(buffer)

    #------------------------------------------------
    
    def handle_frame(self, timeMs, deltaMs, stepAside):
    
        image = None  # returning image, stays None if no redrawing needed
        redraw = False

        #-------------------------------------
        # handle the time
        
        if self.phase == 0:  # starting
            if self.flying_start_time == 0:  # start countdown
                self.flying_start_time = timeMs + 3000
                self.countdown_number = 3
                redraw = True
                start_sound(Sound.Counter)
            elif timeMs < self.flying_start_time:
                number = 1 + int(self.flying_start_time - timeMs) // 1000
                if self.countdown_number != number:
                    self.countdown_number = number
                    redraw = True
                    start_sound(Sound.Counter)
            else:  # finished - start flying
                self.flying_start_time = timeMs  # calibrate the start time
                self.phase = 1  # start flying
                start_sound(Sound.Start)
        
        elif self.phase == 1:  # flying            
            # handle complexity
            complexity = int(timeMs - self.flying_start_time) // 10000
            finishing = complexity > 9
            #finishing = True  #!!! temp
            if not finishing and self.complexity != complexity:
                self.complexity = complexity
                start_sound(Sound.NextComplexity, self.complexity)
        
            # move walls
            deltaY = self.speed * deltaMs / 1000
            for w in self.walls:
                w.y -= deltaY
            
            # remove passed walls
            self.walls = [w for w in self.walls if w.y > -1]
    
            # add new random walls
            if not finishing:
                self.add_walls()
            elif not self.walls:  # no more walls - finish
                #self.win = True
                self.phase = 4
        
        elif self.phase == 2:  # crash
            if self.crash_start_time == 0:  # explosion not yet started
                self.crash_start_time = timeMs
            radius = 1 + int(timeMs - self.crash_start_time) // 50
            if radius >= 10:  # stop the explosion
                self.phase = 3  # start showing score
            elif self.crash_radius != radius:
                self.crash_radius = radius
                redraw = True

        elif self.phase == 3:  # score
            M.display.scroll("%d%%" % self.score)  # !!! async
            # restart the level
            self.reset_level()
            self.phase = 0

        elif self.phase == 4:  # finish
            if self.farewell_start_time == 0:  # farewell not started
                self.farewell_start_time = timeMs
                start_sound(Sound.Finish)
            radius = 1 + int(timeMs - self.farewell_start_time) // 100
            if radius >= 100:  # stop the farewell - restart the level
                self.reset_level()
                self.speed += 0.5  # increase the speed
                self.phase = 0
            elif self.farewell_radius != radius:
                self.farewell_radius = radius
                redraw = True

        
        #-------------------------------------
        # handle buttons
        
        if self.phase == 1 or self.phase == 4:  # flying or farewell
            if stepAside:
                self.ship_pos += stepAside
                if 0:
                    self.ship_pos %= 5
                else:
                    if self.ship_pos < 0:
                        self.ship_pos = 0
                    if self.ship_pos > 4:
                        self.ship_pos = 4

                        
        #-------------------------------------
        # draw
        
        if self.phase == 0:  # starting - countdown
            if redraw:
                self.buffer = bytearray(25)
                for j in [4,2,0][:self.countdown_number]:
                    self.buffer[5 + j] = 8
                self.draw_ship(self.buffer)
                image = M.Image(5,5, self.buffer)

        elif self.phase == 1:  # flying - always redraw
            self.buffer = bytearray(25)
            self.draw_walls(self.buffer)
            self.draw_ship(self.buffer)
            image = M.Image(5,5, self.buffer)
    
        elif self.phase == 2:  # crash
            if redraw:
                self.draw_crash(self.buffer)
                image = M.Image(5,5, self.buffer)

        elif self.phase == 4:  # farewell
            if redraw:
                self.draw_farewell(self.buffer)
                image = M.Image(5,5, self.buffer)

        #-------------------------------------
        # additional handling
        
        if self.phase == 1:  # flying
            # check the crash here - just before the delay
            if self.hitting_wall():
                start_sound(Sound.Crash)
                self.win = False
                self.score = (timeMs - self.flying_start_time) // 1000  # in sec
                self.phase = 2  # start the crash animation


        return image


#------------------------------------------------------

def main():
    
    level = Level()
    
    last_time = 0
    
    while True:

        # allow to quit
        if M.accelerometer.was_gesture('face down'):
            M.display.clear()
            music.play(music.POWER_DOWN)
            break
        
        timeMs = time.ticks_ms()
        deltaMs = timeMs - last_time
        last_time = timeMs
    
        stepAside = M.button_b.get_presses() - M.button_a.get_presses()  # ..,-1,0,1,..
        
        image = level.handle_frame(timeMs, deltaMs, stepAside)
        
        if image:
            M.display.show(image)
    
        # delay
        time.sleep_ms(50)


if __name__ == '__main__':
    main()