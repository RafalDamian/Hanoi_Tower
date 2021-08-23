import random as rand
from vpython import *
    

n = 8 #total number of rings

scene = canvas(width = 1000, height = 800, center=vector(10,n/2,0))

l_max = 1.0
l_min = l_max / n + 0.2
dl = (l_max - l_min) / (n-1.0)

l_pillar = cylinder(pos=vector(0 ,0,0), axis=vector(0,1.5*n,0), radius=l_max, 
    texture=textures.wood, rings=[], rings_height = 0)
m_pillar = cylinder(pos=vector(10,0,0), axis=vector(0,1.5*n,0), radius=l_max, 
    texture=textures.wood, rings=[], rings_height = 0)
r_pillar = cylinder(pos=vector(20,0,0), axis=vector(0,1.5*n,0), radius=l_max, 
    texture=textures.wood, rings=[], rings_height = 0)
stand = box(pos=vector(10,-0.5,0), size=vector(30,1,5), texture=textures.wood)

r_max = stand.size.z / 2.0
r_min = l_pillar.radius + l_min
dr = (r_max - r_min) / (n-1.0)

r = r_max #ring radius
l = l_max #ring thickness

for i in range(0, n):    
    y = l_pillar.rings_height + l
    l_pillar.rings_height += 2*l
    l_pillar.rings.append(ring(pos=vector(l_pillar.pos.x,y,0), axis=vec(0,1,0), radius=r, thickness=l,
                      color=vec(rand.uniform(0,1),rand.uniform(0,1),rand.uniform(0,1))))
    r -= dr
    l -= dl

moves = 0
txt_moves = label(pos=vector(10,-5,0), text=f'{moves}/{2**n-1}', height=40, box=False)

if n % 2 == 0:
    move_order = [(l_pillar, m_pillar),(l_pillar, r_pillar),(m_pillar, r_pillar)]   
else:
    move_order = [(l_pillar, r_pillar),(l_pillar, m_pillar),(m_pillar, r_pillar)]
sleep(3)


def make_move(pillar1, pillar2):
    '''makes the only legal move btw 2 pillars'''
    if not pillar2.rings or (pillar1.rings and pillar1.rings[-1].thickness < pillar2.rings[-1].thickness):
        transfer_ring(pillar1, pillar2)   
    else:
        transfer_ring(pillar2, pillar1)

def transfer_ring(pillar1, pillar2):
    '''transfers the top ring from pillar1 to pillar2'''
    pillar2.rings.append(pillar1.rings.pop(-1))
    pillar2.rings[-1].pos.y = pillar2.rings_height + pillar2.rings[-1].thickness
    pillar2.rings[-1].pos.x = pillar2.pos.x
    pillar2.rings_height += 2 * pillar2.rings[-1].thickness
    pillar1.rings_height -= 2 * pillar2.rings[-1].thickness

while True:
    if  not l_pillar.rings and not m_pillar.rings:
        break
    else:
        for (pillar1, pillar2) in move_order:
            make_move(pillar1, pillar2)
            moves += 1
            txt_moves.text = f'{moves}/{2**n-1}'
            sleep(5/n) 
