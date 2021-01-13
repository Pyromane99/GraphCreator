#Package
import pygame as pg
import ctypes
import math
#Fonction utile
def écriture(commentaire,x,y,couleur):
    text=font.render(commentaire,1,couleur)
    win.blit(text,(x,y))

def milieu(a,b):
    c=(abs(a-b))/2
    if a > b:
        return b+c
    if a < b:
        return a+c
    if a==b:
        return a

def cartésien_to_polaire(x,y):
    norme=(x*x+y*y)**0.5
    alpha=math.atan(y/x)
    if x <0 and y <0:
        alpha =alpha + math.pi
    if x<0 and y >=0:
        alpha=alpha +math.pi
    if x>=0 and y <0 :
        alpha =alpha + 2*math.pi
    return norme,alpha

def polaire_to_cartésien(norme,alpha):
    x=norme*math.cos(alpha)
    y=norme*math.sin(alpha)
    return x,y

def draw_flèche(win,x_i,y_i,x_f,y_f,couleur):
    pg.draw.line(win,couleur,(x_i,y_i),(x_f,y_f),largeur_ligne)
    norme,alpha=cartésien_to_polaire(x_f-x_i,y_f-y_i)
    
    x_1,y_1=polaire_to_cartésien(norme-20,alpha)
    sommet=(int(x_i+x_1),int(y_i+y_1))
    
    x_2,y_2=polaire_to_cartésien(norme-40,alpha)
    mediatrice=(int(x_i+x_2),int(y_i+y_2))

    angle=math.atan(largeur_flèche/(norme-40))
    distance=(norme-40)/math.cos(angle)

    x_3,y_3=polaire_to_cartésien(distance,alpha+angle)
    premier_point=(int(x_i+x_3),int(y_i+y_3))

    x_4,y_4=polaire_to_cartésien(distance,alpha-angle)
    second_point=(int(x_i+x_4),int(y_i+y_4))

    pg.draw.polygon(win,couleur,[sommet,premier_point,second_point])

def parralèle(x_i,y_i,x_f,y_f,taille):
    alpha=math.atan((y_f-y_i)/(x_f-x_i))
    x1,y1=polaire_to_cartésien(taille,alpha+(math.pi/2))
    premier_point=(int(x_i+x1),int(y_i+y1))

    x2,y2=polaire_to_cartésien(taille,alpha-(math.pi/2))
    second_point=(int(x_i+x2),int(y_i+y2))
    return premier_point,second_point
def text():
    a=True
    b=""
    while a :
        for event in pg.event.get():
            if event.type==pg.KEYDOWN:
                if event.key==pg.K_KP0 or event.key==pg.K_0:
                    if b !="":
                        b=b+"0"
                if event.key==pg.K_KP1 or event.key==pg.K_1:
                    b=b+"1"
                if event.key==pg.K_KP2 or event.key==pg.K_2:
                    b=b+"2"
                if event.key==pg.K_KP3 or event.key==pg.K_3:
                    b=b+"3"
                if event.key==pg.K_KP4 or event.key==pg.K_4:
                    b=b+"4"
                if event.key==pg.K_KP5 or event.key==pg.K_5:
                    b=b+"5"
                if event.key==pg.K_KP6 or event.key==pg.K_6:
                    b=b+"6"
                if event.key==pg.K_KP7 or event.key==pg.K_7:
                    b=b+"7"
                if event.key==pg.K_KP8 or event.key==pg.K_8:
                    b=b+"8"
                if event.key==pg.K_KP9 or event.key==pg.K_9:
                    b=b+"9"
                if event.key==pg.K_RETURN:
                    return b
