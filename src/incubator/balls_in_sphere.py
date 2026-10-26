# Web VPython 3.2

# https://glowscript.org/#/user/priisdk/folder/ballsinsphere/program/particlesinsphere2/edit


#
vhist=gdisplay(title='Speed distribution',x=1100,y=0,width=250,height=250,ymin=0,ymax=10)
#speeds = ghistogram(gdisplay=vhist,bins=arange(0,10,0.2), color=color.red,average=True,accumulate=True)# title='Speed distribution',
bmdist= gcurve(gdisplay=vhist, color=color.green)

vaverage=2
sigma=sqrt(pi/2)*vaverage/2

def fbm(x):
    return 40*sqrt(2/pi)*x*x*exp(-x*x/sigma/sigma/2)/2/sigma/sigma/sigma

xybm=[]

for i in range(0,101):
    xybm.append((i/10,fbm(i/10)))
bmdist.plot(pos=xybm)
#seed()

    
animation = display(title='Vpython-demo', x=0, y=0, width=1200, height=800, center=vec(0, 0, 0), background=color.black)

phig=(3-sqrt(5))*pi
#Magic numbers: 2, 8, 20, 28, 50, 82, and 126



R=1
inucleus=0

#nucleusframe=[]

#for i in range(0,4):
#    nucleusframe.append(frame())


def f(t):
    return 2*sqrt(t*(1-t))*R

#Nnucleons=238
#Nprotons=92



#print('Ntriples=',Ntriples)
#print('Ndoubles=',Ndoubles)
#npratio=Nneutrons/Nprotons

Nnucleons=120
Nprotons=60

rnucleon=0.5*R
dnucleon=2*rnucleon
dshell=2*R
opacityvalue=1

nucleons=[]
nucleonspeed=[]
farvearray=[]
Nneutrons=Nnucleons-Nprotons
Ntriples=Nnucleons-2*Nprotons
Ndoubles=3*Nprotons-Nnucleons

iprotons=0
ineutrons=0

"""
for i in range(0,Ndoubles):
    farvearray.append(color.red)
    iprotons=iprotons+1
    farvearray.append(color.green)
    ineutrons=ineutrons+1
for i in range(0,Ntriples):
    farvearray.append(color.green)
    ineutrons=ineutrons+1

    farvearray.append(color.green)
    ineutrons=ineutrons+1
    farvearray.append(color.red)
    iprotons=iprotons+1
shuffle(farvearray)
"""
#print('ineutrons=',ineutrons)
#print('iprotons=',iprotons)
#farvearray[0]=color.blue



"""
for i in range(0,Nprotons):
    farvearray.append(color.red)

for i in range(Nprotons,Nnucleons):
    farvearray.append(color.blue)

for i in range(0,Nneutrons):
    skift=randint(0,1)
    if skift==1:
        j=Nnucleons-i-1
        farve1=farvearray[i]
        #farve2=farvearray[j]
        farvearray[i]=farvearray[j]
        farvearray[j]=farve1
"""
for i in range(0,Nnucleons):
    farvearray.append(color.hsv_to_rgb(vec(i/Nnucleons,1,1)))
print('farvearray=',farvearray)
    
if Nnucleons<4:
    N=Nnucleons
else:
    N=4
   
for i in range(0,N):  
    t=(i+1)/(N+1)
    if t>0.5:
        fortegn=-1
    else:
        fortegn=1
    print('farvearray[i+4]=',farvearray[i+4])
    nucleons.append(sphere(pos=vec(f(t)*cos(i*phig),f(t)*sin(i*phig),fortegn*sqrt(R**2-f(t)**2)),
                               radius=rnucleon,color=farvearray[i+4],opacity=opacityvalue,texture=textures.metal))
                               
        
"""
    if i%2==0:
        farve=color.red
    else:
        farve=color.blue
"""
    
    

if Nnucleons>4:
    if Nnucleons<40:
        N=Nnucleons-4
    else:
        N=36
    R=R+dshell
    for i in range(0,N):
        t=(i+1)/(N+1)
        if t>0.5:
            fortegn=-1
        else:
            fortegn=1
        #sphere(pos=(sin(pi*t)*cos(i*phig),sin(pi*t)*sin(i*phig),cos(pi*t)),radius=0.1,color=color.blue)
        nucleons.append(sphere(pos=vec(f(t)*cos(i*phig),f(t)*sin(i*phig),fortegn*sqrt(R**2-f(t)**2)),
                               radius=rnucleon,color=farvearray[i+4],opacity=opacityvalue,texture=textures.metal))

    if Nnucleons>36:
        if Nnucleons<140:
            N=Nnucleons-36-4
        else:
            N=100
        R=R+dshell
        for i in range(0,N):
            t=(i+1)/(N+1)
            if t>0.5:
                fortegn=-1
            else:
                fortegn=1
            #sphere(pos=(sin(pi*t)*cos(i*phig),sin(pi*t)*sin(i*phig),cos(pi*t)),radius=0.1,color=color.blue)
            nucleons.append(sphere(pos=vec(f(t)*cos(i*phig),f(t)*sin(i*phig),fortegn*sqrt(R**2-f(t)**2)),
                                   radius=rnucleon,color=farvearray[i+36],opacity=opacityvalue,texture=textures.metal))
        if Nnucleons>100:
            if Nnucleons<336:
                N=Nnucleons-100-36-4
            else:
                N=196
            #N=Nnucleons-4-16-64
            R=R+dshell
            for i in range(0,N):
                t=(i+1)/(N+1)
                if t>0.5:
                    fortegn=-1
                else:
                    fortegn=1
                #sphere(pos=(sin(pi*t)*cos(i*phig),sin(pi*t)*sin(i*phig),cos(pi*t)),radius=0.1,color=color.blue)
                nucleons.append(sphere(pos=vec(f(t)*cos(i*phig),f(t)*sin(i*phig),fortegn*sqrt(R**2-f(t)**2)),
                                       radius=rnucleon,color=farvearray[i+100],opacity=opacityvalue,texture=textures.plastic))
