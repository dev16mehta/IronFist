from user304_rsf8mD0BOQ_1 import Vector

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

import random

class StartMenu:
    def __init__(self, game):
        self.game = game

    def draw(self, canvas):
        if not self.game.started:
            # Styling
            title_font_size = 40
            normal_font_size = 20
            title_color = "White"
            normal_color = "#FFD700"  # Gold color

            # Title
            canvas.draw_text("Iron Fist", (self.game.WIDTH / 2 - 100, 100), title_font_size, title_color)

            # Subtitle
            canvas.draw_text("Press Start to Begin", (self.game.WIDTH / 2 - 110, 150), normal_font_size, normal_color)

            # Controls
            controls_y = 250
            canvas.draw_text("Controls:", (self.game.WIDTH / 2 - 60, controls_y), normal_font_size, normal_color)
            controls = [
                "Jump: Up Arrow / W / Space",
                "Fastfall: Down Arrow / S",
                "Punch: Right Arrow / Left Arrow / A / D",
                "Avoid the enemies!"
            ]
            for i, control in enumerate(controls):
                canvas.draw_text(control, (self.game.WIDTH / 2 - 120, controls_y + (i + 1) * 30), normal_font_size, normal_color)

            # Start Button
            button_width = 100
            button_height = 40
            button_pos = (self.game.WIDTH / 2 - button_width / 2, self.game.HEIGHT - 200)
            canvas.draw_polygon([(button_pos[0], button_pos[1]),
                                 (button_pos[0] + button_width, button_pos[1]),
                                 (button_pos[0] + button_width, button_pos[1] + button_height),
                                 (button_pos[0], button_pos[1] + button_height)],
                                1, 'White', '#2C6A6A')  # White border, Dark Turquoise fill
            canvas.draw_text("Start", (button_pos[0] + 25, button_pos[1] + 30), 24, "White")





class Game:
    def __init__(self, width=500, height=500):
        self.WIDTH = width
        self.HEIGHT = height
        self.FLOOR = 0.95*self.HEIGHT
        self.GRAVITY = 0.5
        self.pos = Vector(self.WIDTH/2,self.HEIGHT/2)
        self.kbd = Keyboard(self)
        self.player = Player(self,Vector(self.WIDTH / 2, self.HEIGHT - 40), 25)
        self.background = Spritesheet(self,self,
                                     "https://www.cs.rhul.ac.uk/home/zmac436/cs1822/cyberpunk-street.png",
                                     1,1,Vector(self.WIDTH/2,self.HEIGHT/2),Vector(0,0),self.WIDTH,self.HEIGHT)
        self.enemies = set()

        self.inter = Interaction(self, self.player, self.enemies, self.kbd)

        self.frame = simplegui.create_frame('Iron Fist', self.WIDTH, self.HEIGHT)
        self.start_menu = StartMenu(self)  # Create StartMenu instance
        self.frame.set_draw_handler(self.start_menu.draw)  # Initial draw handler is the start menu
        self.frame.set_canvas_background('#2C6A6A')
        self.frame.set_keydown_handler(self.kbd.keyDown)
        self.frame.set_keyup_handler(self.kbd.keyUp)
        self.frame.add_button('Start', self.play)
        self.frame.set_mouseclick_handler(self.mouse_click)
        self.game_over_screen = False
        self.frame.set_mouseclick_handler(self.mouse_click)


        self.started = False
       
    def mouse_click(self, pos):
        if self.game_over_screen:
            # Check if the mouse click happened within the bounds of the "Play Again" button
            button_width = 130
            button_height = 40
            button_pos = (self.WIDTH / 2 - button_width / 2, self.HEIGHT / 2 + 50)
            if (button_pos[0] <= pos[0] <= button_pos[0] + button_width and
                    button_pos[1] <= pos[1] <= button_pos[1] + button_height):
                self.restart_game()  # Call the restart_game method if the "Play Again" button is clicked
        else:
            # Check if the mouse click happened within the bounds of the Start button
            button_width = 100
            button_height = 40
            button_pos = (self.WIDTH / 2 - button_width / 2, self.HEIGHT - 200)
            if (button_pos[0] <= pos[0] <= button_pos[0] + button_width and
                    button_pos[1] <= pos[1] <= button_pos[1] + button_height):
                self.play()  # Call the play method if the Start button is clicked
        
    def play(self):
        self.started = True
        self.inter.add_enemy_timer.start()
        self.frame.set_draw_handler(self.inter.draw)



        