def calcul():
    for a in ensemble_noeud:
        a.multiplicité_arête=0
        for b in ensemble_arête:
            if b.noeud_i ==a.nom or b.noeud_f ==a.nom:
                if b.x_i == b.x_f and b.y_i ==b.y_f:
                    a.multiplicité_arête=a.multiplicité_arête+2
                else:
                    a.multiplicité_arête=a.multiplicité_arête+1
    for a in ensemble_noeud:
        a.multiplicité_flèche=0
        for b in ensemble_flèche:
            if b.noeud_i ==a.nom or b.noeud_f ==a.nom:
                if b.x_i == b.x_f and b.y_i ==b.y_f:
                    a.multiplicité_flèche=a.multiplicité_flèche+2
                else:
                    a.multiplicité_flèche=a.multiplicité_flèche+1

def affichage(x,y):
    couleur=(0,0,0)
    écriture("Nombre de noeuds : "+str(len(ensemble_noeud)),x,y,couleur)
    écriture("Nombre d'arêtes : "+str(len(ensemble_arête)),x,y+30,couleur)
    écriture("Nombre de flèches : "+str(len(ensemble_flèche)),x,y+60,couleur)
    b=90
    for a in ensemble_noeud:
        écriture("Multiplicité du noeud "+str(a.nom)+" : "+str(a.multiplicité_arête+a.multiplicité_flèche),x,y+b,couleur)
        b=b+30

def triangle(x,y,couleur):
    sommet=(x,y)
    premier_point=(x-10,y-10)
    second_point=(x-10,y+10)
    pg.draw.polygon(win,couleur,[sommet,premier_point,second_point])
#Classe
class Icone(object):
    def __init__(self,x_c,y_c,couleur,nom,x_e,y_e):
        self.x_c=x_c
        self.y_c=y_c
        self.couleur=couleur
        self.nom=nom
        self.x_e=x_e
        self.y_e=y_e
    def draw(self,win):
        pg.draw.rect(win,self.couleur,(self.x_c,self.y_c,100,100))
        écriture(self.nom,self.x_e,self.y_e,(255,255,255))
    def hitbox(self,x,y):
        return (self.x_c <= x <= self.x_c+100 and self.y_c <= y <= self.y_c +100)

class Noeud(object):
    def __init__(self,x,y,nom):
        self.x=x
        self.y=y
        self.nom=nom
        self.rayon=rayon_noeud
        self.couleur=(0,0,255)
        self.multiplicité_arête=0
        self.multiplicité_flèche=0
    def draw(self,win):
        pg.draw.circle(win,self.couleur,(self.x,self.y),self.rayon)
        écriture(self.nom,self.x-6,self.y-6,(255,255,255))
    def hitbox(self,x,y):
        return (self.x-self.rayon <= x <= self.x+self.rayon and self.y-self.rayon <= y <= self.y+self.rayon)
    def hitbox_elargie(self,x,y):
        return (self.x-2*self.rayon <= x <= self.x+2*self.rayon and self.y-2*self.rayon <= y <= self.y+2*self.rayon)

class Arête(object):
    def __init__(self,x_i,y_i,x_f,y_f,nom):
        self.x_i=x_i
        self.y_i=y_i
        self.x_f=x_f
        self.y_f=y_f
        for a in ensemble_noeud:
            if a.x ==x_i and a.y ==y_i:
                self.noeud_i=a.nom
            if a.x ==x_f and a.y ==y_f:
                self.noeud_f=a.nom
        self.couleur=(0,255,0)
        self.largeur=largeur_ligne
        self.nom=nom
        self.x_milieu=milieu(self.x_i,self.x_f)
        self.y_milieu=milieu(self.y_i,self.y_f)
        self.endroit=20
        self.arête_multiple=False
    def draw(self,win):
        if self.noeud_i != self.noeud_f :
            pg.draw.line(win,self.couleur,(self.x_i,self.y_i),(self.x_f,self.y_f),self.largeur)
            écriture(self.nom,self.x_milieu+self.endroit,self.y_milieu+self.endroit,(0,0,0))
        else:
            pg.draw.arc(win,self.couleur,[self.x_i,self.y_i,2*rayon_noeud,2*rayon_noeud],math.pi,math.pi/2,2)
            écriture(self.nom,self.x_i+40,self.y_i+40,(0,0,0))

