#!/usr/bin/python
# DidgArt.py 
"""
    Copyright (C) 2011  Peter Hewitt

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

"""
import g,pygame,utils,sys,load_save,buttons,didg
try:
    import gtk
except:
    pass

class DidgArt:

    def __init__(self):
        self.journal=True # set to False if we come in via main()
        self.canvas=None # set to the pygame canvas if we come in via activity.py

    def display(self):
        g.screen.fill((64,64,255))
        self.didg.draw()
        g.screen.blit(g.surf,g.surf_xy)
        buttons.draw()
        utils.text_blit(g.screen,str(g.save_n),g.font2,\
                        self.save_c,utils.ORANGE,True)
        if g.load_n>0:
            utils.text_blit(g.screen,str(g.load_n),g.font2,\
                            self.load_c,utils.CYAN,True)

    def do_click(self,button):
        # load number
        x,y=self.load_c; d=self.load_d
        if utils.mouse_in(x-d,y-d,x+d,y+d):
            if g.load_n!=None:
                if button==1:
                    g.load_n+=1
                    if g.load_n>g.saves_n: g.load_n=1
                if button==3:
                    g.load_n-=1
                    if g.load_n<1: g.load_n=g.saves_n
            return
        # save number
        x,y=self.save_c; d=self.load_d
        if utils.mouse_in(x-d,y-d,x+d,y+d):
            if button==1:
                g.save_n+=1
                if g.save_n>g.saves_n+1: g.save_n=1
            if button==3:
                g.save_n-=1
                if g.save_n<1: g.save_n=g.saves_n+1
            return
        if button==3: self.didg.rotate(); return
        if button==1:
            # shapes
            if self.didg.which_shape(): return
            # colours
            if self.didg.which_colour(): return
            # drawing area
            x,y=g.surf_xy
            if utils.mouse_in(x,y,x+g.surf_w,y+g.surf_h):
                if g.carry:
                    dx=g.carry_img.get_width()/2; dy=g.carry_img.get_height()/2
                    xy=(g.pos[0]-dx-x,g.pos[1]-dy-y)
                    g.surf.blit(g.carry_img,xy)
                    g.redraw=True
                    return
            # nowhere so put down
            g.carry=False

    def do_button(self,bu):
        if bu=='save': load_save.save_surf(); buttons.on('load'); return
        if bu=='load': load_save.load_surf(); return
        if bu=='clear': g.surf.fill(utils.CREAM); return

    def do_key(self,key):
        if key==pygame.K_v: g.version_display=not g.version_display; return
        if key in g.UP:
            ind=g.scales.index(g.scale); ind+=1
            if ind==len(g.scales): ind=0
            g.scale=g.scales[ind]; self.didg.make_carry(); return
        if key in g.DOWN:
            ind=g.scales.index(g.scale); ind-=1
            if ind<0: ind=len(g.scales)-1
            g.scale=g.scales[ind]; self.didg.make_carry(); return
        if key in g.RIGHT:
            if not g.carry:
                ind=0
            else:
                ind=didg.shapes.index(g.carry_shape); ind+=1
                if ind==len(didg.shapes): ind=0
            g.carry_shape=didg.shapes[ind]; self.didg.make_carry(); g.carry=True
            return
        if key in g.LEFT:
            if not g.carry:
                ind=0
            else:
                ind=didg.shapes.index(g.carry_shape); ind-=1
                if ind<0: ind=len(didg.shapes)-1
            g.carry_shape=didg.shapes[ind]; self.didg.make_carry(); g.carry=True
            return
        if key in g.TICK:
            g.colour_ind+=1
            if g.colour_ind==len(didg.colours): g.colour_ind=0
            self.didg.make_carry(); return

    def buttons_setup(self):
        cx=g.sx(30.25); cy=g.sy(6.5); dy=g.sy(2)
        buttons.Button('save',(cx,cy)); cy+=dy
        y1=cy; cy+=2*dy
        buttons.Button('load',(cx,cy)); cy+=dy
        y2=cy; cy+=2*dy
        buttons.Button('clear',(cx,cy)); cy+=dy
        self.save_c=(cx,y1); self.load_c=(cx,y2)
        if g.saves_n==0: buttons.off('load')
        self.load_d=g.sy(.5) # half size of number for clicking

    def flush_queue(self):
        flushing=True
        while flushing:
            flushing=False
            if self.journal:
                while gtk.events_pending(): gtk.main_iteration()
            for event in pygame.event.get(): flushing=True
            
    def carry(self):
        if g.carry:
            if g.carry_save:
                g.screen.blit(g.carry_save,g.carry_xy)
            w=g.carry_img.get_width(); h=g.carry_img.get_height()
            x,y=g.pos; x-=w/2; y-=h/2
            g.carry_save=pygame.Surface((w,h))
            g.carry_save.blit(g.screen,(0,0),(x,y,w,h))
            g.screen.blit(g.carry_img,(x,y))
            g.carry_xy=(x,y)

    def run(self):
        g.init()
        if not self.journal: utils.load()
        self.didg=didg.Didg()
        g.carry_shape=didg.shapes[0]; self.didg.make_carry()
        load_save.retrieve()
        self.buttons_setup()
        if self.canvas<>None: self.canvas.grab_focus()
        ctrl=False
        pygame.key.set_repeat(600,120); key_ms=pygame.time.get_ticks()
        need_carry=False
        going=True
        while going:
            if self.journal:
                # Pump GTK messages.
                while gtk.events_pending(): gtk.main_iteration()

            # Pump PyGame messages.
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    if not self.journal: utils.save()
                    going=False
                elif event.type == pygame.MOUSEMOTION:
                    g.pos=event.pos
                    need_carry=True
                    if self.canvas<>None: self.canvas.grab_focus()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    g.redraw=True
                    if event.button==1:
                        if self.do_click(1):
                            pass
                        else:
                            bu=buttons.check()
                            if bu!='': self.do_button(bu); self.flush_queue()
                    if event.button==3:
                        self.do_click(3)
                elif event.type == pygame.KEYDOWN:
                    # throttle keyboard repeat
                    if pygame.time.get_ticks()-key_ms>110:
                        key_ms=pygame.time.get_ticks()
                        if ctrl:
                            if event.key==pygame.K_q:
                                if not self.journal: utils.save()
                                going=False; break
                            else:
                                ctrl=False
                        if event.key in (pygame.K_LCTRL,pygame.K_RCTRL):
                            ctrl=True; break
                        self.do_key(event.key); g.redraw=True
                        self.flush_queue()
                elif event.type == pygame.KEYUP:
                    ctrl=False
            if not going: break
            if g.redraw:
                g.carry_save=False
                self.display()
                if g.version_display: utils.version_display()
                self.carry()
                need_carry=False
                pygame.display.flip()
                g.redraw=False
            elif need_carry:
                self.carry()
                pygame.display.flip()
                need_carry=False
            g.clock.tick(40)

if __name__=="__main__":
    pygame.init()
    pygame.display.set_mode((1024,768),pygame.FULLSCREEN)
    game=DidgArt()
    game.journal=False
    game.run()
    pygame.display.quit()
    pygame.quit()
    sys.exit(0)