class Spritesheet:
    def load(self,url,max_attempts):
        attempts = 0
        img = simplegui.load_image(url)
        while((img.get_width() == 0 or img.get_height() == 0) and attempts <= max_attempts):
            img = simplegui.load_image(url)
            attempts +=1
        
        if (attempts > max_attempts):
            return None
        return img
            
    def __init__(self,game,owner,url,rows,columns,pos,offset=Vector(0,0),width="default",height="default"):
        self.game = game
        self.owner = owner
        self.url = url
        self.source = self.load(url,100000)
        self.rows = rows
        self.columns = columns
        self.pos = pos
        self.offset = offset
        self.source_width = self.source.get_width()
        self.source_height = self.source.get_height()
        
        if width == "default":
            self.width = self.source_width
        else:
            self.width = width  
            
        if height == "default":
            self.height = self.source_height
        else:
            self.height = height

         
        
        self.frame_width = (self.source_width)/(self.columns)
        self.frame_height = (self.source_height)/(self.rows)
        self.frame_centerx = (self.frame_width)/2
        self.frame_centery = (self.frame_height)/2
        self.frame_index = [0,0]
        self.start_index = [0,0]
        self.end_index = [0,0]
   
    
    def update(self):
        self.pos = self.pos.add(self.owner.pos.copy().subtract(self.pos))
        
    def draw(self, canvas):
        self.update()
        source_center = (
            self.frame_width*self.frame_index[1] + self.frame_centerx, 
            self.frame_height*self.frame_index[0] + self.frame_centery)
        try:
            canvas.draw_image(
                self.source, 
                source_center , 
                (self.frame_width,self.frame_height), 
                (self.pos.x + self.offset.x, self.pos.y + self.offset.y), (self.width,self.height))
        except:
            canvas.draw_text("Could not draw object." ,(self.pos.x,self.pos.y),12,'Red','serif')
    
    def set_frame_index(self, frame):
        self.frame_index[0] = frame[0]
        self.frame_index[1] = frame[1]
        
    def next_frame(self):
        if self.frame_index == self.end_index:
            self.set_frame_index(self.start_index)
        else:
            self.frame_index[1] += 1
            if self.frame_index[1] >= self.columns:
                self.frame_index[1] = 0
                self.frame_index[0] += 1

            if self.frame_index[0] >= self.rows:
                self.frame_index[0] = 0
                self.frame_index[1] = 0
                
    def next_flipped_frame(self):
        if self.frame_index == self.end_index:
            self.set_frame_index(self.start_index)
        else:
            self.frame_index[1] -= 1
            if self.frame_index[1] < (self.columns/2):
                self.frame_index[1] = self.columns-1
                self.frame_index[0] -= 1

            if self.frame_index[0] < 0:
                self.frame_index[0] = self.rows-1
                self.frame_index[1] = self.columns-1

#abstract - do not instantiate
class Entity: 

    def __init__(self,game,pos,radius,sprite):
        self.game = game
        
        self.pos = pos
        self.x = pos.get_p()[0]
        self.y = pos.get_p()[1]
        
        self.direction = "left"
        self.vel = Vector()
        
        self.radius = radius
        self.lives = 3
        
        self.sprites = None
        
        self.hitbox = None
        self.hurtbox = Hurtbox(self,Vector(0,0),radius)
        self.state = "airborne"
        self.clocks = Clocks(self)
        self.iclocks = Clocks(self)
        
        self.invincible = False
        self.visible = True
        
    #Methods implemented by sublasses
    def attack_init(self):
        pass
    def attack(self):
        pass
    def attack_end(self):
        pass
    
    #Methods to help with some maths/physics
    def on_ground(self):
        return self.pos.y == self.game.FLOOR - self.radius
    
    def is_left_as_num(self):
        return 1 if self.direction == "left" else 0
    
    def adjust_num_for_direction(self,num):
        return num*(1-self.is_left_as_num()*2)
    
    #Methods to help with frames
    def state_initialise(self,frame_duration=1,timer=0,time=1,start_index=[0,0],end_index=[0,1]):
        self.clocks.frame_duration = frame_duration
        self.clocks.timer = timer
        self.clocks.time = time 
        self.sprites.start_index = start_index 
        self.sprites.end_index = end_index  
        self.sprites.set_frame_index(start_index)
        self.adjust_frame_for_direction(self.sprites.frame_index)
        self.adjust_frame_for_direction(self.sprites.start_index)
        self.adjust_frame_for_direction(self.sprites.end_index)
        
    def adjust_frame_for_direction(self,index):
        #if needed to change methods for efficiency, check if nothing needs to be done first rather than last.
        if index[1] < self.sprites.columns/2 and self.direction == "left": # if your sprites arent flipped yet your direction is left
            index[1] = self.sprites.columns - (index[1] + 1)
   
            
        elif index[1] >= self.sprites.columns/2 and self.direction == "right": # if your sprites arent flipped yet your direction is right
            index[1] = 0 + (self.sprites.columns - index[1]) - 1

    def advance_frame(self):
        if self.clocks.frame_timer == 0:
            if self.direction == "right":
                self.sprites.next_frame()
            else:
                self.sprites.next_flipped_frame()
     
    def direction_force(self, direction):
        self.direction = direction
        
    def hit(self):
        print("pow")
        self.score += 1
        
    def hurt(self):
        print("ow")
        
    def create_hitbox(self,owner,x,y,radius,time,hitlag): #params - owner(should nearly always be self), 
                                                       #x offset, y offset, (from centre of entity)
                                                       #radius 
                                                       #time to live (before hitbox is destroyed)
        owner.hitbox = Hitbox(owner,Vector(self.adjust_num_for_direction(x),y),radius,time,hitlag)
       
    def update(self):
        pass
            
    def draw(self, canvas):
        pass
        
    
