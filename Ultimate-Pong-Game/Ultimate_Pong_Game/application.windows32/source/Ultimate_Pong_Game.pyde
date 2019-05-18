"""======================== Version 1.8.5 ==========================="""
"""
-------- Instructions de lancement avec Minim --------
Veuillez installer minim avant de lancer le programme...
Pour cela, allez dans l'onglet outil/ajouter un outil.../Libraries
puis installez le... 

------------------------------------------------------
lien de téléchargement direct:
https://github.com/Darkmauros/Ultimate-Pong-Game/archive/master.zip

------------------------------------------------------
Pour décocher les boutons du menu option, il faut faire un clic gauche

"""
import time
import json #merci à ce module <3
add_library('minim')
global minim
minim = Minim(this)
#from Balle import *
"""================= Liste des choses à faire =====================
-bot
-murs
-magasin pong et plaque 
-class bouton
-pièces (bitcoin)
-nouveaux mods:
    bonus/malus
    bot
============================================================"""
#---------------- Pour le mode hardcore -----------------------
def difficulty(value,valueAdd):
    if boutonHardcore == True:
        value += valueAdd
    return value
#------------------ lecture d'un fichier JSON
def lectureDeFichier():
    global texteLu
    #--- lecture du fichier
    try:
        with open("data/info.JSON","r") as f:
            texteLu = f.read()
            #print(texteLu)
        #--- écrasement du dictionnaire
        dictionnaireInfo = json.loads(texteLu)
        
        global optionSon,optionMusique,boutonHardcore,optionPortails,optionPortails,optionForceField,optionBlackHole,optionBoss1
        global optionBoss2, optionNuage, nombreBalle, optionBonus, optionRainbow, optionDocteur 
        
        optionSon = dictionnaireInfo["optionSon"]
        optionMusique = dictionnaireInfo["optionMusique"]
        boutonHardcore = dictionnaireInfo["boutonHardcore"]
        optionPortails = dictionnaireInfo["optionPortails"]
        optionForceField = dictionnaireInfo["optionForceField"]
        optionBlackHole = dictionnaireInfo["optionBlackHole"]
        optionBoss1 = dictionnaireInfo["ptionBoss1"]
        optionBoss2 = dictionnaireInfo["optionBoss2"]
        optionNuage = dictionnaireInfo["optionNuage"]
        nombreBalle = dictionnaireInfo["nombreBalle"]
        optionBonus = dictionnaireInfo["optionBonus"]
        optionRainbow = dictionnaireInfo["optionRainbow"]
        optionDocteur = dictionnaireInfo["optionDocteur"]
    except:
        optionSon = True
        optionMusique = True
        boutonHardcore = False
        optionPortails = False
        optionForceField = False
        optionBlackHole = False
        optionBoss1 = False
        optionBoss2 = False
        optionNuage = False
        nombreBalle = 1
        optionBonus = False
        optionRainbow = False
        optionDocteur = False
        print 'un probleme est survenu lors de la lecture des sauvegardes'
#-------------------- Quelques variables importantes ------------------
#Balles Rouges/Vitesse de base et vitesse max + grande/Plaque plus petite/Score x2

lectureDeFichier()

"""
#le dictionnaire qui sera écrit en JSON (à n'utiliser que si le dictionnaireInfo est vide)
dictionnaireInfo = {"optionSon" : True, "optionMusique" : True,"boutonHardcore" : False, "optionPortails" : False,
                    "optionForceField" : False,"optionBlackHole" : False ,"optionBoss1" : False,"optionBoss2" : False,
                    "optionNuage" : False,"nombreBalle" : 1}
"""
menuVar = "menue"
optionDebug = False
showVecteurs = False
listeTrail = []
backR = 20
backV = 150
backB = 240
rainbowR = int(random(2,8))
rainbowV = int(random(2,8))
rainbowB = int(random(2,8))
fps = False
#------------------------------- Classe de la Plaque ----------------------------------
class Plaque:
    def __init__ (self, positionX = 40,joueur = 1):
        self.positionX = positionX
        self.positionY = 300
        self.joueur = joueur 
        self.hp = difficulty(20,-15)#pour baisser la vie en hardcore
        self.hauteur = (difficulty(130,-50)) #à remettre à 130,-50 après les tests 
        self.largeur = 20
        self.alive = True
        self.vitesse = 20
        self.vitesseKeyboard = 0
        
    def display(self):
        fill(255-self.hp*15.5 ,self.hp*15.5, 0)#passer du vert au rouge en fonction des HP
        if optionRainbow == True:
            fill(255-self.hp*15.5 +backV,self.hp*15.5- backB, backR)#des couleurs un peu au hasard
        rect(self.positionX ,self.positionY - self.hauteur/2 ,self.largeur, self.hauteur,7)

    def update(self):
        if self.hp < difficulty(20,-4): #pour limiter le max de regen
            self.hp += difficulty(0.005,-0.001) #pour donner une petite regen
            
        #------- déplacement plaque 
        #pour le joueur à la souris
        if self.joueur == 1:
            if self.positionY > mouseY:
                move = mouseY - self.positionY
                if move < self.vitesse:# limite de vitesse
                    move = self.vitesse
                self.positionY -= move
            if self.positionY < mouseY:
                move = mouseY - self.positionY
                if move > self.vitesse:# limite de vitesse
                    move = self.vitesse
                self.positionY += move
        #pour le joueur au clavier                
        if self.joueur == 2:
            keyIndex = 0
            keyIndex = keyCode
            if keyPressed == True:
                if keyIndex == 38: #flèche du haut
                    self.vitesseKeyboard -= 1.5
                    if self.vitesseKeyboard < -self.vitesse:#limite de vitesse
                        self.vitesseKeyboard = -self.vitesse
                elif keyIndex == 40: #flèche du bas     
                    self.vitesseKeyboard += 1.5
            else:
                self.vitesseKeyboard = 0 # pour permettre de stopper la plaque
            if self.vitesseKeyboard > self.vitesse: #limite de vitesse
                self.vitesseKeyboard = self.vitesse
            self.positionY += self.vitesseKeyboard 
        #-- pour ne pas dépasser les bords
        if self.positionY > height- self.hauteur/2:
            self.positionY = height- self.hauteur/2
        if self.positionY < self.hauteur/2:
            self.positionY = self.hauteur/2
        #--- destruction de la plaque
        if self.hp <= 0:
            self.alive = False
#---------------- trail de la balle en mode rainbow
class trail:
    def __init__(self, vecteurPosition):
        self.alive = True
        self.b = 100
        self.bt = 10
        self.taille = 35
        self.vecteurPosition = vecteurPosition
    
    def display (self):
        noStroke()
        fill (self.vecteurPosition.y/2.75 , self.vecteurPosition.x/3.52 , self.b )
        ellipse(self.vecteurPosition.x , self.vecteurPosition.y  , self.taille , self.taille)

    def update (self):
        self.taille = self.taille - 1
        if self.taille == 0:
            self.alive = False
        self.b = self.b+ self.bt
        if self.b >= 255 or self.b <= 0 :
            self.bt = -self.bt
            
#---------------------- Scaphandre de sauvetage pour la neurotoxine du Boss1 OSU ---------------
class Scaph:
    def __init__(self) :
        self.sauvetage = False
        self.positionX = mouseX
        self.positionY = mouseY
        self.diametre = 70
    
    def display(self):
        fill(0,255,0,150)
        ellipse(self.positionX - self.diametre/2, self.positionY - self.diametre/2, self.diametre, self.diametre)
        
    def aie(self):
        fill(255,0,0,150)
        ellipse(self.positionX - self.diametre/2, self.positionY - self.diametre/2, self.diametre, self.diametre)
        
    def update(self):
        self.positionX = mouseX
        self.positionY = mouseY
#----------------------- Neurotoxine du Boss1 --------------------
class Neuro:
    def __init__(self) :
        self.degats = False
        self.alive = True
        self.framecount = 1
        self.framecountB = 0
        self.framecountV = 0
        self.hauteur = 500
        self.largeur = 500
        self.positionX = width/2
        self.positionY = height/2
        
    def update(self):
        pass
        """
        self.positionX = mouseX
        self.positionY = mouseY
        """
    def frameUpdate(self):
        self.framecountB += 1
        if self.framecountB >= 5:
            self.framecount += 1
            self.framecountB = 0
        if self.framecount >= 4:
            self.framecountV +=1
            self.framecount = 1
        if self.framecountV == 5:
            self.framecountV = 0
            self.alive = False
            
    def display(self):
        a = imgNeuro[self.framecount]
        tint(255,150)
        image(a , self.positionX - self.hauteur/2 ,self.positionY - self.largeur/2 ,self.hauteur ,self.largeur)
        noTint()
        
#-------------------------------- Missile du Boss ---------------------------------------
class Missile:
    def __init__(self):
        self.degats = 1
        self.alive = True
        self.angle = random(135,225)
        self.vecteurPosition = PVector(width/1.7 , 400)
        self.vecteurVitesse = PVector(0, 0)
        self.vecteurAcceleration = PVector(0, 0)
    
    def display(self):#affichage
        fill(255,0,0)
        with pushMatrix():
            translate (self.vecteurPosition.x, self.vecteurPosition.y)
            rotate(radians(self.angle))
            image(imgMissile,-120,-30,120,34)#120x34
            #print(self.angle)

    def reset(self):
        v = 9
        x = v*cos(radians(self.angle)) 
        y = sin(radians(self.angle))*v
       
        self.vecteurVitesse = PVector(x , y)
        
    def update(self):
        self.vecteurPosition.add(self.vecteurVitesse)
        self.vecteurVitesse.add(self.vecteurAcceleration)
        self.vecteurAcceleration = PVector(0,0)
