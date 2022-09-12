import pyglet
import math

window = pyglet.window.Window(width = 1000,height = 750)

label = pyglet.text.Label("Mukundan:Lilith",x = 0,y = window.height,anchor_x = 'left',anchor_y = 'top')

star_img = pyglet.image.load('star.png')
star_img.anchor_x = star_img.width//2
star_img.anchor_y = star_img.height//2

ship_img = pyglet.image.load('shippe.png')
ship_img.anchor_x = ship_img.width//2
ship_img.anchor_y = ship_img.height//2

missile_img = pyglet.image.load('missile2.png')
missile_img.anchor_x = missile_img.width//2
missile_img.anchor_y = missile_img.height//2 

def dist(x1,y1,x2,y2):
    return math.pow((x1-x2)**2 + (y1-y2)**2,0.5)

class thing(pyglet.sprite.Sprite):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.vx = 0
        self.vy = 0
        self.acc = 0
        self.omega = 0
        self.k = 0
        self.r2 = 0
        self.g = 0

    def check_bounds(self):
        if (self.y + self.width/2 <= 0) and self.vy < 0:
            self.y = window.height - 5

        #up
        if (self.y - self.width/2 >= window.height) and self.vy > 0:
            self.y = -self.height + 5

        #left
        if (self.x + self.width <= 0) and self.vx < 0:
            self.x = window.width - 5

        #right
        if (self.x >= window.width + self.width/2) and self.vx > 0:
            self.x = -self.width + 5
        
    def update(self,dt):

        self.r2 = math.pow(dist(self.x,self.y,window.width/2,window.height/2),2)#(self.x - window.width/2)**2 + (self.y - window.height/2)**2
        self.g = self.k/self.r2
        self.vx -= self.g*dt*(self.x - window.width/2)/(math.pow(self.r2,0.5))
        self.vy -= self.g*dt*(self.y - window.height/2)/(math.pow(self.r2,0.5))

        self.x += self.vx*dt
        self.y += self.vy*dt
        self.check_bounds()

class ship(thing):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.acc = 500
        self.omega = 180
        self.k = math.pow(10,5)
        self.fuel = 100
        self.life = 15
        self.n_missiles = 1000
        self.keyhandler = pyglet.window.key.KeyStateHandler()

    def shoot(self):
        global missiles
        if self.keyhandler[pyglet.window.key.SPACE] and self.n_missiles>=0:
            missiles.append(thing(missile_img,self.x + self.width/2,self.y + self.width/2))
            missiles[-1].vx = 500*math.cos(-self.rotation*math.pi/180)
            missiles[-1].vy = 500*math.sin(-self.rotation*math.pi/180)
            self.n_missiles -= 1

    def update_ship(self,dt):
        self.update(dt)

        self.shoot()
        
        if self.keyhandler[pyglet.window.key.UP] and self.fuel>=0 :
            self.vx += self.acc*dt*math.cos(-self.rotation*math.pi/180)
            self.vy += self.acc*dt*math.sin(-self.rotation*math.pi/180)
            self.fuel -= 1

        if self.keyhandler[pyglet.window.key.LEFT]:
            me.rotation -= self.omega*dt

        if self.keyhandler[pyglet.window.key.RIGHT]:
            me.rotation += me.omega*dt

class missile(thing):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
    
def collision(ship):
    global missiles
    i = 0
    while len(missiles) and i<=len(missiles)-1:
        if dist(missiles[i].x,missiles[i].y,ship.x,ship.y) < ship.height + missiles[i].height:
            ship.life -= 1
            del missiles[i]
        else:
            i += 1

me = ship(ship_img,750,750//4)
missiles = []

window.push_handlers(me.keyhandler)
dt = 1/60

def update(dt):
    global missiles

    collision(me)
    me.update_ship(dt)
    
    for i in missiles:
        i.update(dt)

pyglet.clock.schedule_interval(update,dt)

@window.event
def on_draw():
    global missiles
    window.clear()
    label.draw()
    star_img.blit(window.width//2,window.height//2)
    for i in missiles:
        i.draw()
    me.draw()
    l1 = pyglet.text.Label(str(me.fuel),x = window.width//3,y = window.height*99//100,anchor_x = 'left',anchor_y = 'top')
    l1.draw()
    l2 = pyglet.text.Label(str(me.life),x = 2*window.width//3,y = window.height*99//100,anchor_x = 'left',anchor_y = 'top')
    l2.draw()
    

pyglet.app.run()
