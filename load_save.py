#load_save.py
import g,pygame,os

loaded=[] # list of strings

def load(f):
    global loaded
    try:
        for line in f.readlines():
            loaded.append(line)
    except:
        pass

def save(f):
    f.write(str(g.saves_n)+'\n')
        
def retrieve():
    global loaded # ignored - gonna count the files instead :o)
    g.saves_n=0; g.load_n=0
    for filename in os.listdir('saves'):
        if filename!='empty': g.saves_n+=1
    g.save_n=g.saves_n+1
    if g.saves_n>0: g.load_n=1

def save_surf():
    fname=str(g.save_n)
    if g.save_n>g.saves_n: g.saves_n=g.save_n # new one
    pygame.image.save(g.surf,os.path.join('saves',fname+'.png'))
    g.load_n=g.save_n

def load_surf():
    fname=str(g.load_n)
    g.surf=pygame.image.load(os.path.join('saves',fname+'.png'))
    g.save_n=g.load_n


    