#----------------------- Boss - GLaDOS -------------------------------
class GLaDOS:
    def __init__(self):
        self.hp = 100
        self.phase = 1
        self.dammage = False
        self.framecount = 1
        self.dammageFramecount = 0
        self.alive = True
        self.timerA = 0
        self.timerB = 0
        self.timerC = 0
        self.N = 0
        self.L = 0
        self.M = 0
        
    def Time(self):
        self.timerA +=1
        if self.timerA <= 99:
            self.M = 0
        if self.timerB <= 1:
            self.N = 0
        if self.timerC <= 49:
            self.L = 0
        if self.timerA == 100:
            self.M = 1
            self.timerA = 0
            self.timerB += 1
            if self.timerB == 2:
                self.N = 1
                self.timerB = 0
                self.timerC +=1
        
    def display(self):#affichage et hitbox et vie
        global menuVar
        #rect(width/1.35, 0 , 200 , 400) hitbox 1
        #rect(width/1.65 , height/2.05, 370 , 155) hitbox 2
        #rect(width/1.65 , 500 , width , height) hitbox 3
        if self.alive == True :
            image(imgPlateforme, width/1.65 , 500 , 200, 200)
            if self.dammage == True:
                self.dammageFramecount +=1
                if self.dammageFramecount > 20: #temps en "tic" avant de modifié la variable tampon
                    self.dammageFramecount = 0
                    self.dammage = False
            if self.dammage == True:
                a = imgGLaDOS2
            else:
                a = imgGLaDOS1
                
            image(a, width/1.7, 0 , 412, 500)#dimension de base du png (412x500)pixels
            #------------------- barre de vie -------------------------
        #self.hp varie de 100 à 0
        fill(255-self.hp*2.55 ,self.hp*2.55, 0) #à revoir pour passer du vert au rouge
        noStroke()
        rect(width/5 , height/1.1 , self.hp*5 , 30,10)
        stroke
        #----------------- Mise en route phase 2 + mort du boss -------------
        if Boss.hp <= 50:
            Boss.phase = 2
        if Boss.hp <= 0:
            Boss.alive = False
            menuVar = "Win1"
            if optionMusique == True:
                musiqueStop()
            if optionSon == True:
                r = int(random(0,2))
                if r == 0:
                    PunchlineW1.play()
                    PunchlineW1.setGain(-10)
                    PunchlineW1.rewind()
                else:
                    PunchlineW2.play()
                    PunchlineW2.setGain(-10)
                    PunchlineW2.rewind()
#----------------------- Les Noxines ,les machines de Nox ----------------------
class Noxine:
    def __init__(self,vecteurVitesse = PVector(15,0) ,vecteurAcceleration = PVector(-0.3,0), focus = "left"):
        self.alive = True
        self.vecteurPosition = PVector(width/1.8,height/2.5)
        self.vecteurVitesse = vecteurVitesse
        self.vecteurAcceleration = vecteurAcceleration
        self.framecount = 1
        self.framecountBis = 0
        self.angle = "droite"
        self.focus = focus #il ne peut être à droite qu'en multi
        self.vitesseMaxG = 7
        self.explosionFramecount = 1
        self.explosionFramecountBis = 0
        self.explosion = False
        
    def display(self):
        if self.angle == "gauche":
            a = imgNoxineG[self.framecount]
        else:
            a = imgNoxineD[self.framecount]
        image(a,self.vecteurPosition.x- 50 ,self.vecteurPosition.y-50, 100,100)    
    #framecount sert à montrer les images et framecountBis sert à ralentir le framecount
    def update(self):
        #------- pour changer le sens de la noxine
        if self.vecteurVitesse.x < 0:
            self.angle = "gauche"
        else:
            self.angle = "droite"
        #------- pour la faire suivre la plaque
        if self.focus == "left":
            if P1.positionY > self.vecteurPosition.y:
                self.vecteurAcceleration.y = 0.2
            else:
                self.vecteurAcceleration.y = -0.2
        if self.focus == "right":
            if P2.positionY > self.vecteurPosition.y:
                self.vecteurAcceleration.y = 0.2
            else:
                self.vecteurAcceleration.y = -0.2
        #--------- pour éviter que la noxine aille trop vite à gauche ou à droite
        if self.vecteurVitesse.x < -self.vitesseMaxG:#gauche
            self.vecteurVitesse.x = -self.vitesseMaxG
        if self.vecteurVitesse.x > self.vitesseMaxG:#droite
            self.vecteurVitesse.x = self.vitesseMaxG
        #--------- update des vecteurs
        self.vecteurPosition.add(self.vecteurVitesse)
        self.vecteurVitesse.add(self.vecteurAcceleration)
        
    def frameUpdate(self):
        self.framecountBis += 1
        if self.framecountBis >= 5:
            self.framecount += 1
            self.framecountBis = 0
        if self.framecount >= 3:
            self.framecount = 1
            
    def explose(self):
        #---- boom
        if self.explosionFramecount == 1 and optionSon == True:
            nombreRandom = int(random(1,4)) # pour avoir un nombre entre 1 et 3
            if nombreRandom == 1:
                sonBoom1.play()
                sonBoom1.rewind()
            elif nombreRandom == 2:
                sonBoom1.play()
                sonBoom1.rewind()
            elif nombreRandom == 3:
                sonBoom1.play()
                sonBoom1.rewind()
            else:
                pass
        #---- framecount de l'animation
        self.explosionFramecountBis += 1
        if self.explosionFramecountBis >= 7:
            self.explosionFramecount += 1
            self.explosionFramecountBis = 0
        self.alive = False
        #--- explosion quand la noxine arrive à gauche
        """if self.vecteurPosition.y < P1.positionY + P1.hauteur+10 and self.vecteurPosition.y > P1.positionY - P1.hauteur-10:
            self.explosion = True"""
        #----destruction Plaque
        if self.explosionFramecount >= 3 and self.explosionFramecount <= 8:
            #calcul de norme : sqrt((Xb-Xa)**2+(Yb-Ya)**2)   __(avec la plaque pour B)
            if sqrt((P1.positionX-self.vecteurPosition.x)**2+(P1.positionY-self.vecteurPosition.y)**2) < ((85 + P1.hauteur/2) or (85- P1.hauteur/2)):
                P1.hp -= 0.2
            if menuVar == "pongMulti":
                if sqrt((P2.positionX-self.vecteurPosition.x)**2+(P2.positionY-self.vecteurPosition.y)**2) < ((85 + P2.hauteur/2) or (85- P2.hauteur/2)):
                    P2.hp -= 0.2
        if self.explosionFramecount >= 12:
            self.explosion = False
        image((imgExplosionBleu[self.explosionFramecount]),self.vecteurPosition.x-90 ,self.vecteurPosition.y-90, 180,180)
#-------------------------------------- NOX --------------------------------------
class Nox:
    def __init__(self):
        self.alive = True
        self.framecount = 1
        self.framecountBis = 0
        self.frameSpell = 0
        self.frameMegaSpell = 0
        self.spell = "none"
        self.used = "none"
        self.animationSpellFrame = 1
        self.animationSpellFrameBis = 0
        self.animationSpell = False
        
    def frameUpdate(self):
        #framecount sert à montrer les images et framecountBis sert à ralentir le framecount
        self.framecountBis += 1
        if self.framecountBis >= 7:
            self.framecount += 1
            self.framecountBis = 0
        if self.framecount >= 19:
            self.framecount = 1
        self.frameSpell += 1

        #---------- pour lancer un sort au hasard  
        if self.frameSpell >= 380: # temps en frame pour lancer un sort
            self.frameMegaSpell += 1
            if self.frameMegaSpell >= 4:
                #--- Nuée de Noxines
                #RAPPEL: class Noxine(self, vecteurVitesse, vecteurAcceleration,focus = "left")
                listeNoxines.append(Noxine(PVector(11,0),PVector(-0.3,0)))
                listeNoxines.append(Noxine(PVector(16,6),PVector(-0.3,0)))
                listeNoxines.append(Noxine(PVector(8,-8),PVector(-0.2,0)))
                listeNoxines.append(Noxine(PVector(3,0),PVector(-0.1,0)))
                listeNoxines.append(Noxine(PVector(25,-5),PVector(-0.3,0)))
                listeNoxines.append(Noxine(PVector(29,5),PVector(-0.3,0)))
                if menuVar == "pongMulti":
                    listeNoxines.append(Noxine(PVector(-11,0),PVector(0.3,0),"right"))
                    listeNoxines.append(Noxine(PVector(-16,6),PVector(0.3,0),"right"))
                    listeNoxines.append(Noxine(PVector(-8,-8),PVector(0.2,0),"right"))
                    listeNoxines.append(Noxine(PVector(-3,0),PVector(0.1,0),"right"))
                    listeNoxines.append(Noxine(PVector(-25,-5),PVector(0.3,0),"right"))
                    listeNoxines.append(Noxine(PVector(-29,5),PVector(0.3,0),"right"))
                self.frameMegaSpell = 0
            elif self.spell == "none":
                nombreRandom = int(random(1,7))#pour avoir un nombre random entre 1 et 6  (1,7)
                #nombreRandom = 1
                if nombreRandom == 1:
                    self.spell = "slow"
                if nombreRandom == 2:
                    self.spell = "acceleration"
                if nombreRandom == 3:
                    self.spell = "stop"
                    self.used = "stop"
                if nombreRandom == 4:
                    listeNoxines.append(Noxine(PVector(20,-3),PVector(-0.3,0)))
                    listeNoxines.append(Noxine(PVector(9,6),PVector(-0.3,0)))
                    if menuVar == "pongMulti":
                        listeNoxines.append(Noxine(PVector(-10,6),PVector(0.3,0),"right"))
                        listeNoxines.append(Noxine(PVector(-25,-3),PVector(0.3,0),"right"))
                if nombreRandom == 5:
                    self.spell = "tp"
                    self.used = "tp"
                if nombreRandom == 6:
                    self.spell = "reverse"
                self.frameSpell = 0
                print(self.spell)
        #-------- pour lancer une animation (le temps doit être un peu moins que pour lancer un sort)
        if self.frameSpell == 360:
            self.animationSpell = True
        #-------- jouer l'animation
        if self.animationSpell == True:
            self.animationSpellFrameBis += 1
            if self.animationSpellFrameBis >= 3:
                self.animationSpellFrame += 1
                self.animationSpellFrameBis = 0
            if self.animationSpellFrame >= 9:
                self.animationSpellFrame = 1
                self.animationSpell = False
    def display(self):
        image((imgNox[self.framecount]), width -800 ,height -621, 678,621)# 678 x 621
        if self.animationSpell == True:
            image((imgSpell[self.animationSpellFrame]),0 ,0,900,700)        
#------------------------------------ Champs de force -----------------------------------
class ForceField:
    def __init__(self):
        self.positionX = int(random(150,width-200))
        self.framecount = 1
        self.sens = "up"
        
    def update(self):
        self.framecount += 1
        if self.framecount >= 42:
            self.framecount = 1
        self.display()
    def display(self):
        tint(255,150)
        if self.sens == "down":
            with pushMatrix():
                translate(self.positionX,0)
                rotate(radians(180))
                image((imgForceField[self.framecount]), -200 ,-height, 200,height)
        else:
            image((imgForceField[self.framecount]), self.positionX, 0, 200,height)
        noTint()
        
    def reset(self):
        rand = int(random(0,2))
        if rand == 1:
            self.sens = "up"
        else:
            self.sens = "down"