class Player(Entity):
    def __init__(self, game, pos, radius):
        super().__init__(game, pos, radius, None)
        self.direction = "right"
        self.JUMP_STRENGTH = -14
        self.fastfalling = False
        self.hit_cancel = False
        self.flash_timer = None
        self.heat = 0
        self.jumps = 0
        self.double_jumping = False
        self.buffered_down = False
        self.attack_alternator = 0
        self.hurtbox = Hurtbox(self, Vector(-3, -15), radius)
        self.score = 0  # Initialize the score attribute

      
        self.sprites = Spritesheet(self, self,
                                   "https://www.cs.rhul.ac.uk/home/zmac627/cs1822/player.png",
                                   9, 20, self.pos.copy(), Vector(0, -38), 192.4, 130)
        self.sprites.frame_index = [1, 0]
        self.sprites.start_index = [1, 0]
        self.sprites.end_index = [1, 3]
    

    

    def idle_init(self):
        self.hitbox = None
        self.double_jumping = False
        self.hit_cancel = False
        self.attack_alternator = 0
        self.state = "idle"
        self.state_initialise(8,0,4,[1,0],[1,3])
 
    def jump(self):
        self.hitbox = None
        self.jumps = 1
        self.state = "airborne"
        self.vel.y = self.JUMP_STRENGTH
        self.state_initialise(8,0,4,[4,0],[4,3])
    
    def double_jump_init(self):
        self.state = "air_attack"
        self.double_jumping = True
        self.hitbox = None
        self.vel.y = self.JUMP_STRENGTH/1.75
        self.hit_cancel = False
        self.state_initialise(6,0,8,[5,0],[5,2])
    
    def double_jump(self):
        self.jumps = 2
        if self.clocks.timer == 1:
            self.create_hitbox(self, 10, -35, 30, 20,9)
        if self.clocks.timer >= self.clocks.time:
            self.double_jump_end()

    def double_jump_end(self):
        self.fastfall_check()
        self.state = "airborne"
        self.double_jumping = False
        self.clocks.timer = 0
        self.clocks.time =-1
        
    def fastfall(self):
        self.fastfalling = True
        self.vel.y = -(self.JUMP_STRENGTH * 2)

    def attack_init(self):
        self.state = "attack"      
        self.hitbox = None
        self.hit_cancel = False
        self.state_initialise(6,0,10,
                             [2,0] if self.attack_alternator == 0 else [3,0],
                             [2,2] if self.attack_alternator == 0 else [3,2])
   
    def air_attack_init(self):
        self.state = "air_attack"      
        self.hitbox = None
        self.hit_cancel = False
        self.state_initialise(2,0,17,[0,0],[0,4])
                          
    def attack(self):
        if self.clocks.timer == 1:
            self.create_hitbox(self, 50, -35, 20, 8,8)
        if self.clocks.timer >= self.clocks.time:
            self.attack_end()
    
    def air_attack(self):
        if self.clocks.timer == 4:
            self.create_hitbox(self, 47, 0, 20, 8,9)
        if self.clocks.timer >= self.clocks.time:
            self.air_attack_end()

    def attack_end(self):
        self.idle_init()  
        self.hit_cancel = False;
    
    def air_attack_end(self):
        self.fastfall_check()
        self.state = "airborne"
        self.clocks.timer = 0
        self.clocks.time =-1


    
    def fastfall_check(self):
        if self.buffered_down == True:
            self.buffered_down = False
            self.fastfall()
            
    def ground_check(self):
        if self.pos.y > self.game.FLOOR - self.radius:
            self.idle_init()
            self.jumps = 0
            self.pos.y = self.game.FLOOR - self.radius
            self.vel.y = 0
            self.fastfalling = False
    
    def hit(self):
        self.score += 1
        self.heat +=1
        if self.heat % 30 == 0:
            self.lives += 1
        
        if self.heat >= 30:
            self.score += self.heat - 30
        if self.heat >= 35:
            self.score += int(game.inter.elapsed_time/100000)
        self.hit_cancel = True
        self.attack_alternator = (self.attack_alternator + 1) % 2
        if self.state == "air_attack":
            self.vel.y = self.JUMP_STRENGTH/2.5
        
    def hurt_init(self, time):
        if self.lives > 0:  # Check if lives are greater than 0 before decreasing
            self.lives -= 1  # Decrease the number of lives
        self.double_jumping = False
        self.buffered_down = False
        self.hitbox = None
        self.state = "hurt"
        self.heat = 0
        self.state_initialise(1,0,time,[7,0],[7,1])
        self.attack_alternator = 0
        
    def hurt(self):
        if self.clocks.timer >= self.clocks.time:
            self.hurt_end()
    
    def hurt_end(self):
        if self.on_ground():
            self.idle_init()
        else:
            self.state = "airborne"
            self.clocks.timer = 0
            self.clocks.time =-1
            
        self.hit_cancel = False;
    
    def flash(self):
        if self.visible:
            self.visible = False
        else:
            self.visible = True
            
   
    def invincibility_end(self):
        self.invincible = False
        self.visible = True
        if self.flash_timer is not None:
            self.flash_timer.stop()
        self.flash_timer = None
        self.iclocks.timer = -1
        self.iclocks.time = 0


    def update(self):
       
        self.clocks.tick()
        self.pos.add(self.vel)
        
        if self.state == "idle":
            self.advance_frame()
            if self.clocks.timer >= self.clocks.time:
                self.clocks.timer = 0
        
        if self.state == "attack":
            self.attack()
            if self.sprites.frame_index != self.sprites.end_index:
                self.advance_frame()
        
        if self.state == "air_attack":
            self.vel.y += self.game.GRAVITY
            self.air_attack() if not self.double_jumping else self.double_jump()
            if self.sprites.frame_index != self.sprites.end_index:
                self.advance_frame()
                
        if self.state == "airborne":
            self.vel.y += self.game.GRAVITY
            if self.sprites.frame_index != self.sprites.end_index:
                self.advance_frame()
        
        if self.state == "hurt":
            self.vel = self.vel/2
            self.hurt()
            self.advance_frame
            
        
        if self.invincible:
            
            self.iclocks.tick()
            if (self.iclocks.timer <= self.iclocks.time/2 and
                self.iclocks.timer % (int(self.iclocks.time/20)) == 0):
                self.flash()
            elif (self.iclocks.timer > self.iclocks.time/2 and 
                  self.iclocks.timer % (int(self.iclocks.time/40)) == 0 ) :
                self.flash()
                
            if self.iclocks.timer >= self.iclocks.time:
                self.invincibility_end()
            
            
        self.ground_check()
        if self.hitbox is not None:
            self.hitbox.update()
        self.hurtbox.update()
  

    

    def draw(self, canvas):
        if self.visible:
            self.sprites.draw(canvas)
            if self.hitbox is not None:
                self.hitbox.draw(canvas)
            self.hurtbox.draw(canvas)


