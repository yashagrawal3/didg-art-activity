#didg.py
import utils,g,pygame,random

colours=[(0,0,0), \
         (77, 43, 22), (162, 70, 33), (176, 129, 17), (193, 134, 48), \
         (157, 141, 142), (240, 80, 10), (255, 0, 0), (240, 150, 62), \
         (242, 160, 147), (245, 202, 232), (215, 167, 50), (244, 214, 51), \
         (243, 230, 160), (255, 255, 192), (48, 68, 75), (47, 84, 126), \
         (44, 102, 181), (0,0,255), (0,255,0), (255, 255, 255)]

shapes=[]

class Shape:
    pass

class Didg:
    def __init__(self):
        gap=g.sy(.4); x=g.sx(.3); maxw=0; maxh=0
        for ind in range(10):
            shape=Shape(); shapes.append(shape)
            img=utils.load_image('0'+str(ind)+'.png',True,'shapes')
            w=img.get_width(); h=img.get_height()
            if w>maxw: maxw=w
            if h>maxh: maxh=h
            w=int(.2*w); h=int(.2*h)
            shape.img_tn=pygame.transform.scale(img,(w,h))
            shape.x=x; shape.y=(g.margin-h)/2; x+=(w+gap)
            shape.w=w; shape.h=h
            shape.imgs=[img]
            for n in range(1,5):
                img=utils.load_image(str(n)+str(ind)+'.png',True,'shapes')
                shape.imgs.append(img)
        side=maxw
        if maxh>maxw: side=maxh
        self.colours_xy=(g.sx(.2),g.margin+g.sy(.2))
        self.colours_wh=(g.sy(2.96),g.surf_h/len(colours))
    
    def draw(self):
        for shape in shapes:
            g.screen.blit(shape.img_tn,(shape.x,shape.y))
        x,y=self.colours_xy; w,h=self.colours_wh
        for ind in range(len(colours)):
            pygame.draw.rect(g.screen,colours[ind],(x,y,w,h))
            if ind==g.colour_ind:
                pygame.draw.rect(g.screen,(0,200,0),(x,y,w,h),g.sy(.2))
            y+=h

    def which_shape(self):
        for shape in shapes:
            x=shape.x; y=shape.y; d=g.sy(1.5)
            w=shape.w
            if w<d: x-=(d-w)/2; w=d
            h=shape.h
            if h<d: y-=(d-h)/2; h=d
            if utils.mouse_in(x,y,x+w,y+h):
                g.carry_shape=shape; self.make_carry(); g.carry=True
                return True
        return False

    def which_colour(self):
        x,y=self.colours_xy; w,h=self.colours_wh
        for ind in range(len(colours)):
            if utils.mouse_in(x,y,x+w,y+h):
                g.colour_ind=ind; self.make_carry(); return True
            y+=h
        return False
    
    def rotate(self):
        if g.carry:
            g.angle-=10
            if g.angle==-360: g.angle=0
            self.make_carry()
        
    def make_carry(self):
        shape=g.carry_shape
        ind=random.randint(0,4)
        img=shape.imgs[ind]
        if g.scale<1:
            w=int(img.get_width()*g.scale)
            h=int(img.get_height()*g.scale)
            try:
                img=pygame.transform.smoothscale(img,(w,h))
            except:
                img=pygame.transform.scale(img,(w,h))
        img=utils.colour(img,colours[g.colour_ind])
        if g.angle!=0: img=pygame.transform.rotate(img,g.angle)
        w2=img.get_width()/2; h2=img.get_height()/2
        g.carry_img=img; g.carry_dxy=w2,h2
        
        

        
        