#----------------------------------- Classe Nuage ------------------------------------------
class Nuage:
    def __init__(self):
        self.hauteur = 363
        self.largeur = 635
        self.positionX = random(-self.largeur,width+self.largeur)
        self.positionY = random(-self.hauteur,height+self.hauteur)
        self.vecteurVitesse = PVector(1,0.25)
        
    def display(self):
        fill(128,129,127)
        image(imgNuage,self.positionX,self.positionY - self.hauteur/2 ,self.largeur, self.hauteur)#635*363
    
    def update(self):
        self.positionY += self.vecteurVitesse.y
        self.positionX += self.vecteurVitesse.x
    
    def rebondir(self):
        if self.positionX >= width + self.largeur/2:
             self.vecteurVitesse.x = -self.vecteurVitesse.x
        if self.positionX <= 0 - self.largeur*2:
            self.vecteurVitesse.x = -self.vecteurVitesse.x
        if self.positionY >= height + self.hauteur/2:
            self.vecteurVitesse.y = -self.vecteurVitesse.y
        if self.positionY <= 0 - self.hauteur*2:
            self.vecteurVitesse.y = -self.vecteurVitesse.y
#--------------------------------------------------------- Classe Bonus -----------------------------------------------------
class Bonus:
    def __init__(self):
        self.taille = 70
        self.positionX = random(200,width - 100)
        self.positionY = random(100,height- 100)
        self.alive = True  
        self.framecountAlive = 0
        self.timeAlive = random(700,800)
        self.effet = "Bonus"
        self.initialised = False 
    
    def display(self):
        if self.alive == True:
            if self.effet == "Bonus":
                image(imgBonus,self.positionX-self.taille/2,self.positionY-self.taille/2 , self.taille, self.taille)
            if self.effet == "Malus":
                image(imgMalus,self.positionX-self.taille/2,self.positionY -self.taille/2, self.taille, self.taille)

    def update(self):
        if self.alive == True:
            self.framecountAlive += 1
            for balle in listeBalles:
                if sqrt((self.positionX - balle.vecteurPosition.x)**2 + (self.positionY - balle.vecteurPosition.y)**2) < self.taille:
                    self.alive = False
                    if self.effet == "Bonus":
                        P1.hauteur += 20
                    if self.effet == "Malus":
                        P1.hauteur -= 20
            if self.framecountAlive > self.timeAlive:
                self.alive = False    
    
    def reseteffet(self):
        if self.initialised == False:
            aleatoire = int(random(0,2))
            if aleatoire == 1:
                self.effet = "Bonus"
            else:
                self.effet = "Malus"
            self.initialised = True
        
                
#---------------------------- gameplay  boss ------------------------
class Docteur:
    def __init__(self):
        self.largeur1 = 100
        self.hauteur1 = height/2
        self.positionX1 = width - 100
        self.positionY1 = 0
        self.largeur2 = 100
        self.hauteur2 = height/2
        self.positionX2 = width - 100
        self.positionY2 = height/2
        self.multiplication1 = int(random(2,10))
        self.multiplication2 = int(random(2,10))
        self.resultat = self.multiplication1 * self.multiplication2
        self.aleatoire = int(random(-15,15))
        self.alive = True
        self.framecountBoss3 = 0
        self.rand = int(random (0,2))
        self.gagner = 0
        self.framecountStop = 0 
        self.repriseX = 0
        self.repriseY = 0
        
    def display(self):
        if self.alive == True:
            stroke(255)
            fill(0)
            R1=rect(self.positionX1,self.positionY1,self.largeur1,self.hauteur1)
            R2=rect(self.positionX2,self.positionY2,self.largeur2,self.hauteur2)
            fill(255)
            f = createFont("Impact",50)
            textFont(f)
            text( "{0} x {1}".format(self.multiplication1,self.multiplication2),width/2,50)
            if self.rand == 0:
                f = createFont("Impact",50)
                textFont(f)
                text(self.resultat, self.positionX1 + 10 , self.positionY1 + 200)
                text(self.resultat + self.aleatoire , self.positionX2 + 10, self.positionY2 + 200)
            if self.rand == 1:
                f = createFont("Impact",50)
                textFont(f)
                text(self.resultat + self.aleatoire, self.positionX1 + 10 , self.positionY1 + 200)
                text(self.resultat , self.positionX2 + 10, self.positionY2 + 200)
            
    def update(self):
        if self.alive == True:
            for balle in listeBalles:
                if self.rand == 0:
                    if balle.vecteurPosition.x> self.positionX1 and balle.vecteurPosition.y < self.hauteur2:
                        self.bonus(balle)
                        self.alive = False
                        self.gagner = True
                    if balle.vecteurPosition.x > self.positionX2 and balle.vecteurPosition.y > self.hauteur2:
                        self.malus(balle)
                        self.alive = False
                        self.gagner = False
                if self.rand == 1:
                    if balle.vecteurPosition.x> self.positionX1 and balle.vecteurPosition.y < self.hauteur2:
                        self.malus(balle)
                        self.alive = False
                        self.gagner = False
                    if balle.vecteurPosition.x > self.positionX2 and balle.vecteurPosition.y > self.hauteur2:
                        self.bonus(balle)
                        self.alive = False
                        self.gagner = True
                if self.aleatoire == 0:
                    if balle.vecteurPosition.x> self.positionX1 and balle.vecteurPosition.y < self.hauteur2:
                        self.bonus(balle)
                        self.alive = False
                        self.gagner = True
                    if balle.vecteurPosition.x > self.positionX2 and balle.vecteurPosition.y > self.hauteur2:
                        self.bonus(balle)
                        self.alive = False
                        self.gagner = True
                
    def resetcalcul(self):
        if self.alive == False:
            self.framecountBoss3 += 1
            if self.gagner == True:
                image(imgKawashima,width/3,height/5,300,400)
            if self.gagner == False:
                image(imgKawashima2,width/7,150,642,400)

        test = False
        for balle in listeBalles:
            if self.framecountBoss3 > 400 and balle.vecteurVitesse.x < 0 and 500 < balle.vecteurPosition.x < 590 :
                self.repriseX = balle.vecteurVitesse.x
                self.repriseY = balle.vecteurVitesse.y
                test = True
        if test == True:
            self.alive = True
            self.framecountBoss3 = 0
            self.multiplication1 = int(random(2,10))
            self.multiplication2 = int(random(2,10))
            self.resultat = self.multiplication1 * self.multiplication2
            self.aleatoire = int(random(-15,15))
        if test == True:
            self.alive = True
            self.rand = int(random (0,2))
        if test == True:
            QuestionKawashima.play()
            QuestionKawashima.rewind()
        for balle in listeBalles:
            if test == True:
                balle.vecteurVitesse.x = 0
                balle.vecteurVitesse.y = 0
            
            if balle.vecteurVitesse.x == 0:
                self.framecountStop += 1
                if self.framecountStop == 120:
                    balle.vecteurVitesse.x = self.repriseX
                    balle.vecteurVitesse.y = self.repriseY
                    self.framecountStop = 0
   
                     

        """if self.gagner == True:
            SonBonus.play()
            SonBonus.close()
            SonBonus.rewind()
        if self.gagner == False:
            SonMalus.play()
            SonMalus.close()
            SonMalus.rewind()"""
 
                    
    def malus(self,objet):
        P1.hauteur -= 15
        if objet.vecteurVitesse.x >= 15:
            objet.vecteurVitesse.x = objet.vecteurVitesse.x
        if objet.vecteurVitesse.x <= 15:
            objet.vecteurVitesse.x += random(0.5,2)
        
    def bonus(self,objet):
        P1.hauteur += 15
        if objet.vecteurVitesse.x <= 4:
            objet.vecteurVitesse.x = objet.vecteurVitesse.x
        if objet.vecteurVitesse.x >= 4:
            objet.vecteurVitesse.x += random(-0.5,-2)
   
#---------------------------- BlackHole -------------------------------------------
class BlackHole:
    def __init__(self):
        self.masse = 7E15 #(en kg) 7E15 :une valeur qui marche et ne bug pas
    #7E15 = 10 x la masse totale de carbone dans l'atmosphère    source:wikipedia
        self.taille = 250
        self.vecteurPosition = PVector(random(100+self.taille,width-self.taille-150),random(self.taille, height-self.taille))
        self.angle = 0
        self.rotation = "left"
    def display(self):
        if self.rotation == "left":
            self.angle += 1
        if self.rotation == "right":
            self.angle -= 1
        if self.angle >= 360:
            self.angle = 0
            
        with pushMatrix():
            translate(self.vecteurPosition.x, self.vecteurPosition.y)
            rotate(radians(self.angle))
            image(imgBlackHole,-self.taille/2 , -self.taille/2, self.taille, self.taille)
    def reset(self):
        rand = int(random(0,2))
        if rand == 1:
            self.rotation = "right"
        else:
            self.rotation = "left"
#---------------------------------- Portails ----------------------------------------------
class Portails:
    def __init__(self):
        self.vecteurPositionBleu = PVector(random( 150,width-70),random(30,height-100))
        self.vecteurPositionOrange = PVector(random (150,width-70),random(30,height-100))
        
    def display(self):
        image(imgPortailBleu, self.vecteurPositionBleu.x-30,self.vecteurPositionBleu.y-49,60,98)
        image(imgPortailOrange, self.vecteurPositionOrange.x-30,self.vecteurPositionOrange.y-49,60,98)
        #ellipse(self.vecteurPositionBleu.x ,self.vecteurPositionBleu.y , 70,70) #hitbox
        