class Ghost(Entity):
    def __init__(self,game, pos, radius):
        super().__init__(game,pos,radius,None)
        self.state = "air_attack"
        self.alive = True  # Add a variable to track if the ghost is alive or dead
        self.create_hitbox(self,0,0,radius/2,float("inf"),15)
        self.accelerator = Vector(0,0) #Adds speed to the current vector
        self.accel = Vector(0.04,0)
        self.max_accel_vel = Vector(7.5,0)
        
        self.sprites = Spritesheet(self, self,
                                   "https://www.cs.rhul.ac.uk/home/zmac627/cs1822/ghosts.png",
                                   3, 18, self.pos.copy(), Vector(0, -20),
                                   100, 100)
        self.sprites.frame_index = [1, 0]
        self.sprites.start_index = [1, 0]
        self.sprites.end_index = [1, 5]
        
    def load_init(self):
        self.attack_init()
        
    def attack_init(self):
        self.state = "air_attack"
        self.state_initialise(8,0,6,[1,0],[1,5])

    def update(self, target):
        self.clocks.tick()
        
        if self.alive:
            self.accelerator.add(self.accel)
            self.accelerator.x = min(self.accelerator.x,self.max_accel_vel.x)
            # Calculate the vector pointing from the enemy to the target (player)
            direction = target.hurtbox.pos - self.pos
            direction.normalize()  # normalize the vector to get a unit vector
            self.vel = direction * (2+self.accelerator.x)
            self.pos.add(self.vel)

            if (self.pos.x < 0 or self.pos.x > self.game.WIDTH or
                self.pos.y < 0 or self.pos.y > self.game.HEIGHT):
                self.reset()

            self.hitbox.update()
            self.hurtbox.update()
            
        if self.state == "air_attack":
            self.advance_frame()
            if (self.clocks.timer >= self.clocks.time):
                self.clocks.timer = 0

    def draw(self, canvas):
        if self.alive:  # Only draw the ghost if it's alive
            self.hitbox.draw(canvas)
            self.hurtbox.draw(canvas)
            self.sprites.draw(canvas)
            
    def hit(self):
        self.reset()
    
    def hurt(self):
        self.die()
        
    def reset(self):
        if random.choice([True, False]):  # choose left or right side randomly
            self.pos = Vector(0, random.uniform(0,self.game.FLOOR - 40))  
            self.vel = Vector(random.uniform(1, 4), 0)
            self.accelerator = Vector()
            self.hitbox.pos = self.pos.copy()
            self.hurtbox.pos = self.pos.copy()
            self.direction_force("right")
            self.attack_init()
        else:
            self.pos = Vector(self.game.WIDTH, random.uniform(0,self.game.FLOOR - 40)) 
            self.vel = Vector(random.uniform(-4, -1), 0)
            self.accelerator = Vector()
            self.hitbox.pos = self.pos.copy()
            self.hurtbox.pos = self.pos.copy()
            self.direction_force("left")
            self.attack_init()

    def die(self):
        self.alive = False

