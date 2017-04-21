# g.py - globals
import pygame,utils,random

app='DidgArt'; ver='1'
ver='21'
ver='22'
# first save -> load 1 shows
ver='23'
# depth forced to 32 on both g.surf & g.carry_surf
ver='24'
# load number updated after save
# min size of shape hot spots = sy(1)
ver='25'
# use simple load/save numbers
ver='26'
# uses colours instead of colour swatch
# counts the files in saves to establish current count
ver='27'
# no pointer version

UP=(264,273)
DOWN=(258,274)
LEFT=(260,276)
RIGHT=(262,275)
CROSS=(259,120)
CIRCLE=(265,111)
SQUARE=(263,32)
TICK=(257,13)
NUMBERS={pygame.K_1:1,pygame.K_2:2,pygame.K_3:3,pygame.K_4:4,\
           pygame.K_5:5,pygame.K_6:6,pygame.K_7:7,pygame.K_8:8,\
           pygame.K_9:9,pygame.K_0:0}

def init(): # called by run()
    random.seed()
    global redraw
    global screen,w,h,font1,font2,clock
    global factor,offset,imgf,message,version_display
    global pos,pointer
    redraw=True
    version_display=False
    screen = pygame.display.get_surface()
    pygame.display.set_caption(app)
    screen.fill((70,0,70))
    pygame.display.flip()
    w,h=screen.get_size()
    if float(w)/float(h)>1.5: #widescreen
        offset=(w-4*h/3)/2 # we assume 4:3 - centre on widescreen
    else:
        h=int(.75*w) # allow for toolbar - works to 4:3
        offset=0
    factor=float(h)/24 # measurement scaling factor (32x24 = design units)
    imgf=float(h)/900 # image scaling factor - all images built for 1200x900
    clock=pygame.time.Clock()
    if pygame.font:
        t=int(40*imgf); font1=pygame.font.Font(None,t)
        t=int(80*imgf); font2=pygame.font.Font(None,t)
    message=''
    pos=pygame.mouse.get_pos()
    #pointer=utils.load_image('pointer.png',True)
    #pygame.mouse.set_visible(False)
    
    # this activity only
    global surf,overlay,surf_xy,surf_w,surf_h,load_n,save_n,saves_n,margin
    global carry,carry_shape,carry_img,carry_xy,carry_save
    global scales,scale,colour_ind,angle
    surf=pygame.Surface((sy(25),sy(18))); surf.fill(utils.CREAM)
    overlay=pygame.Surface((sy(25),sy(18)),pygame.SRCALPHA,32)
    surf_w=surf.get_width(); surf_h=surf.get_height()
    surf_xy=(sx(16)-surf_w/2,sy(16)-surf_w/2); margin=surf_xy[1]
    load_n=None; save_n=None; saves_n=None # set in load_save.retrieve()
    carry=None; carry_shape=None; carry_img=None; carry_xy=None; carry_save=None
    scales=[.1,.2,.3,.4,.5,.6,.7,.8,.9,1]
    scale=.2; colour_ind=0; angle=0
    
def sx(f): # scale x function
    return int(f*factor+offset+.5)

def sy(f): # scale y function
    return int(f*factor+.5)