#------------------------------------ Balle ---------------------------------------------------
class Balle:
    def __init__(self):
        self.vecteurPosition = PVector(width/2,height/2)
        self.vecteurVitesse = PVector(0,0)
        self.vecteurAcceleration = PVector(0,0)
        self.R = random ((difficulty(50,200)),250) #couleurs
        self.V = random (50,(difficulty(255,-130)))
        self.B = random (50,(difficulty(255,-130)))
        self.rainbowR = int(random(-3,3))
        self.rainbowV = int(random(-3,3))
        self.rainbowB = int(random(-3,3))
        self.alive = True
        self.tpPossible = True  #pour les portails
        self.angle = 0 #pour la balle weathley
        self.rand1 = 0 #pour utiliser la tp avec le boss Nox
        self.rand2 = 0
        self.diametre = int(random(19,21))
        self.initialised = False #pour permettre au boss Nox de pas totallement reset la balle
        self.trail = 0
        
    def display(self):
        if self.alive == True:
            #--- affichage de westley
            if optionBoss1 == True:
                self.angle += 3
                if self.angle > 360:
                    self.angle = 0
                #--- pour le faire tourner
                with pushMatrix():
                    translate(self.vecteurPosition.x,self.vecteurPosition.y)
                    rotate(radians(self.angle))
                    image(imgWBalle,-20,-20,40,40)
            #---- affichage d'une balle normale
            else:
                noStroke()
                fill(self.R ,self.V ,self.B )
                ellipse(self.vecteurPosition.x,self.vecteurPosition.y,self.diametre,self.diametre)
                stroke(0,255,255)
                #line(self.vecteurPosition.x, self.vecteurPosition.y, self.vecteurVitesse.x * 10 +self.vecteurPosition.x, self.vecteurVitesse.y* 10 +self.vecteurPosition.y)
                noStroke()

    def update(self):
        self.vecteurPosition.add(self.vecteurVitesse)
        self.vecteurVitesse.add(self.vecteurAcceleration)
        #---- trail du mode rainbow
        if optionRainbow == True:
            self.trail += 1
            if self.trail >= 3:
                self.trail = 0
                listeTrail.append(trail(PVector(self.vecteurPosition.x ,self.vecteurPosition.y))) 
    
    def rebondir(self):
        global scoreSolo ,menuVar
        if P1.alive == True:
            #--- plaque
            if self.vecteurPosition.x<P1.positionX + P1.largeur and self.vecteurPosition.x >P1.positionX-P1.largeur and self.vecteurPosition.y > P1.positionY-P1.hauteur/2 and self.vecteurPosition.y < P1.positionY + P1.hauteur/2 and self.vecteurVitesse.x < 0:
                difference = P1.positionY - self.vecteurPosition.y 
                self.vecteurVitesse.y = 1
                coeff = 0.125 #coeff qui marche  0.125 = 1/8
                if P1.hauteur > 500:
                    coeff = 0.015 #coeff pour plaque debug 0.015 = 2/200
                self.vecteurVitesse.y = difference *- self.vecteurVitesse.y*coeff #fonction
                self.vecteurVitesse.x = -self.vecteurVitesse.x 
        #------- mur de droite 
        if self.vecteurPosition.x > width-10 and self.vecteurVitesse.x > 0:
            self.vecteurVitesse.x = -self.vecteurVitesse.x
            scoreSolo += difficulty(1,1)
            self.acceleration()
        #----- mur du bas
        if self.vecteurPosition.y > height-10 and self.vecteurVitesse.y > 0:
            self.vecteurVitesse.y = -self.vecteurVitesse.y
            self.antiBugY()
        #----- mur du haut
        if self.vecteurPosition.y < 10 and self.vecteurVitesse.y < 0:
            self.vecteurVitesse.y = -self.vecteurVitesse.y
            self.antiBugY()
        #----- mur de gauche
        if self.vecteurPosition.x < -20 and self.alive == True:
            scoreSolo -= difficulty(2,3)
            self.alive = False
            #-------- S'il a plus de balle en jeu, la partie s'arrête -----
            count = 0
            for Balle in listeBalles:
                if Balle.alive == True:
                    count += 1
            if count <= 0:
                #------------------- Défaite Joueur ------------------
                if optionBoss1 == True:
                    menuVar = "lose1"
                    #--- chargement de la phrase de fin
                    if optionMusique == True:
                        musiqueStop()
                    if optionSon == True:
                        r = int(random(1,8))
                        if r == 1:
                            PunchlineL1.play()
                            PunchlineL1.setGain(-10)
                            PunchlineL1.rewind()
                        if r == 2:
                            PunchlineL2.play()
                            PunchlineL2.setGain(-10)
                            PunchlineL2.rewind()
                        if r == 3:                        
                            PunchlineL3.play()
                            PunchlineL3.setGain(-10)
                            PunchlineL3.rewind()
                        if r == 4:                        
                            PunchlineL4.play()
                            PunchlineL4.setGain(-10)
                            PunchlineL4.rewind()
                        if r == 5:                    
                            PunchlineL5.play()
                            PunchlineL5.setGain(-10)
                            PunchlineL5.rewind()
                        if r == 6:                        
                            PunchlineL6.play()
                            PunchlineL6.setGain(-10)
                            PunchlineL6.rewind()
                        if r == 7:                       
                            PunchlineL7.play()
                            PunchlineL7.setGain(-10)
                            PunchlineL7.rewind()
                        print(r)
                    #--- pour arriver dans le menu de fin
                else:
                    menuVar = "finPong"
                    musiqueStop()
                    
            
    #------ fonction rebondir spécial multijoueur ----
    def rebondirMulti(self):
        global menuVar,scoreGauche,scoreDroit
        #plaque du joueur gauche
        if P1.alive == True:
            if self.vecteurPosition.x<P1.positionX + P1.largeur and self.vecteurPosition.x >P1.positionX-P1.largeur and self.vecteurPosition.y > P1.positionY-P1.hauteur/2 and self.vecteurPosition.y < P1.positionY + P1.hauteur/2 and self.vecteurVitesse.x < 0:
                difference = P1.positionY - self.vecteurPosition.y 
                self.vecteurVitesse.y = 1
                coeff = 0.125 #coeff qui marche 0.125 = 1/8
                if P1.hauteur > 500:
                    coeff = 0.015 #coeff pour plaque debug 0.015 = 2/200
                self.vecteurVitesse.y= difference * coeff*-self.vecteurVitesse.y #fonction
                self.vecteurVitesse.x= -self.vecteurVitesse.x 
                scoreGauche += 1
                
        #plaque du joueur droit
        if P2.alive == True:
            if self.vecteurPosition.x > P2.positionX and self.vecteurPosition.x < P2.positionX+P2.largeur and self.vecteurPosition.y > P2.positionY-P2.hauteur/2 and self.vecteurPosition.y < P2.positionY + P2.hauteur/2 and self.vecteurVitesse.x > 0:
                difference = P2.positionY - self.vecteurPosition.y 
                self.vecteurVitesse.y = 1
                coeff = 0.125 #coeff qui marche  0.125 = 1/8
                if P1.hauteur > 500:
                    coeff = 0.015 #coeff pour plaque debug 0.015 = 2/200
                self.vecteurVitesse.y= difference * coeff*-self.vecteurVitesse.y #fonction
                self.vecteurVitesse.x= -self.vecteurVitesse.x 
                scoreDroit += 1
        #mur du bas
        if self.vecteurPosition.y > height-10 and self.vecteurVitesse.y > 0:
            self.vecteurVitesse.y = -self.vecteurVitesse.y
            self.acceleration()
            self.antiBugY()
        #mur du haut
        if self.vecteurPosition.y < 10 and self.vecteurVitesse.y < 0:
            self.vecteurVitesse.y = -self.vecteurVitesse.y
            self.acceleration()
            self.antiBugY()
        #mur de gauche
        if self.vecteurPosition.x < -20 and self.alive == True:
            scoreGauche -= 2
            self.alive = False
            
        #mur de droite
        if self.vecteurPosition.x > width+20 and self.alive == True:
            scoreDroit -= 2
            self.alive = False
            
        count = 0
        #-------- S'il a plus de balle en jeu, la partie s'arrête -----
        for i in listeBalles:
            if i.alive == True:
                count += 1
        if count <= 0:
            menuVar = "menue"
            musiqueStop()
            if optionMusique == True:
                mMenu.loop()
                mMenu.rewind()
        
    def resetAcceleration(self):
        global v1
        v1 = self.vecteurAcceleration.copy()
        self.vecteurAcceleration.x = 0
        self.vecteurAcceleration.y = 0
    def resetBall(self):
        if optionBoss2 != True: #pour donner une position aléatoire à la balle sauf avec Nox
            self.vecteurPosition.x = random(750,880)
            self.vecteurPosition.y = random(20,690)
                
        rand = int(random(0,2)) # pour avoir une valeur entre 0 et 1 
        if rand == 1: # pour avoir un mouvement max trop faible dans un sens ou dans l'autre
            self.vecteurVitesse.x = random(-(difficulty(8,5)),-5)
        else:
            self.vecteurVitesse.x = random(5,(difficulty(8,5)))

        rand = int(random(0,2))
        if rand == 1: # pour avoir un mouvement max trop faible dans un sens ou dans l'autre
            self.vecteurVitesse.y = random(-8,-5)
        else:
            self.vecteurVitesse.y = random(5,8)
        
        #pour commencer en mettant la balle au milieu
        if (optionBoss1 == True or menuVar == "pongMulti" or optionDocteur == True) and self.initialised == False:
            self.vecteurPosition.x = (width/2)
            self.vecteurPosition.y = (height/2)
            self.vecteurVitesse.x = -6
            
        if optionDebug == True: #pour faire des tests avec la balle si besoin
            self.vecteurPosition = PVector (120,height/2)
            self.vecteurVitesse = PVector(-1,0)
            self.vecteurAcceleration = PVector(0,0)
        self.initialised = True
        #------ pour éviter le 0 pour ranbow
        while self.rainbowR == 0:
            self.rainbowR = int(random(-3,3))
        while self.rainbowV == 0:
            self.rainbowV = int(random(-3,3))
        while self.rainbowB == 0:
            self.rainbowB = int(random(-3,3))
            
    def acceleration(self):
        self.vecteurAcceleration.x += int(random(-4,2))
        if menuVar == "pongMulti":
            self.vecteurAcceleration.x += int(random(-1,2))#entre -1 et 1
        if self.vecteurVitesse.x < -difficulty(14,5):#pour controler la balle à haute vitesse
            self.vecteurAcceleration.x += int(random(-1,4))
            self.antiBugY()
    def antiBugY(self):
        if self.vecteurVitesse.y >= 20: #pour empêcher la balle de faire que haut bas haut bas...
            self.vecteurVitesse.y = self.vecteurVitesse.y/1.5
        if self.vecteurVitesse.y <= -20:
            self.vecteurVitesse.y = self.vecteurVitesse.y/1.5
             #self.vecteurAcceleration.x += int(random(-2,4))
#----------------- Lancement du jeu ,utilisé après les boutons -------------
def lancementDuJeu(mode):
    global menuVar
    if mode == "solo":
        menuVar = "pongSolo"
    if mode == "multi":
        menuVar = "pongMulti"
    initialisationMods()
    resetScore()
    for Balle in listeBalles:
        Balle.resetBall()
    musiqueStopmMenu()
    musique()

#--------------------------------- Curseur -----------------------------------------
def curseur():
    noCursor()
    image(imgCurseur ,mouseX,mouseY,26,40) #106/160
#--------------------------------------- Ecran Victoire Boss1 --------------------------------------------------------
def win1():
    global menuVar
    #background(0)
    image(imgWinBoss1,0,0,width,height)
    if keyPressed: #keyIndex == 10: #10 pour Entrer
        menuVar = "menue"
        if optionMusique == True:
            musiqueStop()
            mMenu.loop()
            mMenu.rewind()
#--------------------------------- Ecran Défaite Boss1-----------------------------------------------------------
def lose1():
    global menuVar
    #background(0)
    image(imgLoseBoss1,0,0,width,height)
    if keyPressed: #10 pour Entrer
        menuVar = "menue"
        if optionMusique == True:
            musiqueStop()
            mMenu.loop()
            mMenu.rewind()
        
def blueScreen():
    #background(0)
    image(imgBlueScreen,0,0,width,height)
#------------------------------ PongSolo ----------------------------------
def pongSolo():
    nettoyer()
    modsEvent()
    updateBalls()
    modNuage()
    dessiner()
    score()
    
    """for balle in listeBalles:
        print(int(balle.vecteurVitesse.x))  """
