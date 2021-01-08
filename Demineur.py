import random
import math
import sys
from copy import deepcopy

INCONNU = '_'
PERDU = '!'
DRAPEAU = '*'

LEVELS = [(9,9), (16,16), (24,24)]
MINES = [10, 40, 100]


def genere_plateau_vide(level): # Level = 0/1/2
    x_size, y_size = LEVELS[level]
    plateau_vide = []
    for i in range(y_size):
        plateau_vide.append([])
        for j in range(x_size): 
            plateau_vide[i].append({"mine" : False, "etat" : INCONNU}) 
    return plateau_vide

def place_mines(plateau, level, alea=True):
    x_size,y_size = LEVELS[level]
    # Plateau_avec_mines = place_mines(plateau, level) # alea=True
    # Plateau_avec_mines = place_mines(plateau, level, alea = False) 
    n = MINES[level]
    plateau_avec_mines = deepcopy(plateau)
    if not alea:
    # On place les mines sur la diagonale
        for i in range(x_size):
            plateau_avec_mines[i][i]['mine'] = True
        return plateau_avec_mines

    # On place les mines de façon aléatoire
    while n!=0:
        i = random.randint(0,x_size-1)
        j = random.randint(0,y_size-1)
        if not plateau[i][j]['mine']:
            plateau_avec_mines[i][j]['mine'] = True
            n-=1       
    return plateau_avec_mines

def construire_plateau(level, alea = True):
    plateau_vide = genere_plateau_vide(level)
    plateau = place_mines(plateau_vide, level, alea)
    return plateau

def coup_joueur(plateau):
    # Le joueur donne (x,y) ou met un drapeau
    answer = input("Coordonnées ? : ")
    x, y = answer.split(',')
    d = input("Un DRAPEAU ? oui/non : ")
    if d == 'oui': 
        plateau[int(x)][int(y)]['etat'] = DRAPEAU
        return (int(x),int(y))
    
    else :
        plateau[int(x)][int(y)]['etat'] = INCONNU
        return (int(x),int(y))

def case_voisines(plateau,x,y):
    hauteur = len(plateau)
    largeur = len(plateau[0])
    l = []
    for i in range(-1,2):  
        for j in range(-1,2):
            l.append([x+i,y+j])   
    l.remove([x,y])
    l2=[]
    for k in l:
        if k[0] >= 0 and k[1] >= 0:
            if k[0] < hauteur and k[1]< largeur:
                l2.append(k)
    return l2   

def compte_mines_voisines(plateau,x,y):
    compt = 0
    L = case_voisines(plateau,x,y)
    t = len(L)
    for k in range(t):
        if plateau[L[k][0]][L[k][1]]['mine']== True:
            compt+=1
    return compt
    
def composante_connexe(plateau,x,y):
    # Met le plateau à jour en ouvrant toutes les cases vides à partir de la case (x,y)
    if plateau[x][y]['etat'] != INCONNU:
        return
    L = case_voisines(plateau,x,y)
    plateau[x][y]['etat'] = compte_mines_voisines(plateau,x,y)
    if plateau[x][y]['etat'] != 0:
        return
    else:
        for i in L:
            composante_connexe(plateau,i[0],i[1])
    
def decouvre_case(plateau,x,y):
    if plateau[x][y]["mine"] == True and plateau[x][y]["etat"] != DRAPEAU:
        plateau[x][y]["etat"] = PERDU
        print("Désolé, vous avez perdu ! ")
        return False 
    else :
        composante_connexe(plateau,x,y)
    return True

def compte_mine_solution(plateau):
    h = len(plateau)
    l = len(plateau[0])
    for x in range(h):
        for y in range(l):
            if plateau[x][y]["mine"] :
                plateau[x][y]["etat"] = PERDU
            if plateau[x][y]["etat"] == INCONNU:
                plateau[x][y]["etat"] = INCONNU
            if not plateau[x][y]["mine"] and plateau[x][y]["etat"] != INCONNU:
                plateau[x][y]["etat"] = compte_mines_voisines(plateau,x,y)
    return plateau

def total_mines(plateau):
    # Compte le nombre total de mines sur le plateau.
    c = 0
    for i in plateau:
        for j in i:
            if j['mine'] == True:
                c +=1
    return c

def check(plateau):
    # Compte le nombre de drapeau et de case inconnue
    c = 0
    for i in plateau:
        for j in i:
            if j['etat'] == INCONNU or j['etat'] == DRAPEAU:
                c += 1
    return c

def display(plateau):
    # Permet d'afficher la grille
    for ligne in plateau:
        for colonne in ligne:
            print(colonne['etat'], ' ',end="")
        print()
    return None
    
def write_score(filename, score):
    with open(filename, mode='a', encoding='utf8') as f:
        f.write(str(score))
        f.write('\n')

def read_scores(filename):
    with open(filename, mode='r', encoding='utf8') as f:
        scores = f.readlines()
    return scores

def fin_de_jeu(score):
    write_score(filename,score)
    print( "Merci d'avoir joué ! ")
    sys.exit()

def choix():
    niv = input("Niveau 0/1/2/Q ? : ")
    return niv 

filename = 'scores.txt'

score = [0,0,0]

niv = choix()
plateau=construire_plateau(int(niv), alea = True )
m = total_mines(plateau)
print(m)

while True:
    display(plateau)
    x,y = coup_joueur(plateau)
    if plateau[x][y]["etat"] == DRAPEAU:
        m = m -1
        print(m)
    else : print(m)
    L = case_voisines(plateau,x,y)
    if not decouvre_case(plateau,x,y): # si le joueur à perdu
        score[1] = score[1] + 1
        score[2] = score[0]/score[1]*100
        plateau = compte_mine_solution(plateau)
        display(plateau)
        niv = choix()
        if niv =='Q':
            fin_de_jeu(score) 
        plateau = construire_plateau(int(niv), alea = True)
        m = total_mines(plateau) 
        print(m)                                        
    if total_mines(plateau) == check(plateau): # si le joueur à gagné  
        score[0] = score[0] + 1
        score[2] = score[0]/score[1]*100
        print("Bravo, tu as gagné ! ")
        niv = choix()
        if niv == 'Q':
            fin_de_jeu(score)
        plateau = construire_plateau(int(niv), alea = True)
        m = total_mines(plateau) 
        print(m)

    
    
        