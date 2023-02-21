# if pygame module does not exist currently
# go to command prompt and type
# pip install pygame
# to convert to .exe file, go to command prompt and type
# pip install pyinstaller
# go to the directory where this .py file is located
# type cmd at the address bar, press enter, then type
# pyinstaller --onefile -w main.py
# after conversion the .exe file will be located at the folder named 'dist' and get it out of that folder
# additional folder named 'build' will be there as well and it can be deleted along with 'dist'
# try running the exe file
# using auto py to exe --------
# pip install auto-py-to-exe
# CMD, type "auto-py-to-exe", hit enter
# then just browse the .py file you want converted and icon, if there is any
import pygame
import math
from sys import exit

x = 0
y = 0
time = 0
scrolltime = 0
power = 0
angle = 0
angle2 = 0
time1 = 0
time2 = 0
click = 0
wind = 0
ground1x = 0
ground2x = 1200
ballxpos = 43
ballypos = 440
shoot = False
run = True
active_state = False
object_string = 0
stringsize = 0
entry_color = (255, 255, 255)
rotation = 0
endrotate = 0
endx = 0
endy = 0
mouseclick2 = False

pygame.init()
clock = pygame.time.Clock()
win = pygame.display.set_mode((1200, 500))
icon = pygame.image.load('icon.jpg').convert()
pygame.display.set_icon(icon)
pygame.display.set_caption('Projectile Motion')

golf_clouds1 = pygame.image.load('clouds1.png').convert_alpha() # .convert_alpha() makes the image transparent
golf_clouds2 = pygame.image.load('clouds2.png').convert_alpha()
golf_clouds3 = pygame.image.load('clouds3.png').convert_alpha()
golf_ground1 = pygame.image.load('ground1.png').convert_alpha()
golf_ground2 = pygame.image.load('ground2.png').convert_alpha()
golf_sky = pygame.image.load('sky.png').convert_alpha()
gun_bg = pygame.image.load('Background UI2.png').convert_alpha()
arrow_bg = pygame.image.load('Background UI3.png').convert_alpha()
home_bg_img = pygame.image.load('HomeBackground.png').convert_alpha()
selection = pygame.image.load('Selection.png').convert_alpha()
help_bg = pygame.image.load('Help.png').convert_alpha()
bow = pygame.image.load('bow.png').convert()
arrow = pygame.image.load('arrow.png').convert()
gun = pygame.image.load('gun.png').convert()
bullet = pygame.image.load('bullet.png').convert()
home_bg_img = pygame.transform.scale(home_bg_img,(1200,500))
arrow.set_colorkey((0,0,0))
bow.set_colorkey((0,0,0))
gun.set_colorkey((0,0,0))
bullet.set_colorkey((0,0,0))

simulate_button = False
ballsim = False
arrowsim = False
gunsim = False
help_button = False
home_frame_state = True

# functions for buttons

def golf_return():
    global simulate_button
    global ballsim
    global object_string
    simulate_button = True
    ballsim = False
    object_string = 0

def arrow_return():
    global simulate_button
    global arrowsim
    global object_string
    simulate_button = True
    arrowsim = False
    object_string = 0

def bullet_return():
    global simulate_button
    global gunsim
    global object_string
    simulate_button = True
    gunsim = False
    object_string = 0

def help_return():
    global home_frame_state
    global help_button
    home_frame_state = True
    help_button = False

def simulate_return():
    global home_frame_state
    global simulate_button
    home_frame_state = True
    simulate_button = False

# objects

class ball(object): # Creating a class defining the properties of a ball
    def __init__(self,x,y,radius,color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    def draw(self,win):
        # black outline of the ball
        pygame.draw.circle(win, (0,0,0), (self.x, self.y), self.radius)
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius-1)

    @staticmethod
    def ballPath(startx,starty,power,angle,time,x1,x2,scrolltime): # Static method within the ball class
        initvelx = power * math.cos(angle)
        initvely = power * math.sin(angle)
        if ballsim == True:
            tVel = 75
        elif arrowsim == True:
            tVel = 83
        elif gunsim == True:
            tVel = 50
        else:
            tVel = 1

        # Formula for the path of the ball with air resistance and gravity present
        # x-component and y-component of the object
        newx = (startx + ((initvelx * tVel / 9.8) * (1 - (math.e ** ((-9.8 * time) / tVel)))))
        newy = (starty - ((tVel / 9.8) * (initvely + tVel) * (1 - (math.e ** ((-9.8 * time) / tVel))) - (tVel * time)))

        xvel = math.cos(angle) * initvelx * math.e ** ((-9.8 * time)/tVel)
        yvel = (tVel + math.sin(angle) * initvely) * (math.e ** ((-9.8 * time)/tVel)) - tVel

        # Formula for the rotation of object with respect to its components
        if xvel == 0:
            rotation = 270
        else:
            rotation = (math.atan(yvel/xvel)) * 180/math.pi

        ground1x = round(x1 - ((power * math.cos(angle) * 75 / 9.8) * (1 - (math.e ** ((-9.8 * scrolltime) / 75)))))
        ground2x = round(x2 - ((power * math.cos(angle) * 75 / 9.8) * (1 - (math.e ** ((-9.8 * scrolltime) / 75)))))
        return(newx,newy,ground1x,ground2x,rotation)