#-------------------------------------- Modsevent / Pour jouer les mods -------------------------
def modsEvent():
    global listeMissiles,scoreSolo,listeBalles
    #--------------------------------------- Pour le boss Nox -------------------------------------
    if optionBoss2 == True:
        N1.frameUpdate()
        N1.display()
        #------------------ spell
        if N1.spell == "slow":
            for Balle in listeBalles:
                Balle.vecteurAcceleration.x = -Balle.vecteurVitesse.x/2.2
                Balle.vecteurAcceleration.y = -Balle.vecteurVitesse.y/2.2
        if N1.spell == "acceleration":
            for Balle in listeBalles:
                if Balle.vecteurVitesse.x > 0:
                    Balle.vecteurAcceleration.x += 4
                else:
                    Balle.vecteurAcceleration.x -= 4
                if Balle.vecteurVitesse.y > 0:
                    Balle.vecteurAcceleration.y += 3
                else:
                    Balle.vecteurAcceleration.y -= 3
        if N1.spell == "reverse":
            for Balle in listeBalles:
                Balle.vecteurAcceleration.x = -Balle.vecteurVitesse.x*2
                Balle.vecteurAcceleration.y = -Balle.vecteurVitesse.y*2
                
        if N1.spell == "stop":
            N1.used = "stop"
        if N1.spell == "tp":
            N1.used = "tp"
            for Balle in listeBalles:
                Balle.rand1 = 0
                Balle.rand2 = 0
        #---- pour stoper les balles
        if N1.used == "stop" and N1.frameSpell < 50:
            for Balle in listeBalles:
                Balle.vecteurVitesse = PVector(0,0)
        #---- pour tp les balles
        if N1.used == "tp" and N1.frameSpell < 60:
            for Balle in listeBalles:
                if menuVar == "pongMulti":
                    if Balle.rand1 == 0:
                        Balle.rand1 = int(random(-3,3))
                    if Balle.rand2 == 0:
                        Balle.rand2 = int(random(-4,4))
                else:
                    if Balle.rand1 == 0:
                        Balle.rand1 = int(random(-5,15))
                    if Balle.rand2 == 0:
                        Balle.rand2 = int(random(-6,6))
                Balle.vecteurPosition.x += Balle.rand1 - Balle.vecteurVitesse.x
                Balle.vecteurPosition.y += Balle.rand2 - Balle.vecteurVitesse.y
        #--------- Pour appliqué la fin des spells longs ----------
        if N1.frameSpell >= 50 and N1.used == "stop":
            for Balle in listeBalles:
                Balle.resetBall()
                Balle.acceleration()
            N1.used = "none"
        
        if N1.frameSpell >= 60 and N1.used == "tp":
            for Balle in listeBalles:
                N1.used = "none"

        #---------- reset spell
        N1.spell = "none"
        #-------------------------- Update des machine ----------------------
        for noxine in listeNoxines:
            if noxine.alive == True:
                noxine.frameUpdate()
                noxine.update()
                noxine.display()
                
            if noxine.focus == "left" and noxine.vecteurPosition.x < P1.positionX + P1.largeur and noxine.alive == True: 
                noxine.explosion = True
                
            if noxine.focus == "right" and noxine.vecteurPosition.x > P2.positionX - P2.largeur and noxine.alive == True:
                noxine.explosion = True
            if (width/2 - 3 < noxine.vecteurPosition.x < width/2+3)and noxine.alive == True:
                rand = int(random(0,5))#entre 1 et 4
                if rand == 1:
                    noxine.explosion = True
            if noxine.explosion == True:
                noxine.explose()
    #--------------------- Boss Event -----------------
    if optionDocteur == True:
        C1.update()
        C1.display()
        C1.resetcalcul()
    #-------------------- Mod: Boss1 / GLaDOS -----------------------
    global Soin
    if optionBoss1 == True:
        Boss.display()
        for a in listeNeuro:
            if a.alive == True:
                a.frameUpdate()
                a.display()
                P1.hp -= 0.1
                Soin = Scaph()
                Soin.display()
                Soin.update()
                for Balle in listeBalles:
                    if sqrt(( Balle.vecteurPosition.x - Soin.positionX )**2+( Balle.vecteurPosition.y - Soin.positionY)**2) <= 70:
                        P1.hp += 0.2
                    else:
                        Soin.aie()
        for a in listeMissiles:
            if a.alive == True:
                a.update()
                a.display()
                a.reset()
                #------------ contact Missile - Plaque
                if a.vecteurPosition.x <=0:
                    a.alive = False
                if a.vecteurPosition.x <= P1.positionX +20 and a.vecteurPosition.y < P1.positionY + P1.hauteur/2 and a.vecteurPosition.y > P1.positionY - P1.hauteur/2 :
                    a.alive = False
                    P1.hp -= 4
        #---------------------------------------- Contact Balle - Boss + sorts ----------------------------------------------
        if Boss.alive == True:
            for Balle in listeBalles:
                #ellipse (Balle.vecteurPosition.x , Balle.vecteurPosition.y , 100, 100) <--- Zone ou il faut placer le curseur pour soin()
                # avant le or: Collision entre la balle et le "câblage" de GLaDOS---- après le or: collision avec la "tête" de GLaDOS
                if (Balle.vecteurPosition.x > width/1.35 and Balle.vecteurPosition.y < 400 and Balle.vecteurVitesse.x > 0) or (Balle.vecteurPosition.x > width/1.65 and Balle.vecteurPosition.y < height/2.05 + 155  and Balle.vecteurPosition.y > height/2.05  and Balle.vecteurVitesse.x > 0):
                    Balle.vecteurVitesse.x = -Balle.vecteurVitesse.x
                    Balle.acceleration()
                    Boss.hp -= 10
                    Boss.dammage = True
                    listeMissiles.append(Missile())
                    scoreSolo += difficulty(1,1)
                    if Boss.phase == 2:
                        listeMissiles.append(Missile())
                        listeMissiles.append(Missile())
                #collision avec le mur de protection
                if Balle.vecteurPosition.x > width/1.65 and Balle.vecteurPosition.y > height/2.05 + 155 and Balle.vecteurVitesse.x > 0:
                    Balle.vecteurVitesse.x = -Balle.vecteurVitesse.x
            
            if Boss.phase == 2:
                    Boss.Time()
                    if Boss.M == 1:
                        listeMissiles.append(Missile())
                        listeMissiles.append(Missile())
                        listeMissiles.append(Missile())
                    if Boss.N == 1:
                        listeNeuro.append(Neuro())
                        fill(255,0,0)
    #------------------------------------------- Forcefield update ---------------------------------------
    if optionForceField == True:
        F1.update()
    #----------------------------------------- Contact Balle - Portails --------------------------------------------
    for Portails in listePortails:
        Portails.display()
        for Balle in listeBalles:
            if sqrt(( Portails.vecteurPositionBleu.x - Balle.vecteurPosition.x)**2 +(Portails.vecteurPositionBleu.y - Balle.vecteurPosition.y)**2) < 60 and Balle.tpPossible == True:
                #calcul de la distance = sqrt((Xb -Xa)²+(Yb-Ya)²)
                Balle.vecteurPosition = PVector(Portails.vecteurPositionOrange.x ,Portails.vecteurPositionOrange.y)
                Balle.tpPossible = False
            elif sqrt(( Portails.vecteurPositionOrange.x - Balle.vecteurPosition.x)**2 +(Portails.vecteurPositionOrange.y - Balle.vecteurPosition.y)**2) < 60 and Balle.tpPossible == True:
                #calcul de la distance = sqrt((Xb -Xa)²+(Yb-Ya)²)
                Balle.vecteurPosition = PVector(Portails.vecteurPositionBleu.x ,Portails.vecteurPositionBleu.y)
                Balle.tpPossible = False
            #----------------- pour rendre la tp possible ------------------
            if sqrt(( Portails.vecteurPositionBleu.x - Balle.vecteurPosition.x)**2 +(Portails.vecteurPositionBleu.y - Balle.vecteurPosition.y)**2) > 70 and sqrt(( Portails.vecteurPositionOrange.x - Balle.vecteurPosition.x)**2 +(Portails.vecteurPositionOrange.y - Balle.vecteurPosition.y)**2) > 70:
                Balle.tpPossible = True 
    #---------------------------------------------- Contact  Balle - Forcefield -------------------------------------
    if optionForceField == True:
        for Balle in listeBalles:
            if Balle.vecteurPosition.x > F1.positionX and Balle.vecteurPosition.x < F1.positionX +200:
                if F1.sens == "up" and Balle.vecteurPosition.y > 10:
                    Balle.vecteurAcceleration.y -= difficulty(0.5,0.4) # à remettre à 0.5 , 0.4
                elif F1.sens == "down" and Balle.vecteurPosition.y < height-10:
                    Balle.vecteurAcceleration.y += difficulty(0.5,0.4)
    #------------------------------------ Calcul de la gravitation du trou noir ----------------------------
    if optionBlackHole == True:
        global vecteurG, B1
        B1.display()
        for Balle in listeBalles:
            if Balle.alive == True:
                G = 6.67E-11 #constante gravitationnelle
                #distance entre 2 points = sqrt((xb-xa)²+(yb-ya)²) avec b pour Balle
                distance = sqrt((Balle.vecteurPosition.x - B1.vecteurPosition.x)**2 + (Balle.vecteurPosition.y- B1.vecteurPosition.y)**2)
                g = (G * 2.7E-3 * B1.masse) * 1/(distance**2)
                vecteurG = PVector(0,0)
                vecteurG.sub(Balle.vecteurPosition)
                vecteurG.add(B1.vecteurPosition)
                vecteurG.setMag(1) #pour une gravitation plus réaliste mais moins amusante
                vecteurG.mult(g)
                Balle.vecteurAcceleration.add(vecteurG)
                """stroke(255,255,255)
                line(Balle.vecteurPosition.x ,Balle.vecteurPosition.y, vecteurG.x*1E7, vecteurG.y*1E7)"""
    #------------- rainbow -------------
    if optionRainbow == True:
        for Balle in listeBalles:
            
            Balle.R += Balle.rainbowR
            if Balle.R >= 255 or Balle.R <= 0:
                Balle.rainbowR = -Balle.rainbowR
                
            Balle.V += Balle.rainbowV
            if Balle.V >= 255 or Balle.V <= 0:
                Balle.rainbowV = -Balle.rainbowV
                
            Balle.B += Balle.rainbowB
            if Balle.B >= 255 or Balle.B <= 0:
                Balle.rainbowB = -Balle.rainbowB
#____________________ Mod: Trail-------------
    if optionRainbow == True:
        for trail in listeTrail:
            if trail.alive == True:
                trail.update()
                trail.display()