class Car(Entity):
    def __init__(self,game, pos, radius):
        super().__init__(game,pos,radius,None)
        self.alive = True  # Add a variable to track if the ghost is alive or dead
        self.create_hitbox(self,0,0,radius/2,float("inf"),15)
        self.hurtbox = None
        self.accelerator = Vector(0,0) #Adds speed to the current vector
        self.accel = Vector(0.04,0)
        self.max_accel_vel = Vector(7.5,0)
        
        self.sprites = Spritesheet(self, self,
                                   "https://www.cs.rhul.ac.uk/home/zmac436/cs1822/car.png",
                                   1, 10, self.pos.copy(), Vector(0,-(7)),279,108)
        self.sprites.frame_index = [0, 1]
        self.sprites.start_index = [0, 1]
        self.sprites.end_index = [0, 5]
        
        self.warning_sign_visible = False
    
    def load_init(self):
        self.visible = False
        self.state = "warning"
        self.state_initialise(1,0,180)
        self.warning_sign_visible = True
        
    def warn(self):
        if self.warning_sign_visible == True and self.clocks.timer % 60 == 50:
            self.warning_sign_visible = False
        
        if self.warning_sign_visible == False and self.clocks.timer % 60 == 10:
            self.warning_sign_visible = True
            
        if self.clocks.timer >= self.clocks.time:
            self.warn_end()
    
    def warn_end(self):
        self.warning_sign_visible = False
        self.attack_init()
        
    def attack_init(self):
        self.visible = True
        self.state = "attack"
        self.state_initialise(8,0,6,[0,1],[0,5])

    def update(self, target):
        self.clocks.tick()
        
        if self.alive and self.state == "attack":
            self.vel = Vector(self.adjust_num_for_direction(25),0)
            self.pos.add(self.vel)

            if (self.pos.x < (0-self.radius*2) or self.pos.x > (self.game.WIDTH+self.radius*2) or
                self.pos.y < 0 or self.pos.y > self.game.HEIGHT):
                self.die()

            self.hitbox.update()
        
            
        if self.state == "attack":
            self.advance_frame()
            if (self.clocks.timer >= self.clocks.time):
                self.clocks.timer = 0
                
        if self.state == "warning":
            self.warn()

    def draw(self, canvas):
        if self.alive and self.visible:  
            self.sprites.draw(canvas)
            self.hitbox.draw(canvas)
            
        if self.warning_sign_visible:
            x_offset = self.game.WIDTH/10 + ((random.randrange(-3, 9)*self.clocks.timer/self.clocks.time) if self.clocks.timer >= 120 else 0)
            y_offset = self.game.HEIGHT/7.5 + ((random.randrange(-3, 9)*self.clocks.timer/self.clocks.time) if self.clocks.timer >= 120 else 0)
            warning_radius = self.radius/3
            text_size = warning_radius
           
            
            if self.direction == "right":
                canvas.draw_circle((0 + x_offset, self.game.FLOOR - y_offset),warning_radius,5,"White", "Red")
                canvas.draw_text("!", (0 + x_offset -4.1 ,self.game.FLOOR - y_offset + 4.1),text_size,"White","serif")
            else:
                canvas.draw_circle((self.game.WIDTH - x_offset, self.game.FLOOR - y_offset),warning_radius,5,"White","Red")
                canvas.draw_text("!", (self.game.WIDTH - x_offset -4.1 ,self.game.FLOOR - y_offset + 4.1),text_size,"White","serif")
                
            
            
    def hit(self):
        pass
    
    def hurt(self):
        pass
    
    def reset(self):
        pass

    def die(self):
        self.alive = False

