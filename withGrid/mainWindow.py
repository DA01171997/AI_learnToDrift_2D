from pyglet.gl import *
from pyglet.window import key
from pyglet.window import FPSDisplay
import math
from CarSprite import *
from Line import *
from Track import *
from Grid import *
WINDOWWIDTH=1280
WINDOWHEIGHT=720 
class MyWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super(MyWindow,self).__init__(*args, **kwargs)
        #this clear thing affect the background color
        #comment it out to get a black background
        glClearColor(1,1.0,1.0,1)
        self.fps_display = FPSDisplay(self)
        self.car = CarSprite()
        self.key_handler = key.KeyStateHandler()
        self.testTrack= Track([40,60,1200,600],[240,260,800,200])
        self.testGrid = Grid(40,60,1200,600,50)

    def on_draw(self):
        glClear(GL_COLOR_BUFFER_BIT)
        self.fps_display.draw()
        self.testGrid.draw()
        self.testTrack.draw()
        self.car.draw()

    def on_key_press(self, symbol,modifiers):
        if symbol == key.UP:
            #print('accelerate')
            print(self.car.goStraight())
            self.car.checkPoint()
        elif symbol == key.DOWN:
            #print('reverse')
            print(self.car.goReverse())
            self.car.checkPoint()
        elif symbol == key.LEFT:
            #print('turn left')
            print(self.car.turnLeft())
            self.car.checkPoint()
        elif symbol == key.RIGHT:
            #print('turn right')
            print(self.car.turnRight())
            self.car.checkPoint()
        elif symbol == key.ESCAPE:
            pyglet.app.exit()

    def update(self, dt):
        pass

if __name__ == "__main__":
    window = MyWindow(WINDOWWIDTH,WINDOWHEIGHT, "DRIFT AI", resizable=True, vsync =True)
    window.push_handlers(window.key_handler)
    pyglet.clock.schedule_interval(window.update,1/60.0)
    pyglet.app.run()