class textbox(object): # Creating a class defining the properties of textbox
    def __init__(self,string,fontstyle,fontsize,bool,color_Text,color_BG,x,y):
        self.string = string
        self.fontstyle = fontstyle
        self.fontsize = fontsize
        self.bool = bool
        self.color_Text = color_Text
        self.color_BG = color_BG
        self.x = x
        self.y = y
        self.font = pygame.font.SysFont(self.fontstyle, self.fontsize)
        self.text = self.font.render(self.string, self.bool, self.color_Text, self.color_BG)
        self.textRect = self.text.get_rect()
        self.textRect.center = (self.x, self.y)

    def draw(self,win):
        win.blit(self.text, self.textRect)

class button(object):
    def __init__(self,string,fontstyle,fontsize,bool,color_Text,color_BG,x,y,width,height,color_Button_active,color_Button_inactive,command):
        self.string = string
        self.fontstyle = fontstyle
        self.fontsize = fontsize
        self.bool = bool
        self.color_Text = color_Text
        self.color_BG = color_BG
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color_Button_active = color_Button_active
        self.color_Button_inactive = color_Button_inactive
        self.font = pygame.font.SysFont(self.fontstyle, self.fontsize)
        self.text = self.font.render(self.string, self.bool, self.color_Text, self.color_BG)
        self.textRect = self.text.get_rect()
        self.textRect.center = (self.x + self.width // 2, self.y + self.height // 2)
        self.command = command

    def draw(self,win):
        global mouseclick
        if self.x <= pos[0] <= self.x + self.width and self.y <= pos[1] <= self.x + self.height and event.type == pygame.MOUSEBUTTONDOWN:
            # Change the button's color when clicking the mouse
            button_color = self.color_Button_active
            if mouseclick == False:
                self.command()
                mouseclick = True
        else:
            # Reset the button's color when the mouse is not hovering over it
            button_color = self.color_Button_inactive
            mouseclick = False

        # Draw the button
        pygame.draw.rect(win, button_color, (self.x, self.y, self.width, self.height))
        win.blit(self.text,self.textRect)

class entrybox(object):
    def __init__(self,string,fontstyle,fontsize,bool,color_Text,color_BG,x,y,width,height,color_Button_active,color_Button_inactive,BordWidth,BordRadius):
        self.string = string
        self.fontstyle = fontstyle
        self.fontsize = fontsize
        self.bool = bool
        self.color_Text = color_Text
        self.color_BG = color_BG
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color_Button_active = color_Button_active
        self.color_Button_inactive = color_Button_inactive
        self.BordWidth = BordWidth
        self.BordRadius = BordRadius
        self.font = pygame.font.SysFont(self.fontstyle, self.fontsize)
        self.text = self.font.render(str(self.string), self.bool, self.color_Text, self.color_BG)
        self.textRect = self.text.get_rect()
        self.textRect.center = (self.x + self.width // 2, self.y + self.height // 2)

    def draw(self,win):
        global active_state
        global object_string
        global entry_color
        global stringsize
        if self.x <= pos[0] <= self.x + self.width and self.y <= pos[1] <= self.y + self.height and event.type == pygame.MOUSEBUTTONDOWN:
            # Change the button's color when clicking the button
            entry_color = self.color_Button_active
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)
            if active_state == False:
                active_state = True
                object_string = ''
                stringsize = 0
        else:
            # Reset the button's color when the mouse is not hovering over it and becomes inactive
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if active_state == True:
                    entry_color = self.color_Button_inactive
                    active_state = False
                    if object_string == '0':
                        object_string = '0'

        pygame.draw.rect(win, entry_color, (self.x, self.y, self.width, self.height),0,self.BordRadius)
        pygame.draw.rect(win,(0,0,0),(self.x, self.y, self.width, self.height),self.BordWidth,self.BordRadius)
        win.blit(self.text,self.textRect)

def redrawWindow(): # Update function to simulate movements of objects
    global mouseclick2
    win.fill((255, 255, 255))
    if home_frame_state == True:
        win.blit(home_bg_img,(0,0))
    if simulate_button == True:
        win.blit(selection,(0,0))
        simulate_return_button1.draw(win)
    if ballsim == True:
        win.blit(golf_sky, (0, 0))
        win.blit(golf_ground1, (ground1x, 0))
        win.blit(golf_ground2, (ground2x, 0))
        win.blit(golf_clouds1, (ground1x, 0))
        win.blit(golf_clouds2, (ground2x, 0))
        golfBall.draw(win)
        angle_text.draw(win)
        golf_return_button1.draw(win)
        entry1.draw(win)
    if arrowsim == True:
        win.blit(arrow_bg,(0,0))
        win.blit(arrow_rotate,(golfBall.x - arrow_rotate.get_width() // 2, golfBall.y - arrow_rotate.get_height() // 2))
        win.blit(bow_rotate,(ballxpos - bow_rotate.get_width() // 2, ballypos-4 - bow_rotate.get_height() // 2))
        arrow_return_button1.draw(win)
        entry1.draw(win)
        if event.type == pygame.KEYDOWN:
            mouseclick2 = True
    if gunsim == True:
        win.blit(gun_bg,(0,0))
        win.blit(bullet_rotate,(golfBall.x - arrow_rotate.get_width() // 2, golfBall.y - arrow_rotate.get_height() // 2))
        win.blit(gun_rotate,(ballxpos - bow_rotate.get_width() // 2, ballypos-4 - bow_rotate.get_height() // 2))
        bullet_return_button1.draw(win)
        entry1.draw(win)
    if help_button == True:
        win.blit(help_bg,(0,0))
        help_return_button1.draw(win)
    #pygame.draw.line(win,(50,0,255),line[0],line[1])
    pygame.display.update()

def findAngle(pos): # Finding angle of the line between the ball and the cursor with the ball as the origin
    sX = ballxpos
    sY = ballypos-5
    try:
        angle = math.atan((sY - pos[1]) / (sX - pos[0]))
    except:
        angle = math.pi/2

    if pos[1] < sY and pos[0] > sX:
        angle = abs(angle)
    elif pos[1] < sY and pos[0] < sX:
        angle = math.pi-angle
    elif pos[1] > sY and pos[0] < sX:
        angle = math.pi+abs(angle)
    elif pos[1] > sY and pos[0] > sX:
        angle = (math.pi*2) - angle

    return angle

golfBall = ball(ballxpos,ballypos-5,5,(255,255,255)) # Moving ball
residueBall = ball(ballxpos,ballypos-5,5,(255,255,255)) # Marker ball

while run: # Will keep the execution of the program until exit
    pos = pygame.mouse.get_pos()
    line = [(ballxpos,ballypos-5),pos]
    arrow_rotate = pygame.transform.rotate(arrow, rotation)
    bow_rotate = pygame.transform.rotate(bow, findAngle(pos)*180/math.pi)
    bullet_rotate = pygame.transform.rotate(bullet,0)
    gun_rotate = pygame.transform.rotate(gun, findAngle(pos)*180/math.pi)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if home_frame_state == True:
                if 763 <= pos[0] <= 763 + 298 and 147 <= pos[1] <= 147 + 54:
                    simulate_button = True
                    home_frame_state = False
                elif 763 <= pos[0] <= 763 + 298 and 226 <= pos[1] <= 226 + 54:
                    help_button = True
                    home_frame_state = False
                elif 761 <= pos[0] <= 761 + 298 and 306 <= pos[1] <= 306 + 54:
                    exit()

            if simulate_button == True:
                if 347 <= pos[0] <= 475 and 223 <= pos[1] <= 352:
                    ballsim = True
                    simulate_button = False
                elif 570 <= pos[0] <= 697 and 227 <= pos[1] <= 350:
                    arrowsim = True
                    simulate_button = False
                elif 786 <= pos[0] <= 915 and 225 <= pos[1] <= 350:
                    gunsim = True
                    simulate_button = False
            if shoot == False:
                shoot = True
                golfBall.x = ballxpos
                golfBall.y = ballypos - golfBall.radius
                x = golfBall.x
                y = golfBall.y
                time = 0
                scrolltime = 0
                ground1x = 0
                ground2x = 1200
                if object_string == '':
                    object_string = 0
                power = 1.5 * int(object_string) #meters? #math.sqrt((line[1][1]-line[0][1])**2 + (line[1][0]-line[0][0])**2)/9.67
                angle = findAngle(pos)

        if active_state == True:
            if event.type == pygame.KEYDOWN:
                if stringsize < 0:
                    stringsize = 0
                elif stringsize == 5:
                    if event.key == pygame.K_BACKSPACE:
                        object_string = object_string[:-1]
                        stringsize -= 1
                else:
                    if event.key == pygame.K_BACKSPACE:
                        object_string = object_string[:-1]
                        stringsize -= 1
                    elif event.key == pygame.K_0:
                        object_string += event.unicode
                        stringsize += 1
                    elif event.key == pygame.K_1:
                        object_string += event.unicode
                        stringsize += 1
                    elif event.key == pygame.K_2:
                        object_string += event.unicode
                        stringsize += 1
                    elif event.key == pygame.K_3:
                        object_string += event.unicode
                        stringsize += 1
                    elif event.key == pygame.K_4:
                        object_string += event.unicode
                        stringsize += 1
                    elif event.key == pygame.K_5:
                        object_string += event.unicode
                        stringsize += 1
                    elif event.key == pygame.K_6:
                        object_string += event.unicode
                        stringsize += 1
                    elif event.key == pygame.K_7:
                        object_string += event.unicode
                        stringsize += 1
                    elif event.key == pygame.K_8:
                        object_string += event.unicode
                        stringsize += 1
                    elif event.key == pygame.K_9:
                        object_string += event.unicode
                        stringsize += 1

    if shoot:
        if ballsim == True:
            if golfBall.y < ballypos - golfBall.radius+1 and golfBall.y > 0:
                # flight
                time += 0.0375
                po = ball.ballPath(x, y, power, angle, time, 0, 1200, scrolltime)
                golfBall.y = po[1]
                if golfBall.x >= 1200-8:
                    scrolltime += 0.0325
                    ground1x = po[2]
                    if ground2x > 0:
                        ground2x = po[3]
                    else:
                        ground2x = 0
                else:
                    golfBall.x = po[0]
            else:
                # touching the ground
                shoot = False
                click = 1
                endx = golfBall.x
                endy = golfBall.y
        elif arrowsim == True:
            if golfBall.y < ballypos - golfBall.radius + 1 and golfBall.y > 0 and (golfBall.x < 1040 or (golfBall.y < 347)):
                # flight
                time += 0.0375
                po = ball.ballPath(x, y, power, angle, time, 0, 1200, scrolltime)
                golfBall.y = po[1]
                golfBall.x = po[0]
                rotation = po[4]
            else:
                shoot = False
                click = 1
        elif gunsim == True:
            if golfBall.y < ballypos - golfBall.radius + 1 and golfBall.y > 0 and golfBall.x < 1300 and (golfBall.x < 1090 or (golfBall.y < 363)):
                # flight
                time += 0.0375
                po = ball.ballPath(x, y, power, angle, time, 0, 1200, scrolltime)
                golfBall.y = po[1]
                golfBall.x = po[0]
            else:
                # touching the ground
                shoot = False
                click = 1
                endx = golfBall.x
                endy = golfBall.y
    else:
        if mouseclick2 == False:
            rotation = findAngle(pos) * 180 / math.pi

    disp_angle = str(round(findAngle(pos) * 180 / math.pi)) + "°"  # alt + 0176 = °
    angle_text = textbox(disp_angle, 'monospace', 35, True, (0, 0, 0), None, pos[0] + 20, pos[1] - 10)
    golf_return_button1 = button('X', 'system', 35, True, (255, 0, 0), None, 0, 0, 35, 35, (0, 255, 0), (0, 0, 0),golf_return)
    arrow_return_button1 = button('X', 'system', 35, True, (255, 0, 0), None, 0, 0, 35, 35, (0, 255, 0), (0, 0, 0),arrow_return)
    bullet_return_button1 = button('X', 'system', 35, True, (255, 0, 0), None, 0, 0, 35, 35, (0, 255, 0), (0, 0, 0),bullet_return)
    simulate_return_button1 = button('X', 'system', 35, True, (255, 0, 0), None, 0, 0, 35, 35, (0, 255, 0), (0, 0, 0),simulate_return)
    help_return_button1 = button('X', 'system', 35, True, (255, 0, 0), None, 0, 0, 35, 35, (0, 255, 0), (0, 0, 0),help_return)
    entry1 = entrybox(object_string,'monospace', 35, True, (255, 0, 0), None, 200, 100, 125, 35, (200,200,200), (255,255,255),1,15)
    redrawWindow()

exit()