class Shooter(Entity):
    def __init__(self,game, pos, radius):
        super().__init__(game,pos,radius,None)
        self.state = "air_attack"
        self.alive = True  # Add a variable to track if the ghost is alive or dead
        self.create_hitbox(self,0,0,radius/2,float("inf"),15)
        self.accelerator = Vector(0,0) #Adds speed to the current vector
        self.accel = Vector(0.04,0)
        self.max_accel_vel = Vector(7.5,0)
        
        self.sprites = Spritesheet(self, self,
                                   "https://www.cs.rhul.ac.uk/home/zmac436/cs1822/enemy.png",
                                   6, 16, self.pos.copy(), Vector(0,-10),124,127)
        self.sprites.frame_index = [3, 0]
        self.sprites.start_index = [3, 0]
        self.sprites.end_index = [3, 6]
    
    def load_init(self):
        self.attack_init()
    
    def hit(self):
        self.reset()
    
    def hurt(self):
        self.die()
        
    def attack_init(self):
        self.state = "air_attack"
        self.state_initialise(8,0,6,[3,0],[3,6])

    def update(self, target):
        self.clocks.tick()
        
        if self.alive:
            self.accelerator.add(self.accel)
            self.accelerator.x = min(self.accelerator.x,self.max_accel_vel.x)
            # Calculate the vector pointing from the enemy to the target (player)
            direction = target.hurtbox.pos - self.pos
            direction.normalize()  # normalize the vector to get a unit vector
            self.vel = direction * (2+self.accelerator.x)
            self.pos.add(self.vel)

            if (self.pos.x < 0 or self.pos.x > self.game.WIDTH or
                self.pos.y < 0 or self.pos.y > self.game.HEIGHT):
                self.reset()

            self.hitbox.update()
            self.hurtbox.update()
            
        if self.state == "air_attack":
            self.advance_frame()
            if (self.clocks.timer >= self.clocks.time):
                self.clocks.timer = 0

    def draw(self, canvas):
        if self.alive:  # Only draw the ghost if it's alive
            self.sprites.draw(canvas)
            self.hitbox.draw(canvas)
            self.hurtbox.draw(canvas)
            

    def reset(self):
        if random.choice([True, False]):  # choose left or right side randomly
            self.pos = Vector(0, random.uniform(0,self.game.FLOOR - 40))  
            self.vel = Vector(random.uniform(1, 4), 0)
            self.accelerator = Vector()
            self.hitbox.pos = self.pos.copy()
            self.hurtbox.pos = self.pos.copy()
            self.direction_force("right")
            self.attack_init()
        else:
            self.pos = Vector(self.game.WIDTH, random.uniform(0,self.game.FLOOR - 40)) 
            self.vel = Vector(random.uniform(-4, -1), 0)
            self.accelerator = Vector()
            self.hitbox.pos = self.pos.copy()
            self.hurtbox.pos = self.pos.copy()
            self.direction_force("left")
            self.attack_init()

    def die(self):
        self.alive = False        

class Clocks:
    def __init__(self,owner):
        self.owner = owner
        self.timer = 0
        self.time = -1
        self.frame_timer = 0
        self.frame_duration = 1
        
    def transition_check(self, frame_duration):
        return self.frame_timer % frame_duration == 0

    def tick(self):
        self.frame_timer += 1
        if self.transition_check(self.frame_duration):
            self.timer +=1
            self.frame_timer = 0
        

class Collision_Box: #abstract - do not instantiate
    def __init__(self,owner,offset,radius):
        self.owner = owner
        self.offset = offset
        self.pos = self.owner.pos.copy().add(offset)
        self.radius = radius
        self.visible = False
        
    def destroy_box(self):
        pass
    
    def hit(self, box):
        distance = self.pos.copy().subtract(box.pos).length()
        return distance <= self.radius + box.radius
        
    def update(self):
        self.pos.add(self.owner.pos.copy().add(self.offset).subtract(self.pos))
        
    def draw(self, canvas):
        if self.visible:
            canvas.draw_circle((self.pos.get_p()),self.radius,5,"Red")
             
    
class Hitbox(Collision_Box):
    def __init__(self,owner,offset,radius,time,hitlag):
        super().__init__(owner,offset,radius)
        self.hitlag = hitlag
        self.clocks = Clocks(self)
        self.clocks.time = time
    
    def update(self):
        super().update()
        self.clocks.tick()
        
        if self.clocks.timer >= self.clocks.time and self.clocks.time is not float("inf"):
            self.destroy_hitbox()

    def destroy_hitbox(self):
        self.owner.hitbox = None
        
class Hurtbox(Collision_Box):
    def __init__(self,owner,offset,radius):
        super().__init__(owner,offset,radius)
                
    def draw(self, canvas):
        if self.visible:
            canvas.draw_circle((self.owner.pos.get_p()),self.radius,5,"Green") # this is the player pos
            canvas.draw_circle((self.pos.get_p()),self.radius,5,"Blue")
            
        
