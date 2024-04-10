# 'Tilt' test.
# Two tilt-controlled points.
# "face down" to quit.

import math

import microbit as M
import time


ICON = M.Image("00000:00000:09030:00000:00000")  # used by shell on choosing an app

#-------------------------------------

class Point:
    def __init__(self, x,y, bright, speed):
        self.x = x
        self.y = y
        self.bright = bright
        self.speed = speed

_points = [
    Point(0,0, 1.0, 0.2),
    Point(0,0, 0.2, 4.0),
]

_last_time = 0  # ms

#-------------------------------------
# 5x5 matrix

def make_empty_matrix():
    return [[0]*5 for i in range(5)]

def add_to_matrix(mat, X,Y, bright, validate = False):
    mat[Y+2][X+2] += bright
    if validate:
        if   mat[Y+2][X+2] > 1.0: mat[Y+2][X+2] = 1.0
        elif mat[Y+2][X+2] < 0.0: mat[Y+2][X+2] = 0.0

def make_image(mat):
    buffer = bytearray(int(cell * 9) for row in mat for cell in row)
    return M.Image(5, 5, buffer)

def split_coord(x):
    F = math.floor(x)
    C = math.ceil(x)
    if F == C:
        return ((F, 1.0),)
    else:
        k = x - F  # (0..1)
        return ((F, 1-k), (C, k))
    
def draw_point(mat, x,y, bright = 1.0):
    # x, y: [-2..2]
    for X,kx in split_coord(x):
        for Y,ky in split_coord(y):
            add_to_matrix(mat, X,Y, bright * kx * ky, validate = True)

#-------------------------------------

def main():
    global _last_time
    
    while True:

        # allow to quit
        if M.accelerometer.was_gesture('face down'):
            break
    
        now = time.ticks_ms()
        mat = make_empty_matrix()
        
        if _last_time > 0:
            deltaMs = now - _last_time
            
            ax = M.accelerometer.get_x()
            ay = M.accelerometer.get_y()
            
            for point in _points:
                speed = 0.00001 * point.speed
                point.x += ax * deltaMs * speed
                point.y += ay * deltaMs * speed
                
                if   point.x >  2: point.x =  2
                elif point.x < -2: point.x = -2
                if   point.y >  2: point.y =  2
                elif point.y < -2: point.y = -2
                
                draw_point(mat, point.x, point.y, point.bright)
           
        _last_time = now
        
        
        im = make_image(mat)
        M.display.show(im)
        
        M.sleep(50)


if __name__ == '__main__':
    main()