class Flèche(object):
    def __init__(self,x_i,y_i,x_f,y_f,nom):
        self.x_i=x_i
        self.y_i=y_i
        self.x_f=x_f
        self.y_f=y_f
        for a in ensemble_noeud:
            if a.x ==x_i and a.y ==y_i:
                self.noeud_i=a.nom
            if a.x ==x_f and a.y ==y_f:
                self.noeud_f=a.nom
        self.couleur=(0,255,0)
        self.largeur=largeur_ligne
        self.nom=nom
        self.x_milieu=milieu(self.x_i,self.x_f)
        self.y_milieu=milieu(self.y_i,self.y_f)
        self.flèche_multiple=False
        self.endroit=20
    def draw(self,win,):
        if self.noeud_i != self.noeud_f :
            draw_flèche(win,self.x_i,self.y_i,self.x_f,self.y_f,self.couleur)
            écriture(self.nom,self.x_milieu+self.endroit,self.y_milieu+self.endroit,(0,0,0))
        else:
            pg.draw.arc(win,self.couleur,[self.x_i,self.y_i,2*rayon_noeud,2*rayon_noeud],math.pi,math.pi/2,2)
            écriture(self.nom,self.x_i+40,self.y_i+40,(0,0,0))
    
#Initialisation
pg.init()

ctypes.windll.user32.SetProcessDPIAware()
true_res = (ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1))
win=pg.display.set_mode(true_res, pg.FULLSCREEN)
pg.display.set_caption("Theory of graph")
win.fill((255,255,255))

#Paramètre
font=pg.font.SysFont('comicsans',25,True)
rayon_noeud=20
largeur_ligne=2
largeur_flèche=10

nom=["Fermer","Noeud","Arête(v)","Flèche(v)","Arête","Flèche","Undo","Clear"]
position_nom=[1850,1850,1840,1835,1850,1850,1860,1855]
couleur=[(255,0,0),(0,0,255),(0,255,0),(0,255,0),(0,255,0),(0,255,0),(100,100,100),(100,100,100)]
ensemble_icone=[]
ensemble_noeud=[]
ensemble_arête=[]
ensemble_flèche=[]
historique=[]
compteur=0
commentaire=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
objet_current_state="Noeud"
x_arête=0
y_arête=0
x_flèche=0
y_flèche=0
def initialisation():
    y=0
    for a in range(8):
        b=Icone(1835,y,couleur[a],nom[a],position_nom[a],y+45)
        b.draw(win)
        ensemble_icone.append(b)
        y+=105
    écriture("Sélection : "+objet_current_state,1625,1000,(0,0,0))
    if objet_current_state=="Noeud":
        triangle(1800,155,(0,0,0))
    elif objet_current_state=="Arête avec valeur":
        triangle(1800,260,(0,0,0))
    elif objet_current_state=="Flèche avec valeur":
        triangle(1800,365,(0,0,0))
    elif objet_current_state=="Arête sans valeur":
        triangle(1800,470,(0,0,0))
    elif objet_current_state=="Flèche sans valeur":
        triangle(1800,575,(0,0,0))