inucleus=inucleus+1
R=1



kv=1
for i in range(0,len(nucleons)):
    nucleons[i].velocity=kv*vector(log(1-random()),log(1-random()),log(1-random()))
    #nucleons[i].vy=kv*log(1-random())
    #nucleons[i].vz=kv*log(1-random())
#print(nucleons[0].vx,nucleons[0].vy,nucleons[0].vz)
#print(vx,vy,vz)
for i in range(0,len(nucleons)):
    nucleonspeed.append(mag(nucleons[i].velocity))

#speeds.plot(data=nucleonspeed)

Rvessel=10*R
#Rvessel=4*R
rmax=Rvessel-rnucleon
vessel=sphere(pos=vec(0,0,0),radius=Rvessel,color=color.green, texture=textures.metal,opacity=0.15)
vesselring1=ring(pos=vec(0,0,0),axis=vec(1,0,0),radius=Rvessel,thickness=0.005*Rvessel,color=color.yellow, texture=textures.metal,opacity=0.25)
vesselring2=ring(pos=vec(0,0,0),axis=vec(0,1,0),radius=Rvessel,thickness=0.005*Rvessel,color=color.yellow, texture=textures.metal,opacity=0.25)
vesselring3=ring(pos=vec(0,0,0),axis=vec(0,0,1),radius=Rvessel,thickness=0.005*Rvessel,color=color.yellow, texture=textures.metal,opacity=0.25)
dt=0.02
t=0
ncalc=0
for i in range(0,Nnucleons):
    print(nucleons[i].pos)

while True:
    ncalc=ncalc+1
    #rate(2000)
    rate(200)
    t=t+dt
    for i in range(0,Nnucleons):
        newposi=nucleons[i].pos+dt*nucleons[i].velocity
        if mag(newposi)>=rmax:
            #nucleons[i].velocity=nucleons[i].velocity-2*dot(nucleons[i].pos,nucleons[i].velocity)/dot(nucleons[i].pos,nucleons[i].pos)*nucleons[i].pos
            #nucleons[i].velocity=nucleons[i].velocity-2*vdot(nucleons[i].pos,nucleons[i].velocity)/vdot(nucleons[i].pos,nucleons[i].pos)*nucleons[i].pos
            #nucleons[i].velocity=nucleons[i].velocity-2*dot(nucleons[i].pos,nucleons[i].velocity)/mag2(nucleons[i].pos)*nucleons[i].pos
            nucleons[i].velocity=nucleons[i].velocity-2*proj(nucleons[i].velocity,nucleons[i].pos)
        
        #else:
        #nucleons[i].pos=newpos
        for j in range(0,i):
            newposj=nucleons[j].pos+dt*nucleons[j].velocity
            dist=mag(newposi-newposj)
            if dist<dnucleon:
                vcms=(nucleons[j].velocity+nucleons[i].velocity)/2
                u1=(nucleons[j].velocity-nucleons[i].velocity)/2
                u2=-u1
                rrel=nucleons[j].pos-nucleons[i].pos
                vrel=2*u2
                ivec=norm(u1)
                kvec=norm(cross(rrel,u1))
                jvec=cross(kvec,ivec)
                sinphi=mag(rrel-proj(rrel,vrel))/rnucleon/2
                cos2phi=1-2*sinphi*sinphi
                sin2phi=2*sinphi*sqrt(1-sinphi*sinphi)
                u=u1.mag
                u1hat=u*(cos2phi*ivec+sin2phi*jvec)
                u2hat=-u1hat
                #print(mag2(nucleons[i].velocity)+mag2(nucleons[j].velocity))
                nucleons[i].velocity=u1hat+vcms
                nucleons[j].velocity=u2hat+vcms
                #print(mag2(nucleons[i].velocity)+mag2(nucleons[j].velocity))
                #print()
                
                #vj=nucleons[j].velocity
                #nucleons[j].velocity=nucleons[i].velocity
                #nucleons[i].velocity=vj
 

                #nucleons[i].pos=nucleons[i].pos+dt*nucleons[i].velocity
                #nucleons[j].pos=nucleons[j].pos+dt*nucleons[j].velocity
        nucleons[i].pos=nucleons[i].pos+dt*nucleons[i].velocity
    if ncalc%100==0:
        nucleonspeed=[]
        for ii in range(0,len(nucleons)):
            nucleonspeed.append(mag(nucleons[ii].velocity))
        #speeds.plot(data=nucleonspeed)
        #for i in range(0,len(xybm)):
        #    xybm[i]=(xybm[i][0],2*xybm[i][1])
        #bmdist.pos=xybm

"""
    v1x=-(v1-V)*cos(2*phi)+V
    v1y=-(v1-V)*sin(2*phi)
    v2x=V*cos(2*phi)+V
    v2y=V*sin(2*phi)
    x02=R12*cos(phi)
    y02=R12*sin(phi)
"""

     



     #nucleons[i].pos=newpos