#-------------------------- Bonus Event ---------------------------
    if optionBonus == True:
        global framecountBonus, listeBonus
        for bonus in listeBonus:
            bonus.update()
            bonus.display()
        framecountBonus += 1
        if framecountBonus > 600:
            listeBonus.append(Bonus())
            framecountBonus = 0 
            for bonus in listeBonus:
                bonus.reseteffet() # 
#--------------------------- Nuage Event --------------------------
def modNuage():
    if optionNuage == True:
        Nu.update()
        Nu.display()
        Nu.rebondir()
#-------------------------------- Reset Solo -----------------------------------------
def resetScore():
    global scoreSolo,scoreGauche,scoreDroit
    scoreSolo = 0
    scoreGauche = 0
    scoreDroit = 0
#---------------------------------- Initialisation TOUT les mods ! ----------------------
def initialisationMods():
    global optionBoss1, optionDocteur
    initialisationPlaques()
    initialisationPortails()
    initialisationBalles()
    initialisationForceField()
    initialisationBlackHole()
    if menuVar == "pongMulti":
        optionBoss1 = False
    initialisationGLaDOS()
    initialisationNox()
    initialisationNuage()
    initialisationBonus()
    if menuVar == "pongMulti":
        optionDocteur = False
    initialisationDocteur()
#---------------------------------------- Initialisation Boss ---------------------------------
def initialisationDocteur():
    global C1
    if optionDocteur == True:
        C1 = Docteur()
        QuestionKawashima.play()
        QuestionKawashima.rewind()
#---------------------------------------- Initialisation Bonus ---------------------------------
def initialisationBonus():
    global listeBonus, framecountBonus
    listeBonus = []
    framecountBonus = 0
    listeBonus.append(Bonus())
    for bonus in listeBonus:
         bonus.reseteffet()
#------------------------------------- Initialisation Nox ---------------------------------
def initialisationNox():
    global N1, listeNoxines
    listeNoxines = []
    if optionBoss2 == True:
        N1 = Nox()
#----------------------------------- Initialisation Brouillard ---------------------------------
def initialisationNuage():
    global Nu, Brouillard
    Nu = Nuage()
#------------------------------------ Initialisation GLaDOS ---------------------------------
def initialisationGLaDOS():
    global Boss, listeMissiles,listeNeuro
    if optionBoss1 == True:
        Boss = GLaDOS()
        listeMissiles = []
        listeNeuro = []
#--------------------------------- Initialisation Portails -------------------------------
def initialisationPortails():
    global listePortails ,optionPortails
    listePortails = []
    if optionPortails == True:
        listePortails.append(Portails())
#---------------------------------------- Initialisation ForceField ----------------------------------
def initialisationForceField():
    global F1
    if optionForceField == True:
        F1 = ForceField()
        F1.reset()
#-------------------------------------- Initialisation BlackHole -------------------------------------
def initialisationBlackHole():
    global B1
    if optionBlackHole == True:
        B1 = BlackHole()
        B1.reset()
        
#---------------------------------- création et destruction des balles / Initialisation -------------------------------
def initialisationBalles():
    global listeBalles
    listeBalles = []
    for i in range(0,nombreBalle):
        listeBalles.append(Balle())
# ---------------------------------- Initialisation Plaques -----------------------------
def initialisationPlaques():
    global P2, P1
    P1 = Plaque()
    if menuVar == "pongMulti":
        P2 = Plaque(width -40-20, 2)
#--------------------------------------- score -----------------------------------------
def score():
    global scoreSolo,scoreGauche, scoreDroit
    fill(255,250,10)
    if optionRainbow == True:
        fill(255-backV,250-backR,10+backB)
    f = createFont("Impact",50)
    textFont(f)
    if menuVar == "pongSolo":
        text("SCORE =", 10,50)
        text(scoreSolo,190,50)
    if menuVar =="pongMulti":
        text(scoreGauche, 10,50)
        text(scoreDroit, width-35,50)
        
def rainbow():
    global backR, backV, backB, rainbowR, rainbowV, rainbowB
    if optionRainbow == True:
        background(0)
        backR += rainbowR
        if backR >= 255 or backR <= 0:
            rainbowR = -rainbowR
        backV += rainbowV
        if backV >= 255 or backV <= 0:
            rainbowV = -rainbowV
        backB += rainbowB
        if backB >= 255 or backB <= 0:
            rainbowB = -rainbowB
        fill(backR,backV,backB,20)#4e var: plus c'est petit = plus c'est transparent
        noStroke()
        rect(0,0,width,height)
#--------------------------------------- Nettoyer -----------------------------------------
def nettoyer():
    #background(0)
    if optionBoss2 == True:
        image(imgNoxBack,0,0,width,height)
    elif optionBoss1 == True:
        image(imgGLaDOSBack,0,0,width,height)
    else:
        image(fondPong, 0,0,width,height)
    rainbow()
#--------------------------------------- Dessiner -----------------------------------------
def dessiner():
    #------------------- Controle de la plaque
    global P1,P2
    if P1.alive == True:
        P1.update()
        P1.display()
    
    if menuVar == "pongMulti" and P2.alive == True:
        P2.update()
        P2.display()
#----------------------------- Bouger -----------------------------------------
def updateBalls():
    for Balle in listeBalles:
        Balle.display()
        if menuVar == "pongMulti":
            Balle.rebondirMulti()
        if menuVar == "pongSolo":
            Balle.rebondir()
        Balle.update()
        Balle.resetAcceleration()
#------------------------------- Multijoueur ---------------------------------
def pongMulti():
    nettoyer()
    modsEvent()
    updateBalls()
    modNuage()
    dessiner()
    score()   
#----------------------------------------- Menu Principal ---------------------------
def menue():
    global menuVar 
    image(back,0,0,width,height) #--------Si ça lag trop ça vient d'ici
    

    #-------------------------------- Bouton Solo ------------------
    if mouseX > width/2-200 and mouseX< width/2-200+400 and mouseY>height/2.2 and mouseY<height/2.2+100: 
               #width/2-200 = gauche et width/2-200+400 = droite
        imgBoutonSolo = loadImage("boutonSolo2.png")
        if mousePressed:
            lancementDuJeu("solo")
    else:
        imgBoutonSolo = loadImage("boutonSolo1.png")
    image(imgBoutonSolo , width/2-200 ,height/2.2 , 400, 100)
    #rect(width/2-200,height/3,400,100) 
    #----------------------- bouton multijoueur -------------------------
    if mouseX > width/2-200 and mouseX< width/2-200+400 and mouseY>height/1.5  and mouseY<height/1.5 +100: 
               #width/2-200 = gauche et width/2-200+400 = droite
        imgBoutonMulti = loadImage("boutonMultijoueur2.png")
        if mousePressed:
            lancementDuJeu("multi")
            #---- Pour lancer le multijoueur
            menuVar = "pongMulti"

    else:
        imgBoutonMulti = loadImage("boutonMultijoueur1.png")
    image(imgBoutonMulti , width/2-200 ,height/1.5 , 400, 100)
    #rect(width/2-200,height/2 + height/30,400,100) 
    #-------------------------------- bouton 3 ------------------------------------
    """if mouseX > width/2-200 and mouseX< width/2-200+400 and mouseY>height -180 and mouseY<height -180+100: 
               #width/2-200 = gauche et width/2-200+400 = droite
        fill(0,0,255)
    else:
        fill(255)
    rect(width/2-200,height-180,400,100) """
    #--------------------------------- bouton option ----------------------------
    if mouseX > width-80 and mouseX < width-80+62 and mouseY > height-80 and mouseY < height-80+62: 
        if mousePressed:
            menuVar = "menuOption"
    image(imgBoutonOption ,width-80,height-80, 62, 62)
    #----------------------------------- curseur ------------------------------
    curseur()
#------------------------------------------- Menu Option ----------------------------
def menuOption():
    global boutonHardcore, optionPortails,menuVar,nombreBalle ,optionForceField, optionBlackHole,optionBoss1,optionBoss2,optionNuage,optionSon,optionMusique
    #background(0)
    image(backOption,0,0,width,height) #--------Si ça lag trop ça vient d'ici
    
#------------------------------------------Bouton Hardcore-------------------------------------------------------------- 
    if mouseX > width/15 and mouseX < width/15+60 and mouseY > height/170 and mouseY<height/170+60:
        boutonGodMod = loadImage ("boutonGodMod.png")
        image(boutonGodMod,width/1.35,height/80 ,225,53)#taille 225,53
        if mousePressed and mouseButton == RIGHT:
            if boutonHardcore == True:
                boutonHardcore = False
        if mousePressed and mouseButton == LEFT:
            boutonHardcore = True
    if boutonHardcore == True:
        image(imgCase2 , width/15 ,height/170 , 60, 60)
    else:
        image(imgCase1 , width/15 ,height/170 , 60, 60)
    image(Hardcore,width/7,height/38,400,28) #coordonné texte1 1860*130
#----------------------------------------Bouton nombre----------------------------------------------------------------
    if mouseX > width/15 and mouseX < width/15+40 and mouseY > height/10 and mouseY <height/10+40:
        if mousePressed and nombreBalle < 9:
            nombreBalle += 1
            time.sleep(0.06)
    if mouseX > width/15 and mouseX < width/15+60 and mouseY > height/10+150-52 and mouseY < height/10+150:
        if mousePressed and nombreBalle > 1:
            nombreBalle -= 1
            time.sleep(0.06)
            
    fill(0)
    f = createFont("Impact",50)
    textFont(f)
    text("Nombre de balles", width/8 ,height/4.2)
    text(nombreBalle,width/13,height/4.2)               
    image(imgBoutonNombre,width/15,height/10,40,150) #boutonNombre 
#----------------------------------- Bouton Portails -------------------------------------------------------------------
    if mouseX > width/15 and mouseX < width/15+60 and mouseY > height/3.2 and mouseY<height/3.2+60:
        if mousePressed and mouseButton == RIGHT:
            if optionPortails == True:
                optionPortails = False
        if mousePressed and mouseButton == LEFT:
            optionPortails = True
    if optionPortails == True:
        a = imgCase2
    else:
        a = imgCase1
    image(a,width/15,height/3.2,60,60) #bouton3*
    #time.sleep(0.01)
    image (imgTextePortail,width/7,height/3, 300,40)
    #rect(width/4,height/1.55,500,100) #coordonné texte3
#-------------------------------------- Bouton ForceField ----------------------------------------------------------
    if mouseX > width/15 and mouseX < width/15+60 and mouseY > height/2.5 and mouseY<height/2.5+60:
        if mousePressed and mouseButton == RIGHT:
            if optionForceField == True:
                optionForceField = False
        if mousePressed and mouseButton == LEFT:
            optionForceField = True
    if optionForceField == True:
        a = imgCase2
    else:
        a = imgCase1
    image(a,width/15,height/2.5,60,60)
    image(texteForceField, width/7.5, height/2.4,260,35)