#MainLoop:
condition=True
while(condition):
    #Calcul:
    calcul()
    #Dessin
    win.fill((255,255,255))
    #Quand la souris passe au dessus
    #Arête multiple:
    for a in ensemble_arête:
        for b in ensemble_arête:
            if ensemble_arête.index(a) != ensemble_arête.index(b):
                if (a.noeud_i == b.noeud_i and a.noeud_f == b.noeud_f) or (a.noeud_i == b.noeud_f and a.noeud_f == b.noeud_i):
                    if a.arête_multiple==False and b.arête_multiple==False:
                        initiale_1,initiale_2=parralèle(a.x_i,a.y_i,a.x_f,a.y_f,10)
                        finale_1,finale_2=parralèle(a.x_f,a.y_f,a.x_i,a.y_i,10)
                        a.x_i=initiale_1[0]
                        a.y_i=initiale_1[1]
                        b.x_i=initiale_2[0]
                        b.y_i=initiale_2[1]
                        a.x_f=finale_1[0]
                        a.y_f=finale_1[1]
                        b.x_f=finale_2[0]
                        b.y_f=finale_2[1]
                        a.arête_multiple=True
                        b.arête_multiple=True
                        a.endroit=-20
    #Flèche multiple
    for a in ensemble_flèche:
        for b in ensemble_flèche:
            if ensemble_flèche.index(a) != ensemble_flèche.index(b):
                if (a.noeud_i == b.noeud_i and a.noeud_f == b.noeud_f) or (a.noeud_i == b.noeud_f and a.noeud_f == b.noeud_i):
                    if a.flèche_multiple==False and b.flèche_multiple==False:
                        initiale_1,initiale_2=parralèle(a.x_i,a.y_i,a.x_f,a.y_f,10)
                        finale_1,finale_2=parralèle(a.x_f,a.y_f,a.x_i,a.y_i,10)
                        if a.noeud_i ==b.noeud_i:
                            a.x_i=initiale_1[0]
                            a.y_i=initiale_1[1]
                            b.x_i=initiale_2[0]
                            b.y_i=initiale_2[1]
                            a.x_f=finale_1[0]
                            a.y_f=finale_1[1]
                            b.x_f=finale_2[0]
                            b.y_f=finale_2[1]
                            if abs(a.x_f-a.x_i) > abs(a.y_f-a.y_i):
                                a.endroit=-20
                            else:
                                b.endroit=-20
                        elif a.noeud_i ==b.noeud_f:
                            a.x_i=initiale_1[0]
                            a.y_i=initiale_1[1]
                            b.x_f=initiale_2[0]
                            b.y_f=initiale_2[1]
                            a.x_f=finale_1[0]
                            a.y_f=finale_1[1]
                            b.x_i=finale_2[0]
                            b.y_i=finale_2[1]
                            if abs(a.x_f-a.x_i) > abs(a.y_f-a.y_i):
                                b.endroit=-20
                            else:
                                a.endroit=-20
                        a.flèche_multiple=True
                        b.flèche_multiple=True
    position=pg.mouse.get_pos()
    for a in ensemble_noeud:
        if a.hitbox(position[0],position[1]):
            pg.draw.circle(win,(200,200,200),(a.x,a.y),rayon_noeud+10)
    for a in ensemble_icone:
        if a.hitbox(position[0],position[1]):
            pg.draw.rect(win,(0,0,0),(a.x_c-5,a.y_c-5,110,110))
    if x_arête !=0 and y_arête !=0 :
        pg.draw.line(win,(200,250,200),(x_arête,y_arête),(position[0],position[1]),largeur_ligne)
    if x_flèche !=0 and y_flèche !=0:
        if x_flèche !=position[0] and y_flèche !=position[1]:
            draw_flèche(win,x_flèche,y_flèche,position[0],position[1],(200,250,200))
    #Suite dessin
    initialisation()
    for a in ensemble_arête:
        a.draw(win)
    for a in ensemble_flèche:
        a.draw(win)
    for a in ensemble_noeud:
        a.draw(win)
    affichage(0,200)
    pg.display.update()
    #Action
    for event in pg.event.get():
        if event.type==pg.QUIT:                                                                         #QUITTER
            condition=False
            pg.quit()
        if event.type==pg.KEYDOWN:
            if event.key==pg.K_SPACE:
                pg.image.save(win,"screenshot.jpg")
        if event.type==pg.MOUSEBUTTONDOWN and event.button==1:
            pos=pg.mouse.get_pos()
            if ensemble_icone[0].hitbox(pos[0],pos[1]):                                         #Fermer
                condition=False
                pg.quit()
            elif ensemble_icone[1].hitbox(pos[0],pos[1]):                                       #Noeud
                objet_current_state="Noeud"
                x_arête=0
                y_arête=0
                x_flèche=0
                y_flèche=0
            elif ensemble_icone[2].hitbox(pos[0],pos[1]):                                       #Arête
                objet_current_state="Arête avec valeur"
                x_arête=0
                y_arête=0
                x_flèche=0
                y_flèche=0
            elif ensemble_icone[3].hitbox(pos[0],pos[1]):                                       #Flèche
                objet_current_state="Flèche avec valeur"
                x_arête=0
                y_arête=0
                x_flèche=0
                y_flèche=0
            elif ensemble_icone[4].hitbox(pos[0],pos[1]):                                       #Arête sans chiffre
                objet_current_state="Arête sans valeur"
                x_arête=0
                y_arête=0
                x_flèche=0
                y_flèche=0
            elif ensemble_icone[5].hitbox(pos[0],pos[1]):                                       #Flèche sans chiffre
                objet_current_state="Flèche sans valeur"
                x_arête=0
                y_arête=0
                x_flèche=0
                y_flèche=0
            elif ensemble_icone[6].hitbox(pos[0],pos[1]) :           #Undo
                if historique == []:
                    continue;
                if historique[-1]=="Noeud":
                    del ensemble_noeud[-1]
                    compteur=compteur-1
                elif historique[-1]=="Arête":
                    del ensemble_arête[-1]
                elif historique[-1]=="Flèche":
                    del ensemble_flèche[-1]
                del historique[-1]
            elif ensemble_icone[7].hitbox(pos[0],pos[1]):                                       #Clear
                ensemble_noeud=[]
                ensemble_arête=[]
                ensemble_flèche=[]
                historique=[]
                compteur=0
            else:
                okay=True
                if objet_current_state=="Noeud":                                                    #Dessin Noeud
                        okay=True
                for a in ensemble_noeud:
                    if a.hitbox_elargie(pos[0],pos[1]):
                        okay=False
                if okay==True:
                    noeud=Noeud(pos[0],pos[1],commentaire[compteur])
                    ensemble_noeud.append(noeud)
                    historique.append("Noeud")
                    compteur=compteur+1
                if objet_current_state=="Arête avec valeur" or objet_current_state=="Arête sans valeur":                   #Dessin Arête
                    for a in ensemble_noeud :
                        if a.hitbox(pos[0],pos[1]):
                            if x_arête ==0 and y_arête ==0 :
                                x_arête=a.x
                                y_arête=a.y
                            else:
                                truc=""
                                if objet_current_state=="Arête avec valeur":
                                    écriture("Ecriver la valeur de l'arête puis appuyez sur ENTER",100,100,(0,0,0))
                                    pg.display.update()
                                    truc=text()
                                arête=Arête(x_arête,y_arête,a.x,a.y,truc)
                                ensemble_arête.append(arête)
                                historique.append("Arête")
                                x_arête=0
                                y_arête=0
                if objet_current_state=="Flèche avec valeur" or objet_current_state=="Flèche sans valeur":                 #Dessin Flèche
                    for a in ensemble_noeud :
                        if a.hitbox(pos[0],pos[1]):
                            if x_flèche ==0 and y_flèche ==0 :
                                x_flèche=a.x
                                y_flèche=a.y
                            else:
                                truc=""
                                if objet_current_state=="Flèche avec valeur":
                                    écriture("Ecriver la valeur de la flèche puis appuyez sur ENTER",100,100,(0,0,0))
                                    pg.display.update()
                                    truc=text()
                                flèche=Flèche(x_flèche,y_flèche,a.x,a.y,truc)
                                ensemble_flèche.append(flèche)
                                historique.append("Flèche")
                                x_flèche=0
                                y_flèche=0
                        