class Keyboard:
    def __init__(self,game):
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        
    def keyDown(self, key):
        if key == simplegui.KEY_MAP['up'] or key == simplegui.KEY_MAP['w'] or key == simplegui.KEY_MAP['space']:
            self.up = True
        if key == simplegui.KEY_MAP['down'] or key == simplegui.KEY_MAP['s']:
            self.down = True
        if key == simplegui.KEY_MAP['left'] or key == simplegui.KEY_MAP['a']:
            self.left = True
        if key == simplegui.KEY_MAP['right'] or key == simplegui.KEY_MAP['d']:
            self.right = True

    def keyUp(self, key):
        if key == simplegui.KEY_MAP['up'] or key == simplegui.KEY_MAP['w'] or key == simplegui.KEY_MAP['space']:
            self.up = False
        if key == simplegui.KEY_MAP['down'] or key == simplegui.KEY_MAP['s']:
            self.down = False
        if key == simplegui.KEY_MAP['left'] or key == simplegui.KEY_MAP['a']:
            self.left = False
        if key == simplegui.KEY_MAP['right'] or key == simplegui.KEY_MAP['d']:
            self.right = False
    

class Interaction:
    def __init__(self, game, player, enemies, keyboard):
        self.game = game
        self.player = player
        self.non_paused = set()
        self.enemies = enemies
        self.keyboard = keyboard
        self.hit_cooldown = 5  # Cooldown in frames between hits
        self.hit_timer = 0
        self.stop_timer = 0
        self.elapsed_time = 0
    
    
        
        # Timer for adding enemies for a random amount of seconds
        self.add_enemy_timer = simplegui.create_timer(random.randint(1000,2000), self.add_enemy)
    
    def choose_enemy(self):
        chosen = random.choice(["ghost","ghost","ghost","ghost","ghost","car"]) # choices are car,ghost, and shooter
        
        if chosen == "ghost":
            return Ghost(self.game, Vector((0),(random.uniform(0,self.game.FLOOR-40))),20)
        
        elif chosen == "car":
            radius = 75
            return Car(self.game, Vector(0,self.game.FLOOR-radius*0.5),radius)
        
        elif chosen == "shooter":
            return Shooter(self.game, Vector((0),(random.uniform(0,self.game.FLOOR-40))),25)
        
    def add_enemy(self):
        direction = random.choice(["left", "right"])
        enemy = self.choose_enemy()
        enemy.direction = direction
        
        if direction == "left":
            enemy.pos.x = self.game.WIDTH
            enemy.hitbox.update() # Avoids a bug where the hitbox appears on the left side for a frame
        
        self.enemies.add(enemy)
        enemy.direction_force(enemy.direction)
        enemy.load_init()
        
        
        self.add_enemy_timer.stop()
        self.add_enemy_timer = simplegui.create_timer(random.randint(max(500,int(1000-self.elapsed_time/7)),max(1200,int(3000-self.elapsed_time/7))), self.add_enemy)
        self.add_enemy_timer.start()
        enemy.accel.x = min(0.12,enemy.accel.x + (self.elapsed_time * 0.0000015))
        enemy.max_accel_vel.x = min(15.6,enemy.max_accel_vel.x + self.elapsed_time/10000)

        
        
    def update(self):
        if self.elapsed_time % 60 == 0:
            self.player.score += 1
        self.elapsed_time += 1
        if self.stop_timer > 0:
            expired = set()
            for entity in self.non_paused:
                entity.update()
                if entity.state != "hurt":
                    expired.add(entity)
            self.non_paused = self.non_paused.difference(expired)
            self.stop_timer -=1
        else:
            if self.player.lives <= 0:  # Check if player's lives are 0
                self.game_over()
                return
            
            # Code to allow the player to jump  
            elif self.keyboard.up and self.player.on_ground() and self.player.state is not "attack" and self.player.state is not "air_attack" or (self.keyboard.up and self.player.hit_cancel and self.player.on_ground()):
                self.player.jump()
                self.keyboard.up = False
                self.player.jumps = 1
                self.player.direction_force(self.player.direction)
                
            #Code that allows the player to double jump
            if (self.keyboard.up and self.player.jumps ==1 and self.player.state is "airborne") or (self.keyboard.up and self.player.hit_cancel and self.player.on_ground() == False):
                self.player.jumps = 2
                self.player.double_jump_init()
                self.keyboard.up = False
                self.player.direction_force(self.player.direction)
            
            #Code to buffer fastfalling- allows for tighter control of the character
            if self.player.state == "air_attack" and self.player.hit_cancel == True and self.keyboard.down:
                self.player.buffered_down = True
                
            #Code that actually enables fastfalling
            if self.keyboard.down and not self.player.fastfalling and self.player.state == "airborne":
                self.player.fastfall()
            
            #Code that allows the player to attack
            if (self.keyboard.left or self.keyboard.right) and (
                    self.player.state == "idle" or self.player.state == "airborne" or self.player.hit_cancel):
                if self.keyboard.left:
                    self.player.direction_force("left")
                    self.keyboard.left = False
                else:
                    self.player.direction_force("right")
                    self.keyboard.right = False
                self.player.attack_init() if (self.player.state == "idle" or self.player.state == "attack") else self.player.air_attack_init()
                self.player.direction_force(self.player.direction)
            

            #Code that allows for the player to switch directions when attacking in the air
            if self.player.state == "air_attack" and self.player.clocks.timer <= 2:
                if self.keyboard.left:
                    self.player.direction_force("left")
                    self.player.adjust_frame_for_direction(self.player.sprites.frame_index)
                    self.player.adjust_frame_for_direction(self.player.sprites.start_index)
                    self.player.adjust_frame_for_direction(self.player.sprites.end_index)
                    self.keyboard.left = False
                elif self.keyboard.right:
                    self.player.direction_force("right")
                    self.player.adjust_frame_for_direction(self.player.sprites.frame_index)
                    self.player.adjust_frame_for_direction(self.player.sprites.start_index)
                    self.player.adjust_frame_for_direction(self.player.sprites.end_index)
                    self.keyboard.right = False

            removed = set()
            for enemy in self.enemies:
                enemy.update(self.player)  # Pass the player as the target
                # Check collision with the player
                if self.player.hitbox is not None and enemy.hurtbox is not None and self.player.hitbox.hit(enemy.hurtbox):
                    self.player.hit()
                    self.stop_timer = self.player.hitbox.hitlag
                    enemy.hurt()  # Kill the enemy if it collides with the player

                elif enemy.hitbox.hit(self.player.hurtbox):
                    if not self.player.invincible:
                        self.stop_timer = enemy.hitbox.hitlag
                        self.player.hurt_init(enemy.hitbox.hitlag)
                        self.player.iclocks.time = 120
                        self.player.invincible = True
                        self.non_paused.add(self.player)
                        enemy.hit()
                    else:
                        enemy.hurt()
                if enemy.alive == False:
                    removed.add(enemy)
   
            
            
            self.enemies = self.enemies.difference(removed)
            self.player.update()

            # Decrement hit cooldown timer
            if self.hit_timer > 0:
                self.hit_timer -= 1
       
            
            

    def draw(self, canvas):
        self.game.background.draw(canvas)
        self.update()
        self.player.draw(canvas)
        for enemy in self.enemies:
            enemy.draw(canvas)
        
        canvas.draw_text("Score: " + str(self.player.score), (10, 30), 24, "White")
        canvas.draw_text("Lives: " + str(self.player.lives), (self.game.WIDTH - 100, 30), 24, "White")
        canvas.draw_text("Hits: " + str(self.player.heat), ((self.game.WIDTH-100)/2, 30), 24, "White")
        #canvas.draw_line((0,self.game.FLOOR),(self.game.WIDTH,self.game.FLOOR),1,"Yellow")


    

    def game_over(self):
        # Display game over screen
        self.game.frame.stop()
        self.game.frame = simplegui.create_frame('Game Over', self.game.WIDTH, self.game.HEIGHT)
        self.game.frame.set_draw_handler(self.draw_game_over)
        self.game.frame.add_button("Play Again", self.restart_game, 100)
        self.game.frame.start()

    def draw_game_over(self, canvas):
        # Draw a semi-transparent background rectangle using polygons
        background_polygon = [(0, 0), (self.game.WIDTH, 0),
                            (self.game.WIDTH, self.game.HEIGHT),
                            (0, self.game.HEIGHT)]
        canvas.draw_polygon(background_polygon, 1, 'Black', 'rgba(0, 0, 0, 0.7)')

        # Draw "Game Over" text
        canvas.draw_text("Game Over!", (self.game.WIDTH / 2 - 100, self.game.HEIGHT / 2 - 50), 50, "White")

        # Draw final score
        canvas.draw_text("Final Score: " + str(self.player.score), (self.game.WIDTH / 2 - 70, self.game.HEIGHT / 2), 36, "White")

        # Draw "Play Again" button
        play_again_button_pos = (self.game.WIDTH / 2 - 50, self.game.HEIGHT / 2 + 50)
        canvas.draw_polygon([(play_again_button_pos[0], play_again_button_pos[1]),
                            (play_again_button_pos[0] + 130, play_again_button_pos[1]),
                            (play_again_button_pos[0] + 130, play_again_button_pos[1] + 40),
                            (play_again_button_pos[0], play_again_button_pos[1] + 40)],
                            1, 'White', 'Green')
        canvas.draw_text("Play Again", (self.game.WIDTH / 2 - 40, self.game.HEIGHT / 2 + 75), 24, "White")

    def restart_game(self):
        # Restart the game
        self.game.frame.stop()
        self.game = Game(1218, 384)
        self.game.frame.start()




game = Game(1218,384)
game.frame.start()