#------------------------------------- Bouton BlackHole ----------------------------------------------------
    if mouseX > width/15 and mouseX < width/15+60 and mouseY > height/2 and mouseY<height/2+60:
        if mousePressed and mouseButton == RIGHT:
            if optionBlackHole == True:
                optionBlackHole = False
        if mousePressed and mouseButton == LEFT:
            optionBlackHole = True
    if optionBlackHole == True:
        a = imgCase2
    else:
        a = imgCase1
    image(a,width/15,height/2,60,60)
    image(texteTrouNoir, width/7.5, height/2.1,300,90) #836 x 252
#------------------------------------- Bouton Boss GLaDOS ----------------------------------------------------
    if mouseX > width/15 and mouseX < width/15+60 and mouseY > height/1.7 and mouseY<height/1.7+60:
        if mousePressed and mouseButton == RIGHT:
            if optionBoss1 == True:
                optionBoss1 = False
        if mousePressed and mouseButton == LEFT:
            optionBoss1 = True
    if optionBoss1 == True:
        a = imgCase2
    else:
        a = imgCase1
    image(a,width/15,height/1.7,60,60)
    image(texteBoss1, width/7.4, height/1.68,145,58) #584 x 232
#------------------------------------- Bouton Boss Nox ----------------------------------------------------
    if mouseX > width/15 and mouseX < width/15+60 and mouseY > height/1.48 and mouseY<height/1.48+60:
        if mousePressed and mouseButton == RIGHT:
            if optionBoss2 == True:
                optionBoss2 = False
        if mousePressed and mouseButton == LEFT:
            optionBoss2 = True
    if optionBoss2 == True:
        a = imgCase2
    else:
        a = imgCase1
    image(a,width/15,height/1.48,60,60)
    image(imgTexteBoss2, width/9, height/1.6,352,140) #2047,812
#--------------------------------- Bouton Nuage -------------------------------------------------
    if mouseX > width/1.9 and mouseX < width/1.9+60 and mouseY > height/3.2 and mouseY<height/3.2+60:
        if mousePressed and mouseButton == RIGHT:
            if optionNuage == True:
                optionNuage = False
        if mousePressed and mouseButton == LEFT:
            optionNuage = True
    if optionNuage == True:
        a = imgCase2
    else:
        a = imgCase1
    image(a,width/1.9,height/3.2,60,60)
    fill(0)
    f = createFont("Dialog.plain-48",50)
    textFont(f)
    text("Nuage", width/1.7 ,height/2.65)
#--------------------------------- Bouton Bonus --------------------------------------
    global optionBonus
    if mouseX > width/1.9 and mouseX < width/1.9+60 and mouseY > height/1.75 and mouseY<height/1.75+60:
        if mousePressed and mouseButton == RIGHT:
            if optionBonus == True:
                optionBonus = False
        if mousePressed and mouseButton == LEFT:
            optionBonus = True
    if optionBonus == True:
        a = imgCase2
    else:
        a = imgCase1
    image(a,width/1.9,height/1.7,60,60)
    fill(0)
    f = createFont("Dialog.plain-48",50)
    textFont(f)
    text("Bonus", width/1.7 ,height/1.52)

#--------------------------------- Bouton Rainbow --------------------------------------
    global optionRainbow
    if mouseX > width/1.9 and mouseX < width/1.9+60 and mouseY > height/2.05 and mouseY<height/2.05+60:
        if mousePressed and mouseButton == RIGHT:
            if optionRainbow == True:
                optionRainbow = False
        if mousePressed and mouseButton == LEFT:
            optionRainbow = True
    if optionRainbow == True:
        a = imgCase2
    else:
        a = imgCase1
    image(a,width/1.9,height/2.05,60,60)
    fill(0)
    f = createFont("Dialog.plain-48",50)
    textFont(f)
    text("Rainbow", width/1.7 ,height/1.8)
#----------------------------- Bouton Docteur Kawashima ---------------------------------
    global optionDocteur
    if mouseX > width/1.9 and mouseX < width/1.9+60 and mouseY > height/2.5 and mouseY<height/2.5+60:
        if mousePressed and mouseButton == RIGHT:
            if optionDocteur == True:
                optionDocteur = False
        if mousePressed and mouseButton == LEFT:
            optionDocteur = True
    if optionDocteur == True:
        a = imgCase2
    else:
        a = imgCase1
    image(a,width/1.9,height/2.5,60,60)
    fill(0)
    f = createFont("Dialog.plain-48",48)
    textFont(f)
    text("Dr. Kawashima", width/1.7,height/2.12)

#------------------------------------- Bouton Son ----------------------------------------------------
    if mouseX > width/1.16 and mouseX < width/1.16+100 and mouseY > height/2 and mouseY<height/2+100:
        if mousePressed and mouseButton == RIGHT:
            if optionSon == True:
                optionSon = False
        if mousePressed and mouseButton == LEFT:
            optionSon = True

    if optionSon == True:
        a = imgSonOUI
    else:
        a = imgSonNON
    image(a,width/1.16,height/2,100,100)
#------------------------------------- Bouton Musique ----------------------------------------------------
    if mouseX > width/1.16 and mouseX < width/1.16+100 and mouseY > height/1.5 and mouseY<height/1.5+100:
        if mousePressed and mouseButton == RIGHT:
            if optionMusique == True:
                optionMusique = False
        if mousePressed and mouseButton == LEFT:
            optionMusique = True

    if optionMusique == True:
        a = imgMusiqueOUI
    else:
        a = imgMusiqueNON
    image(a,width/1.16,height/1.5,100,100)
#------------------------------------ Bouton Return -----------------------------------------------------------------
    if mouseX > width/25 and mouseX < width/25+110 and mouseY > height/1.20 and mouseY<height/1.20+90:
        if mousePressed:
            menuVar = "menue"
    image(imgReturn,width/25,height/1.20,110,90)#280*240
    verif()
#--Curseur
    curseur()
#---------- vérification des mods ---------
def verif():
    global optionPortails,nombreBalle ,optionForceField, optionBlackHole,optionBoss1,optionBoss2, optionDocteur
    # ----pour n'avoir qu'un seul boss 
    test = 0
    if optionBoss1 == True:
        test += 1
        optionPortails = False
    if optionBoss2 == True:
        test += 1
    if optionDocteur == True:
        nombreBalle = 1
        test += 1
    if test >= 2:
        optionBoss1 = False
        optionBoss2 = False
        optionDocteur = False
    if optionForceField == True and optionBlackHole == True:
        optionForcefield = False
        optionBlackHole = False
    
#------------------- Menu quand le jeu est perdu -------------
def finPong():
    global menuVar
    image(backOption,0,0,width,height)
    fill(255,250,10)
    f = createFont("Impact",110)
    textFont(f)
    text("SCORE =",200,200)
    text(scoreSolo,600,200)
    if optionMusique == True:
        musiqueStop()
        mMenu.loop()
        mMenu.rewind()

    #--------------- bouton menu -----------------
    if mouseX > width/30 and mouseX < width/30+200 and mouseY > height/1.8 and mouseY<height/1.8+160:
        if mousePressed:
            menuVar = "menue"
    image(imgReturn,width/30,height/1.8,200,160)#280*240
    #------------------ bouton replay -----------------
    if mouseX > width/1.4 and mouseX < width/1.4+200 and mouseY > height/1.8 and mouseY<height/1.8+160:
        if mousePressed:
            lancementDuJeu("solo")
    image(imgRetry,width/1.4,height/1.8,200,160)#280*240
    #----- pour le curseur
    curseur()
#-------------------- Tout ce qui est en relation avec la musique ----------------

def musique():
    global Hard,Ez ,Easy,Ttm,Trou,Bossm,musiqueNox,Rmusic1,Rmusic2
    if optionMusique == True:
        if menuVar == "menue" or menuVar == "menuOption":
            mMenu.loop()
            mMenu.rewind()
        elif optionPortails == True and boutonHardcore == True and optionNuage == True and (optionBlackHole == True or optionForceField == True):
            Ttm.loop()
            Ttm.rewind()
        elif optionBoss2 == True:
            musiqueNox.loop()
            musiqueNox.rewind()
        elif optionBoss1 == True:
            Bossm.loop()
            Bossm.setGain(-10) #Pour baisser un peu le volume de la musique
            Bossm.rewind()
        elif optionDocteur == True:
            MusiqueKawashima.loop()
            MusiqueKawashima.setGain(-10)
            MusiqueKawashima.rewind()
        elif optionBlackHole == True:
            Trou.loop()
            Trou.rewind()
        elif boutonHardcore == True:
            Hard.loop()
            Hard.rewind()
        elif optionPortails == True or optionForceField == True:
            Easy.loop()
            Easy.rewind()
        elif optionRainbow == True:
            rMusic = int(random(0,2))
            if rMusic == 0:
                Rmusic1.loop()
                Rmusic1.rewind()
            if rMusic == 1 :
                Rmusic2.loop()
                Rmusic2.rewind()
        
        else:
            Ez.loop()
            Ez.rewind()
        
def musiqueStop():
    global Hard,Ez ,Easy,Ttm,Trou,Bossm,musiqueNox
    if optionMusique == True:
        if optionPortails == True and boutonHardcore == True and optionNuage == True and (optionBlackHole == True or optionForceField == True):
            Ttm.pause()
        elif optionBoss2 == True:
            musiqueNox.pause()
        elif optionBoss1 == True:
            Bossm.pause()
        elif optionDocteur == True:
            MusiqueKawashima.pause()
        elif optionBlackHole == True:
            Trou.pause()
        elif boutonHardcore == True:
            Hard.pause()
        elif optionPortails == True or optionForceField == True:
            Easy.pause()        
        elif optionRainbow == True:
            Rmusic1.pause()
            Rmusic2.pause()
        

        else:
            Ez.pause()
            
def musiqueStopmMenu():
    mMenu.pause()

#------------------ écriture d'un fichier JSON ------------
def ecritureDeFichier():
    global dictionnaireInfo
    dictionnaireInfo = {}
    dictionnaireInfo["optionSon"] = optionSon
    dictionnaireInfo["optionMusique"] = optionMusique
    dictionnaireInfo["boutonHardcore"] = boutonHardcore
    dictionnaireInfo["optionPortails"] = optionPortails
    dictionnaireInfo["optionForceField"] = optionForceField
    dictionnaireInfo["optionBlackHole"] = optionBlackHole
    dictionnaireInfo["ptionBoss1"] = optionBoss1
    dictionnaireInfo["optionBoss2"] = optionBoss2
    dictionnaireInfo["optionNuage"] = optionNuage
    dictionnaireInfo["nombreBalle"] = nombreBalle
    dictionnaireInfo["optionBonus"] = optionBonus
    dictionnaireInfo["optionRainbow"] = optionRainbow
    dictionnaireInfo["optionDocteur"] = optionDocteur
    
    #le dictionnaire qui sera écrit en JSON (à n'utiliser que si le dictionnaireInfo est vide)
    """dictionnaireInfo = {"optionSon" : True, "optionMusique" : True,"boutonHardcore" : False, "optionPortails" : False,
                        "optionForceField" : False,"optionBlackHole" : False ,"optionBoss1" : False,"optionBoss2" : False,
                        "optionNuage" : False,"nombreBalle" : 1}"""

    
    with open("data/info.JSON","w") as f:
        f.write(json.dumps(dictionnaireInfo, ensure_ascii=False))
#---------------------------------------------------------------------------------------------------------
def setup():
   
    size(900,700)
    imgChargement = loadImage("loading.jpg")
    image(imgChargement,0,0,width,height)
    global imgTextePortail,Hardcore,backOption,back,fondPong,imgCase1, imgCase2,imgPortailBleu, imgPortailOrange, imgCurseur, imgForceField,imgBoutonNombre
    global imgLoseBoss1 , imgWinBoss1, imgGLaDOSBack
    global texteForceField, imgBoutonOption, imgBlackHole, texteTrouNoir,imgGLaDOS1, imgGLaDOS2, imgMissile, imgPlateforme, imgWBalle,imgNox,imgNoxineG,imgNoxineD, imgNoxBack
    global imgExplosionBleu, imgSpell, texteBoss1,imgRetry, imgReturn,imgTexteBoss2, imgNuage,imgBlueScreen,imgMusiqueOUI,imgMusiqueNON,imgSonOUI,imgSonNON,imgNeuro
    global imgKawashima,imgKawashima2,imgBonus,imgMalus
#----------------------------------- Chargement des images ---------------------------------------
    imgTextePortail = loadImage("textePortail.png")#taille = 887x77
    Hardcore = loadImage("boutonHardcore.png")
    backOption = loadImage("ArcadeBackgroundVide.png")
    back = loadImage("ArcadeBackground.png")
    fondPong = loadImage("fondPong.png")
    imgCase1 = loadImage("case1.png")
    imgCase2 = loadImage("case2.png")
    imgBoutonNombre =loadImage("boutonNombre.png") #taille 100x 330 / taille d'une flèche 100x88
    imgPortailBleu = loadImage("PortailBleu.png") # 60x98
    imgPortailOrange = loadImage("PortailOrange.png")# 60x98
    imgCurseur = loadImage("curseur.png")
    imgBoutonOption = loadImage("boutonOption.png")
    imgBlackHole = loadImage("BlackHole.png") #250x250
    imgWinBoss1 = loadImage("GLaDOS/WIN.png")
    imgLoseBoss1 = loadImage("GLaDOS/Lose.png")
    imgForceField = []
    for i in range(0,44):
        imgForceField.insert(0,0)
    for i in range(1,43):
        imgForceField[i] = loadImage("Forcefield/frame-{}.gif".format(i)) #taille 257 * 600
    texteForceField = loadImage("texteForcefield.png")#875 * 119
    texteTrouNoir = loadImage("texteTrouNoir.png")#836 x 252
    imgGLaDOS2 = loadImage("GLaDOS/GLaDOS2.png")# 412*500
    imgGLaDOS1 = loadImage("GLaDOS/GLaDOS1.png")
    imgGLaDOSBack = loadImage("GLaDOS/Pannel.png")
    texteBoss1 = loadImage("texteBoss1.png")
    imgMissile = loadImage("GLaDOS/missile1.png")#120x34
    imgPlateforme = loadImage("GLaDOS/wall.png")
    imgWBalle = loadImage("GLaDOS/wBall.png")#40x40
    imgBlueScreen = loadImage("blueScreen.png")
    imgNox = []
    imgNoxineG = []
    imgNoxineD = []
    imgRetry = loadImage("boutonRetry.png")
    imgReturn =loadImage("boutonReturn.png")
    imgNoxBack = loadImage("Nox/backgroundNox.jpg")
    imgKawashima = loadImage("Kawashima.png")
    imgKawashima2 = loadImage("Kawashima2.png")
    imgBonus = loadImage("bonus.png")
    imgMalus = loadImage("malus.png")
    for i in range(0,20):
        imgNox.insert(0,0)
    for i in range(1,19):#pour charger les 18 images
        imgNox[i] = loadImage("Nox/frame-{}.gif".format(i)) # 678 x 621
    for i in range(0,3):
        imgNoxineG.insert(0,0)
    for i in range(1,3):#pour charger les 2 images
        imgNoxineG[i] = loadImage("Nox/noxine{}G.png".format(i))#100x100
    for i in range(0,3):
        imgNoxineD.insert(0,0)
    for i in range(1,3):#pour charger les 2 images
        imgNoxineD[i] = loadImage("Nox/noxine{}D.png".format(i))#100x100
        
    imgNeuro = []
    for i in range(0,4):
        imgNeuro.insert(0,0)
    for i in range(1,4):
        imgNeuro [i] = loadImage("GLaDOS/Neuro{}.png".format(i))#500,500

    imgExplosionBleu = []
    for i in range(0,14):
        imgExplosionBleu.insert(0,0)
    for i in range(1,13):#pour charger les 12 images
        imgExplosionBleu[i] = loadImage("explosionBleu/frame-{}.png".format(i))#180x180
    imgSpell = []
    for i in range(0,10):
        imgSpell.insert(0,0)
    for i in range(1,9):#pour charger les 8 images
        imgSpell[i] = loadImage("spell/spell{}.png".format(i))#900,700
    imgTexteBoss2 = loadImage("texteBoss2.png")#2047,812
    imgNuage = loadImage("nuage.png") #635*363
    imgMusiqueOUI = loadImage("boutonMusique.png") #288,290
    imgMusiqueNON = loadImage("boutonMusique2.png") #288,290
    imgSonOUI = loadImage("boutonSon.png") #288,290
    imgSonNON = loadImage("boutonSon2.png") #288,290
    #--chargement des punchline
    global PunchlineW1,PunchlineW2,PunchlineL1,PunchlineL2,PunchlineL3,PunchlineL4,PunchlineL5,PunchlineL6,PunchlineL7
    PunchlineW1 = minim.loadFile("GLaDOS/win/Win1.ogg")  
    PunchlineW2 = minim.loadFile("GLaDOS/win/Win2.ogg")
    PunchlineL1 = minim.loadFile("GLaDOS/lose/lose1.ogg")  
    PunchlineL2 = minim.loadFile("GLaDOS/lose/lose2.ogg")
    PunchlineL3 = minim.loadFile("GLaDOS/lose/lose3.ogg")  
    PunchlineL4 = minim.loadFile("GLaDOS/lose/lose4.ogg")
    PunchlineL5 = minim.loadFile("GLaDOS/lose/lose5.ogg")  
    PunchlineL6 = minim.loadFile("GLaDOS/lose/lose6.ogg")
    PunchlineL7 = minim.loadFile("GLaDOS/lose/lose7.ogg")
    #--- chargement des booms!
    global sonBoom1, sonBoom2, sonBoom3
    sonBoom1 = minim.loadFile("explosionBleu/boom1.wav")  
    sonBoom2 = minim.loadFile("explosionBleu/boom2.wav")  
    sonBoom3 = minim.loadFile("explosionBleu/boom3.wav") 
    #--- chargement musique de questions du docteurs
    global QuestionKawashima,SonBonus,SonMalus,MusiqueKawashima
    QuestionKawashima = minim.loadFile("musiques/QuestionKawashima.mp3")
    QuestionKawashima.setGain(-10)
    MusiqueKawashima = minim.loadFile("musiques/MusiqueKawashima.mp3")
    SonBonus = minim.loadFile("musiques/SonBonus.mp3")
    SonMalus = minim.loadFile("musiques/SonMalus.mp3")
    #--- chargement des musiques
    global Ttm,musiqueNox,Bossm,Trou,Hard,Easy,Ez,Rmusic1,Rmusic2,mMenu
    mMenu = minim.loadFile("musiques/mMenu.mp3")
    Ttm = minim.loadFile("musiques/Ttm.mp3")
    musiqueNox = minim.loadFile("musiques/musiqueNox.mp3")
    Bossm = minim.loadFile("musiques/Boss.mp3")
    Trou = minim.loadFile("musiques/Trou.mp3")
    Hard = minim.loadFile("musiques/Hard.mp3")
    Easy = minim.loadFile("musiques/Easy.mp3")
    Ez = minim.loadFile("musiques/Ez.mp3")
    Rmusic1 = minim.loadFile("R1.mp3")
    Rmusic2 = minim.loadFile("R2.mp3")
    musique()


    
#------- pour tester plus facilement
def debug():
    global menuVar,fps
    if keyPressed and key == "9":
        menuVar = "blueScreen"
    if keyPressed and key == "8":
        menuVar = "menue"
        if optionMusique == True:
            musiqueStop()
    if keyPressed and key == "7":
        if menuVar == "pongSolo" or menuVar == "pongMulti":
            for Balle in listeBalles:
                Balle.vecteurVitesse = PVector(0,0)
    if keyPressed and key == "6":
        if menuVar == "pongSolo":
            P1.hauteur = 680
        if menuVar == "pongMulti":
            P1.hauteur = 680
            P2.hauteur = 680
    if keyPressed and key == "1":
        fps = True
    if fps == True:
        print("fps=",int(frameRate))
    if keyPressed and key == "2":
        for Balle in listeBalles:
            print(Balle.vecteurVitesse)
    if keyPressed and key == "4":
        global showVecteurs
        showVecteurs = True
    if showVecteurs == True:
        for Balle in listeBalles:
            strokeWeight(12)
            stroke("#EFFF17")
            line(0,0,Balle.vecteurPosition.x, Balle.vecteurPosition.y)
            stroke(240,10,10)
            line(Balle.vecteurPosition.x, Balle.vecteurPosition.y, Balle.vecteurPosition.x+Balle.vecteurVitesse.x*8, Balle.vecteurPosition.y+Balle.vecteurVitesse.y*8)
            stroke("#DE00A7")
            line(Balle.vecteurPosition.x, Balle.vecteurPosition.y, Balle.vecteurPosition.x+v1.x*1500, Balle.vecteurPosition.y+v1.y*1500)
    
def draw():
    global menuVar
    noCursor()
    frameRate(60)
    if menuVar == "menue":
        menue()
    if menuVar == "pongSolo" :
        pongSolo()
    if menuVar == "menuOption":
        menuOption()
        ecritureDeFichier()
    if menuVar == "pongMulti":
        pongMulti()
    if menuVar == "finPong":
        finPong()
    if menuVar == "Win1":
        win1()
    if menuVar == "lose1":
        lose1()
    if menuVar == "blueScreen":
        blueScreen()
    debug()
