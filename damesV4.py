#Jeu de dames créé par Célian Lesage

# python -m pip install rich
import numpy as np
from typing import Final
import sys
import os
import time

# python -m pip install rich
# module pour colorer le texte
from rich.console import Console
console = Console()

#constantes
DIM_DAMIER:Final[int] = 10  #dimension damier
DIM_DEPL:int = 4
DIM_DEPL_DAME:int = 36
DIM_COUNT_PRISE:int = 100
NOIR:str = '○'
NOIR_DAME:str = '▢'
BLANC:str = '●'
BLANC_DAME:str = '▨'
VIDE:str = ' '
PRISE_DAME:str = 'X'

#variables
mode_dev:bool = False
ligne_in:int
colonne_in:int
ligne_dest:int
colonne_dest:int
nb_blanc:int
nb_blanc_dame:int
nb_noir:int
nb_noir_dame:int
joueur:str = BLANC  #definit à qui le tour
nb_pion_adverse:int = 0 #pour connaitre le nombre de pions à prendre ->
pion_select:str
doit_prendre:bool = False
num_dest:int #numero pour le tableau de deplacement (tdepl)
dbl_prise:bool = False
ligne_dame:int  #coordonnées de destination des dames en deplacement sans prise
colonne_dame:int

#creation damier 10x10
damier = np.empty([DIM_DAMIER,DIM_DAMIER],dtype = np.str_) 

damier_prise = np.empty([DIM_DAMIER,DIM_DAMIER],dtype = np.str_)

'''
cases de deplacement : Ex  [1]    [0]   [1]     [0] -> Si deplacement possible
                           [0]    [-1]  [0]     [-1]  -> ligne de deplacement
                           [0]    [-1]  [2]     [-1]  -> colonne de deplacement
                            ->  1 x x
                                x ○ x
                                3 x x
'''
tdepl = np.empty([3,DIM_DEPL],dtype = np.int_)

count_prise = np.empty([4,DIM_COUNT_PRISE],dtype = np.int_)
#   emplacements de prises possibles :
#   [0]:capture ou non   [1]:0=blanc   1=noir      [2]:ligne_in      [3]:colonne_in

tdepl_dame = np.empty([3,DIM_DEPL_DAME],dtype = np.int_)
'''
Emplacements de deplacement sans prise des dames :
            
            De 0 à 8      de 9 à 17     de 18 à 26    de 27 à 35
Direction : haut gauche   haut droit    bas gauche    bas droite

cases possibles représentés par des 'x'
'''


#fonctions
def clear():    #efface ce qui est affiché dans la console (fonctionne sur windows, mac et linux)
    os.system('cls' if os.name == 'nt' else 'clear')

def clear_tdepl():    #initialise ou reset le tableau de deplacement
    for i in range(DIM_DEPL):
        tdepl[0][i] = 0
        tdepl[1][i] = -1
        tdepl[2][i] = -1
        
def clear_count_prise():
    for i in range(DIM_COUNT_PRISE):
        count_prise[0][i] = 0
        count_prise[1][i] = -1
        count_prise[2][i] = -1
        count_prise[3][i] = -1

def remplir_damier():   #remplissage du damier
    for i in range(0,4):    #les X
        for j in range(0,10):
            if i%2 == 0:
                if j%2 == 1:
                    damier[i][j] = NOIR
                else:
                    damier[i][j] = VIDE
            else:
                if j%2 == 0:
                    damier[i][j] = NOIR
                else:
                    damier[i][j] = VIDE

    for i in range(0,2):    #espace entre X et O
        for j in range(1,10):
            damier[4+i] = VIDE

    for i in range(6,10):   #les O
        for j in range(0,10):
            if i%2 == 0:
                if j%2 == 1:
                    damier[i][j] = BLANC
                else:
                    damier[i][j] = VIDE
            else:
                if j%2 == 0:
                    damier[i][j] = BLANC
                else:
                    damier[i][j] = VIDE
    return(damier)

def fcase_origine(damier:np.ndarray,joueur:str):  #demande la case d'origine d'un pion avec tests is possible (ligne_in,colonne_in) (utilisation : pion_select , ligne_in , colonne_in = fcase_origine(damier,joueur))
    global count_prise
    clear()
    show_damier()

    accept:str = 'n'
    select_pion:bool = False
    bon_pion:bool = False
    is_correct:bool = False
    deplacement_possible:bool = False
    prise_correct:bool = False

    #demande case d'origine
    while accept != 'o' or is_correct != True or deplacement_possible != True or select_pion != True or bon_pion != True or prise_correct != True:
        accept = 'n'
        select_pion:bool = False
        bon_pion:bool = False
        is_correct = False
        deplacement_possible = False
        prise_correct = False
        while True:
            console.print('Insérez l\'emplacement d\'origine d\'une pièce (ligne colonne entre 0 et 9)\n',end='',style='bold green')
            try:
                case_origine:str = str(input('>> '))
                ligne , colonne = case_origine.split()
                ligne_in = int(ligne)
                colonne_in = int(colonne)
                break
            except ValueError:
                clear()
                show_damier()
                console.print('\nERREUR : Valeur incorrecte !\n',style='bold red')
        if (colonne_in > 9 or ligne_in > 9):
            clear()
            show_damier()
            console.print('\nERREUR : Valeur en dehors des limites du damier !\n',style='bold red')
        else:
            is_correct = True
            if damier[ligne_in][colonne_in] == VIDE:
                clear()
                show_damier()
                console.print('\nERREUR : Vous devez sélectionner un pion !\n',style='bold red')
            else:
                select_pion = True
                if ((damier[ligne_in][colonne_in] == BLANC or damier[ligne_in][colonne_in] == BLANC_DAME) and joueur == NOIR) or ((damier[ligne_in][colonne_in] == NOIR or damier[ligne_in][colonne_in] == NOIR_DAME) and joueur == BLANC):
                    clear()
                    show_damier()
                    console.print('\nERREUR : Ce n\'est pas votre tour !\n',style='bold red')
                else:
                    bon_pion = True
                    
                    #SI pion == BLANC
                    if damier[ligne_in][colonne_in] == BLANC:
                        if colonne_in == 0:
                            if (damier[ligne_in - 1][colonne_in + 1] == NOIR or damier[ligne_in - 1][colonne_in + 1] == NOIR_DAME) and (damier[ligne_in - 2][colonne_in + 2] == NOIR or damier[ligne_in - 2][colonne_in + 2] == NOIR_DAME or damier[ligne_in - 2][colonne_in + 2] == BLANC or damier[ligne_in - 2][colonne_in + 2] == BLANC_DAME):
                                clear()
                                show_damier()
                                console.print('\nERREUR : Vous ne pouvez pas bouger ce pion !\n',style='bold red')
                            else:
                                deplacement_possible = True
                        elif colonne_in == 9:
                            if (damier[ligne_in - 1][colonne_in - 1] == BLANC) or (damier[ligne_in - 1][colonne_in - 1] == BLANC_DAME):
                                clear()
                                show_damier()
                                console.print('\nERREUR : Vous ne pouvez pas bouger ce pion !\n',style='bold red')
                            elif (damier[ligne_in - 1][colonne_in - 1] == NOIR or damier[ligne_in - 1][colonne_in - 1] == NOIR_DAME) and (damier[ligne_in - 2][colonne_in - 2] == NOIR or damier[ligne_in - 2][colonne_in - 2] == NOIR_DAME or damier[ligne_in - 2][colonne_in - 2] == BLANC or damier[ligne_in - 2][colonne_in - 2] == BLANC_DAME):
                                clear()
                                show_damier()
                                console.print('\nERREUR : Vous ne pouvez pas bouger ce pion !\n',style='bold red')
                            else:
                                deplacement_possible = True
                        elif (damier[ligne_in - 1][colonne_in - 1] == BLANC and damier[ligne_in - 1][colonne_in + 1] == BLANC) or (damier[ligne_in - 1][colonne_in - 1] == BLANC_DAME and damier[ligne_in - 1][colonne_in + 1] == BLANC_DAME):
                            clear()
                            show_damier()
                            console.print('\nERREUR : Vous ne pouvez pas bouger ce pion !\n',style='bold red')
                        elif colonne_in == 1 and (damier[ligne_in - 1][colonne_in - 1] == BLANC or damier[ligne_in - 1][colonne_in - 1] == BLANC_DAME or damier[ligne_in - 1][colonne_in - 1] == NOIR or damier[ligne_in - 1][colonne_in - 1] == NOIR_DAME) and ((damier[ligne_in - 1][colonne_in + 1] == BLANC or damier[ligne_in - 1][colonne_in + 1] == BLANC_DAME or damier[ligne_in - 1][colonne_in + 1] == NOIR or damier[ligne_in - 1][colonne_in + 1] == NOIR_DAME) and (damier[ligne_in - 2][colonne_in + 2] == BLANC or damier[ligne_in - 2][colonne_in + 2] == BLANC_DAME or damier[ligne_in - 2][colonne_in + 2] == NOIR or damier[ligne_in - 2][colonne_in + 2] == NOIR_DAME)):
                            clear()
                            show_damier()
                            console.print('\nERREUR : Vous ne pouvez pas bouger ce pion !\n',style='bold red')
                        elif colonne_in == 8 and (damier[ligne_in - 1][colonne_in + 1] == BLANC or damier[ligne_in - 1][colonne_in + 1] == BLANC_DAME or damier[ligne_in - 1][colonne_in + 1] == NOIR or damier[ligne_in - 1][colonne_in + 1] == NOIR_DAME) and (damier[ligne_in - 1][colonne_in - 1] == BLANC or damier[ligne_in - 1][colonne_in - 1] == BLANC_DAME or damier[ligne_in - 1][colonne_in - 1] == NOIR or damier[ligne_in - 1][colonne_in - 1] == NOIR_DAME) and (damier[ligne_in - 2][colonne_in - 2] == BLANC or damier[ligne_in - 2][colonne_in - 2] == BLANC_DAME or damier[ligne_in - 2][colonne_in - 2] == NOIR or damier[ligne_in - 2][colonne_in - 2] == NOIR_DAME):
                            clear()
                            show_damier()
                            console.print('\nERREUR : Vous ne pouvez pas bouger ce pion !\n',style='bold red')
                        elif (damier[ligne_in - 1][colonne_in - 1] == BLANC or damier[ligne_in - 1][colonne_in - 1] == BLANC_DAME or damier[ligne_in - 1][colonne_in - 1] == NOIR or damier[ligne_in - 1][colonne_in - 1] == NOIR_DAME) and (damier[ligne_in - 1][colonne_in + 1] == BLANC or damier[ligne_in - 1][colonne_in + 1] == BLANC_DAME or damier[ligne_in - 1][colonne_in + 1] == NOIR or damier[ligne_in - 1][colonne_in + 1] == NOIR_DAME) and (damier[ligne_in - 2][colonne_in - 2] == BLANC or damier[ligne_in - 2][colonne_in - 2] == BLANC_DAME or damier[ligne_in - 2][colonne_in - 2] == NOIR or damier[ligne_in - 2][colonne_in - 2] == NOIR_DAME) and (damier[ligne_in - 2][colonne_in + 2] == BLANC or damier[ligne_in - 2][colonne_in + 2] == BLANC_DAME or damier[ligne_in - 2][colonne_in + 2] == NOIR or damier[ligne_in - 2][colonne_in + 2] == NOIR_DAME):
                            clear()
                            show_damier()
                            console.print('\nERREUR : Vous ne pouvez pas bouger ce pion !\n',style='bold red')
                        else:
                            deplacement_possible = True
                    #SI pion == BLANC_DAME
                    elif damier[ligne_in][colonne_in] == BLANC_DAME:
                        for i in range(0,4,2):
                            for j in range(0,4,2):
                                k = ligne_in - 1 + i
                                l = colonne_in - 1 + j
                                try:
                                    if damier[k][j] == VIDE or (joueur == BLANC and (damier[k][j] == NOIR or damier[k][j] == NOIR_DAME) and damier[k-1+i][l-1+j] == VIDE):
                                        deplacement_possible = True
                                        break
                                except IndexError:
                                    pass
                            
                    #SI pion == NOIR
                    elif damier[ligne_in][colonne_in] == NOIR:
                        if colonne_in == 0:
                            if (damier[ligne_in + 1][colonne_in + 1] == NOIR) or (damier[ligne_in + 1][colonne_in + 1] == NOIR_DAME):
                                clear()
                                show_damier()
                                console.print('\nERREUR : Vous ne pouvez pas bouger ce pion !\n',style='bold red')
                            elif (damier[ligne_in + 1][colonne_in + 1] == BLANC or damier[ligne_in + 1][colonne_in + 1] == BLANC_DAME) and (damier[ligne_in + 2][colonne_in + 2] == NOIR or damier[ligne_in + 2][colonne_in + 2] == NOIR_DAME or damier[ligne_in + 2][colonne_in + 2] == BLANC or damier[ligne_in + 2][colonne_in + 2] == BLANC_DAME):
                                clear()
                                show_damier()
                                console.print('\nERREUR : Vous ne pouvez pas bouger ce pion !\n',style='bold red')
                            else:
                                deplacement_possible = True
                        elif colonne_in == 9:
                            if (damier[ligne_in + 1][colonne_in - 1] == NOIR) or (damier[ligne_in + 1][colonne_in - 1] == NOIR_DAME):
                                clear()
                                show_damier()
                                console.print('\nERREUR : Vous ne pouvez pas bouger ce pion !\n',style='bold red')
                            elif (damier[ligne_in + 1][colonne_in - 1] == BLANC or damier[ligne_in + 1][colonne_in - 1] == BLANC_DAME) and (damier[ligne_in + 2][colonne_in - 2] == NOIR or damier[ligne_in + 2][colonne_in - 2] == NOIR_DAME or damier[ligne_in + 2][colonne_in - 2] == BLANC or damier[ligne_in + 2][colonne_in - 2] == BLANC_DAME):
                                clear()
                                show_damier()
                                console.print('\nERREUR : Vous ne pouvez pas bouger ce pion !\n',style='bold red')
                            else:
                                deplacement_possible = True
                        elif (damier[ligne_in + 1][colonne_in - 1] == NOIR and damier[ligne_in + 1][colonne_in + 1] == NOIR) or (damier[ligne_in + 1][colonne_in - 1] == NOIR_DAME and damier[ligne_in + 1][colonne_in + 1] == NOIR_DAME):
                            clear()
                            show_damier()
                            console.print('\nERREUR : Vous ne pouvez pas bouger ce pion !\n',style='bold red')
                        elif colonne_in == 1 and (damier[ligne_in + 1][colonne_in - 1] == NOIR or damier[ligne_in + 1][colonne_in - 1] == NOIR_DAME or damier[ligne_in + 1][colonne_in - 1] == BLANC or damier[ligne_in + 1][colonne_in - 1] == BLANC_DAME) and (damier[ligne_in + 1][colonne_in + 1] == NOIR or damier[ligne_in + 1][colonne_in + 1] == NOIR_DAME or damier[ligne_in + 1][colonne_in + 1] == BLANC or damier[ligne_in + 1][colonne_in + 1] == BLANC_DAME) and (damier[ligne_in + 2][colonne_in + 2] == NOIR or damier[ligne_in + 2][colonne_in + 2] == NOIR_DAME or damier[ligne_in + 2][colonne_in + 2] == BLANC or damier[ligne_in + 2][colonne_in + 2] == BLANC_DAME):
                            clear()
                            show_damier()
                            console.print('\nERREUR : Vous ne pouvez pas bouger ce pion !\n',style='bold red')
                        elif colonne_in == 8 and (damier[ligne_in + 1][colonne_in - 1] == NOIR or damier[ligne_in + 1][colonne_in - 1] == NOIR_DAME or damier[ligne_in + 1][colonne_in - 1] == BLANC or damier[ligne_in + 1][colonne_in - 1] == BLANC_DAME) and (damier[ligne_in + 2][colonne_in - 2] == NOIR or damier[ligne_in + 2][colonne_in - 2] == NOIR_DAME or damier[ligne_in + 2][colonne_in - 2] == BLANC or damier[ligne_in + 2][colonne_in - 2] == BLANC_DAME) and (damier[ligne_in + 1][colonne_in + 1] == NOIR or damier[ligne_in + 1][colonne_in + 1] == NOIR_DAME or damier[ligne_in + 1][colonne_in + 1] == BLANC or damier[ligne_in + 1][colonne_in + 1] == BLANC_DAME):
                            clear()
                            show_damier()
                            console.print('\nERREUR : Vous ne pouvez pas bouger ce pion !\n',style='bold red')
                        elif (damier[ligne_in + 1][colonne_in - 1] == NOIR or damier[ligne_in + 1][colonne_in - 1] == NOIR_DAME or damier[ligne_in + 1][colonne_in - 1] == BLANC or damier[ligne_in + 1][colonne_in - 1] == BLANC_DAME) and (damier[ligne_in + 2][colonne_in - 2] == NOIR or damier[ligne_in + 2][colonne_in - 2] == NOIR_DAME or damier[ligne_in + 2][colonne_in - 2] == BLANC or damier[ligne_in + 2][colonne_in - 2] == BLANC_DAME) and (damier[ligne_in + 1][colonne_in + 1] == NOIR or damier[ligne_in + 1][colonne_in + 1] == NOIR_DAME or damier[ligne_in + 1][colonne_in + 1] == BLANC or damier[ligne_in + 1][colonne_in + 1] == BLANC_DAME) and (damier[ligne_in + 2][colonne_in + 2] == NOIR or damier[ligne_in + 2][colonne_in + 2] == NOIR_DAME or damier[ligne_in + 2][colonne_in + 2] == BLANC or damier[ligne_in + 2][colonne_in + 2] == BLANC_DAME):
                            clear()
                            show_damier()
                            console.print('\nERREUR : Vous ne pouvez pas bouger ce pion !\n',style='bold red')
                        else:
                            deplacement_possible = True
                            #SI pion == NOIR_DAME
                    elif damier[ligne_in][colonne_in] == NOIR_DAME:
                        for i in range(0,4,2):
                            for j in range(0,4,2):
                                k = ligne_in - 1 + i
                                l = colonne_in - 1 + j
                                try:
                                    if damier[k][j] == VIDE or (joueur == NOIR and (damier[k][j] == BLANC or damier[k][j] == BLANC_DAME) and damier[k-1+i][l-1+j] == VIDE):
                                        deplacement_possible = True
                                        break
                                except IndexError:
                                    pass
                            
                    if deplacement_possible == True:
                        #testprise
                        clear_count_prise()
                        for i in range(10):
                            for j in range(10):
                                test_prise(i,j,True)
                        if doit_prendre == True:
                            for i in range(DIM_COUNT_PRISE):
                                if joueur == BLANC:
                                    if count_prise[0][i] == 1 and count_prise[1][i] == 0 and count_prise[2][i] == ligne_in and count_prise[3][i] == colonne_in:
                                        prise_correct = True
                                elif joueur == NOIR:
                                    if count_prise[0][i] == 1 and count_prise[1][i] == 1 and count_prise[2][i] == ligne_in and count_prise[3][i] == colonne_in:
                                        prise_correct = True
                        else:
                            prise_correct = True
                        if prise_correct == True:
                            return(damier[ligne_in][colonne_in],ligne_in,colonne_in)
                        else:
                            clear()
                            show_damier()
                            console.print('\nERREUR : Vous devez obligatoirement prendre un pion quand vous le pouvez !\n',style='bold red')
                    else:
                        clear()
                        show_damier()
                        console.print('\nERREUR : Vous ne pouvez pas bouger ce pion !\n',style='bold red')

def test_prise(ligne_in:int,colonne_in:int,test:bool):   #test si il y a des pions adverse à prendre
    global doit_prendre, nb_pion_adverse
    if test == False:
        clear_tdepl()
        nb_pion_adverse = 0
        doit_prendre = False
        
    #pions blancs
    if (test == False and damier[ligne_in][colonne_in] == BLANC) or (test == True and joueur == BLANC and damier[ligne_in][colonne_in] == BLANC):
        if ligne_in == 0 or ligne_in == 1:
            pass
        elif (colonne_in == 0 or colonne_in == 1):
            if ligne_in == 9 or ligne_in == 8:
                if (damier[ligne_in - 1][colonne_in + 1] == NOIR or damier[ligne_in - 1][colonne_in + 1] == NOIR_DAME) and damier[ligne_in - 2][colonne_in + 2] == VIDE:
                    if test == False:
                        doit_prendre = True
                        nb_pion_adverse += 1
                        tdepl[0][1] = 1
                        tdepl[1][1] = ligne_in - 2
                        tdepl[2][1] = colonne_in + 2
                    else:
                        doit_prendre = True
                        count_prise[0][colonne_in+ligne_in*10] = 1
                        count_prise[1][colonne_in+ligne_in*10] = 0
                        count_prise[2][colonne_in+ligne_in*10] = ligne_in
                        count_prise[3][colonne_in+ligne_in*10] = colonne_in
            else:
                for i in range(0,4,2):
                    if ((damier[ligne_in - 1 + i][colonne_in + 1] == NOIR) or (damier[ligne_in - 1 + i][colonne_in + 1] == NOIR_DAME)) and damier[ligne_in - 2 + (i*2)][colonne_in + 2] == VIDE:
                        if test == False:
                            doit_prendre = True
                            nb_pion_adverse += 1
                            tdepl[0][1+i] = 1
                            tdepl[1][1+i] = ligne_in - 2 + i * 2
                            tdepl[2][1+i] = colonne_in + 2
                        else:
                            doit_prendre = True
                            count_prise[0][colonne_in+ligne_in*10] = 1
                            count_prise[1][colonne_in+ligne_in*10] = 0
                            count_prise[2][colonne_in+ligne_in*10] = ligne_in
                            count_prise[3][colonne_in+ligne_in*10] = colonne_in
                            
        elif (colonne_in == 9 or colonne_in == 8):
            if ligne_in == 9 or ligne_in == 8:
                if (damier[ligne_in - 1][colonne_in - 1] == NOIR or damier[ligne_in - 1][colonne_in - 1] == NOIR_DAME) and damier[ligne_in - 2][colonne_in - 2] == VIDE:
                    if test == False:
                        doit_prendre = True
                        nb_pion_adverse += 1
                        tdepl[0][0] = 1
                        tdepl[1][0] = ligne_in - 2
                        tdepl[2][0] = colonne_in - 2
                    else:
                        doit_prendre = True
                        count_prise[0][colonne_in+ligne_in*10] = 1
                        count_prise[1][colonne_in+ligne_in*10] = 0
                        count_prise[2][colonne_in+ligne_in*10] = ligne_in
                        count_prise[3][colonne_in+ligne_in*10] = colonne_in
            else:
                for i in range(0,4,2):
                    if ((damier[ligne_in - 1 + i][colonne_in - 1] == NOIR) or (damier[ligne_in - 1 + i][colonne_in - 1] == NOIR_DAME)) and damier[ligne_in - 2 + (i*2)][colonne_in - 2] == VIDE:
                        if test == False:
                            doit_prendre = True
                            nb_pion_adverse += 1
                            tdepl[0][0+i] = 1
                            tdepl[1][0+i] = ligne_in - 2 + i * 2
                            tdepl[2][0+i] = colonne_in - 2
                        else:
                            doit_prendre = True
                            count_prise[0][colonne_in+ligne_in*10] = 1
                            count_prise[1][colonne_in+ligne_in*10] = 0
                            count_prise[2][colonne_in+ligne_in*10] = ligne_in
                            count_prise[3][colonne_in+ligne_in*10] = colonne_in
        else:
            if ligne_in == 9 or ligne_in == 8:
                for i in range(0,4,2):
                    if (damier[ligne_in - 1][colonne_in - 1 + i] == NOIR or damier[ligne_in - 1][colonne_in - 1 + i] == NOIR_DAME) and damier[ligne_in - 2][colonne_in - 2 + (i*2)] == VIDE:
                        if test == False:
                            doit_prendre = True
                            nb_pion_adverse += 1
                            tdepl[0][0+int(i/2)] = 1
                            tdepl[1][0+int(i/2)] = ligne_in - 2
                            tdepl[2][0+int(i/2)] = colonne_in - 2 + i * 2
                        else:
                            doit_prendre = True
                            count_prise[0][colonne_in+ligne_in*10] = 1
                            count_prise[1][colonne_in+ligne_in*10] = 0
                            count_prise[2][colonne_in+ligne_in*10] = ligne_in
                            count_prise[3][colonne_in+ligne_in*10] = colonne_in
            else:
                for i in range(0,4,2):
                    for j in range(0,4,2):
                        if ((damier[ligne_in - 1 + i][colonne_in - 1 + j] == NOIR) or (damier[ligne_in - 1 + i][colonne_in - 1 + j] == NOIR_DAME)) and damier[ligne_in - 2 + (i * 2)][colonne_in - 2 + (j*2)] == VIDE:
                            if test == False:
                                doit_prendre = True
                                nb_pion_adverse += 1
                                tdepl[0][0+int(j/2)+i] = 1
                                tdepl[1][0+int(j/2)+i] = ligne_in - 2 + i * 2
                                tdepl[2][0+int(j/2)+i] = colonne_in - 2 + j * 2
                            else:
                                doit_prendre = True
                                count_prise[0][colonne_in+ligne_in*10] = 1
                                count_prise[1][colonne_in+ligne_in*10] = 0
                                count_prise[2][colonne_in+ligne_in*10] = ligne_in
                                count_prise[3][colonne_in+ligne_in*10] = colonne_in
                                
    #pions noirs
    elif (test == False and damier[ligne_in][colonne_in] == NOIR) or (test == True and joueur == NOIR and damier[ligne_in][colonne_in] == NOIR):
        if ligne_in == 8 or ligne_in == 9:
            pass
        elif colonne_in == 0 or colonne_in == 1:
            if ligne_in == 0 or ligne_in == 1:
                if (damier[ligne_in + 1][colonne_in + 1] == BLANC or damier[ligne_in + 1][colonne_in + 1] == BLANC_DAME) and damier[ligne_in + 2][colonne_in + 2] == VIDE:
                    if test == False:
                        doit_prendre = True
                        nb_pion_adverse += 1
                        tdepl[0][3] = 1
                        tdepl[1][3] = ligne_in + 2
                        tdepl[2][3] = colonne_in + 2
                    else:
                        doit_prendre = True
                        count_prise[0][colonne_in+ligne_in*10] = 1
                        count_prise[1][colonne_in+ligne_in*10] = 1
                        count_prise[2][colonne_in+ligne_in*10] = ligne_in
                        count_prise[3][colonne_in+ligne_in*10] = colonne_in
            else:
                for i in range(0,4,2):
                    if (damier[ligne_in - 1 + i][colonne_in + 1] == BLANC or damier[ligne_in - 1 + i][colonne_in + 1] == BLANC_DAME) and damier[ligne_in - 2 + (i*2)][colonne_in + 2] == VIDE:
                        if test == False:
                            doit_prendre = True
                            nb_pion_adverse += 1
                            tdepl[0][1+i] = 1
                            tdepl[1][1+i] = ligne_in - 2 + i * 2
                            tdepl[2][1+i] = colonne_in + 2
                        else:
                            doit_prendre = True
                            count_prise[0][colonne_in+ligne_in*10] = 1
                            count_prise[1][colonne_in+ligne_in*10] = 1
                            count_prise[2][colonne_in+ligne_in*10] = ligne_in
                            count_prise[3][colonne_in+ligne_in*10] = colonne_in
        elif (colonne_in == 9 or colonne_in == 8):
            if ligne_in == 0 or ligne_in == 1:
                if (damier[ligne_in + 1][colonne_in - 1] == BLANC or damier[ligne_in + 1][colonne_in - 1] == BLANC_DAME) and damier[ligne_in + 2][colonne_in - 2] == VIDE:
                    if test == False:
                        doit_prendre = True
                        nb_pion_adverse += 1
                        tdepl[0][2] = 1
                        tdepl[1][2] = ligne_in + 2
                        tdepl[2][2] = colonne_in - 2
                    else:
                        doit_prendre = True
                        count_prise[0][colonne_in+ligne_in*10] = 1
                        count_prise[1][colonne_in+ligne_in*10] = 1
                        count_prise[2][colonne_in+ligne_in*10] = ligne_in
                        count_prise[3][colonne_in+ligne_in*10] = colonne_in
            else:
                for i in range(0,4,2):
                    if (damier[ligne_in - 1 + i][colonne_in - 1] == BLANC or damier[ligne_in - 1 + i][colonne_in - 1] == BLANC_DAME) and (damier[ligne_in - 2 + (i*2)][colonne_in - 2] == VIDE):
                        if test == False:
                            doit_prendre = True
                            nb_pion_adverse += 1
                            tdepl[0][0+i] = 1
                            tdepl[1][0+i] = ligne_in - 2 + i * 2
                            tdepl[2][0+i] = colonne_in - 2
                        else:
                            doit_prendre = True
                            count_prise[0][colonne_in+ligne_in*10] = 1
                            count_prise[1][colonne_in+ligne_in*10] = 1
                            count_prise[2][colonne_in+ligne_in*10] = ligne_in
                            count_prise[3][colonne_in+ligne_in*10] = colonne_in
        else:
            if ligne_in == 0 or ligne_in == 1:
                for i in range(0,4,2):
                    if (damier[ligne_in + 1][colonne_in - 1 + i] == BLANC or damier[ligne_in + 1][colonne_in - 1 + i] == BLANC_DAME) and damier[ligne_in + 2][colonne_in - 2 + (i*2)] == VIDE:
                        if test == False:
                            doit_prendre = True
                            nb_pion_adverse += 1
                            tdepl[0][2+int(i/2)] = 1
                            tdepl[1][2+int(i/2)] = ligne_in + 2
                            tdepl[2][2+int(i/2)] = colonne_in - 2 + i * 2
                        else:
                            doit_prendre = True
                            count_prise[0][colonne_in+ligne_in*10] = 1
                            count_prise[1][colonne_in+ligne_in*10] = 1
                            count_prise[2][colonne_in+ligne_in*10] = ligne_in
                            count_prise[3][colonne_in+ligne_in*10] = colonne_in
            else:
                for i in range(0,4,2):
                    for j in range(0,4,2):
                        if ((damier[ligne_in - 1 + i][colonne_in - 1 + j] == BLANC) or (damier[ligne_in - 1 + i][colonne_in - 1 + j] == BLANC_DAME)) and damier[ligne_in - 2 + (i * 2)][colonne_in - 2 + (j*2)] == VIDE:
                            if test == False:
                                doit_prendre = True
                                nb_pion_adverse += 1
                                tdepl[0][0+int(j/2)+i] = 1
                                tdepl[1][0+int(j/2)+i] = ligne_in - 2 + i * 2
                                tdepl[2][0+int(j/2)+i] = colonne_in - 2 + j * 2
                            else:
                                doit_prendre = True
                                count_prise[0][colonne_in+ligne_in*10] = 1
                                count_prise[1][colonne_in+ligne_in*10] = 1
                                count_prise[2][colonne_in+ligne_in*10] = ligne_in
                                count_prise[3][colonne_in+ligne_in*10] = colonne_in
                                
    #pion dame blanc et noir
    elif (test == False and damier[ligne_in][colonne_in] == BLANC_DAME) or (test == True and joueur == BLANC and damier[ligne_in][colonne_in] == BLANC_DAME):
        for k in range(0,4,2):
            for l in range(0,4,2):
                i = ligne_in - 1 + k
                j = colonne_in - 1 + l
                while i >= 0 and i <= 9 and j >= 0 and j <= 9 and damier[ligne_in - 1 + k][colonne_in - 1 + l] == VIDE:
                    try:
                        if (damier[i][j] == NOIR or damier[i][j] == NOIR_DAME or damier[i][j] == BLANC or damier[i][j] == BLANC_DAME) and damier[i-1+k][j-1+l] == VIDE:
                            if test == False:
                                doit_prendre = True
                                nb_pion_adverse += 1
                                tdepl[0][0+int(l/2)+k] = 1
                                tdepl[1][0+int(l/2)+k] = i - 1 + k
                                tdepl[2][0+int(l/2)+k] = j - 1 + l
                                break
                            else:
                                doit_prendre = True
                                count_prise[0][colonne_in+ligne_in*10] = 1
                                if joueur == BLANC or joueur == BLANC_DAME:
                                    count_prise[1][colonne_in+ligne_in*10] = 0
                                else:
                                    count_prise[1][colonne_in+ligne_in*10] = 1
                                count_prise[2][colonne_in+ligne_in*10] = ligne_in
                                count_prise[3][colonne_in+ligne_in*10] = colonne_in
                                break
                    except IndexError:
                        pass
                    i = i - 1 + k
                    j = j - 1 + l


def fdeplacement():   #fait les propositions quand il n'y a pas de pion à prendre
    global dbl_prise
    if doit_prendre == False and dbl_prise == False:
        global num_dest
        clear_tdepl()
        #pions blancs
        if joueur == BLANC:
            if colonne_in == 0:
                tdepl[0][1] = 1
                tdepl[1][1] = ligne_in - 1
                tdepl[2][1] = colonne_in + 1
            elif colonne_in == 9:
                tdepl[0][0] = 1
                tdepl[1][0] = ligne_in - 1
                tdepl[2][0] = colonne_in - 1
            elif damier[ligne_in - 1][colonne_in - 1] == BLANC or damier[ligne_in - 1][colonne_in - 1] == BLANC_DAME or damier[ligne_in - 1][colonne_in - 1] == NOIR or damier[ligne_in - 1][colonne_in - 1] == NOIR_DAME:
                tdepl[0][1] = 1
                tdepl[1][1] = ligne_in - 1
                tdepl[2][1] = colonne_in + 1
            elif damier[ligne_in - 1][colonne_in + 1] == BLANC or damier[ligne_in - 1][colonne_in + 1] == BLANC_DAME or damier[ligne_in - 1][colonne_in + 1] == NOIR or damier[ligne_in - 1][colonne_in + 1] == NOIR_DAME:
                tdepl[0][0] = 1
                tdepl[1][0] = ligne_in - 1
                tdepl[2][0] = colonne_in - 1
            else:
                tdepl[0][1] = 1
                tdepl[1][1] = ligne_in - 1
                tdepl[2][1] = colonne_in + 1
                tdepl[0][0] = 1
                tdepl[1][0] = ligne_in - 1
                tdepl[2][0] = colonne_in - 1
        #pions noirs
        elif joueur == NOIR:
            if colonne_in == 0:
                tdepl[0][3] = 1
                tdepl[1][3] = ligne_in + 1
                tdepl[2][3] = colonne_in + 1
            elif colonne_in == 9:
                tdepl[0][2] = 1
                tdepl[1][2] = ligne_in + 1
                tdepl[2][2] = colonne_in - 1
            elif damier[ligne_in + 1][colonne_in - 1] == NOIR or damier[ligne_in + 1][colonne_in - 1] == NOIR_DAME or damier[ligne_in + 1][colonne_in - 1] == BLANC or damier[ligne_in + 1][colonne_in - 1] == BLANC_DAME:
                tdepl[0][3] = 1
                tdepl[1][3] = ligne_in + 1
                tdepl[2][3] = colonne_in + 1
            elif damier[ligne_in + 1][colonne_in + 1] == NOIR or damier[ligne_in + 1][colonne_in + 1] == NOIR_DAME or damier[ligne_in + 1][colonne_in + 1] == BLANC or damier[ligne_in + 1][colonne_in + 1] == BLANC_DAME:
                tdepl[0][2] = 1
                tdepl[1][2] = ligne_in + 1
                tdepl[2][2] = colonne_in - 1
            else:
                tdepl[0][3] = 1
                tdepl[1][3] = ligne_in + 1
                tdepl[2][3] = colonne_in + 1
                tdepl[0][2] = 1
                tdepl[1][2] = ligne_in + 1
                tdepl[2][2] = colonne_in - 1
        
        elif joueur == BLANC_DAME or joueur == NOIR_DAME:
            for i in range(0,4,2):
                for j in range(0,4,2):
                    k = ligne_in - 1 + i
                    l = colonne_in - 1 + j
                    try:
                        if damier[k][l] == VIDE:
                            tdepl[0][i+j//2] = 1
                            tdepl[1][i+j//2] = k
                            tdepl[2][i+j//2] = l
                    except IndexError:
                        pass
        
        
    if (dbl_prise == False or (dbl_prise == True and doit_prendre == True)):
        if joueur == BLANC or joueur == NOIR or ((joueur == BLANC_DAME or joueur == NOIR_DAME) and doit_prendre == True):
            for i in range(4):
                if tdepl[0][i] == 1:
                    damier_prise[tdepl[1][i]][tdepl[2][i]] = str(i + 1)
                    
        elif (joueur == BLANC_DAME or joueur == NOIR_DAME) and doit_prendre == False:
            for i in range(0,4,2):
                for j in range(0,4,2):
                    k = ligne_in - 1 + i
                    l = colonne_in - 1 + j
                    if tdepl[0][i+j//2] == 1:
                        while damier[k][l] == VIDE and k >= 0 and k <= 9 and l >= 0 and j <= 9:
                            damier_prise[k][l] = PRISE_DAME
                            k = k - 1 + i
                            l = l - 1 + j
                            


def in_case_dest(): #demande le numero de deplacement proposé avec tests (num_dest = in_case_dest())
    depl_ok:bool = False
    nb_deplacement:int = 0
    for i in range(4):
        if tdepl[0][i] == 1:
            nb_deplacement += 1
    while depl_ok == False:
        while True:
            nb_try:int = 0
            console.print('Insérez le numéro de la case de destination\n',end='',style='bold green')
            try:
                num_dest = int(input('>> ')) - 1
                break
            except ValueError:
                clear()
                show_damier_prise()
                console.print('\nERREUR : Valeur incorrecte !\n',style='bold red')
        for i in range(4):
            if tdepl[0][i] == 1:
                if (num_dest + 1) < 1 or (num_dest + 1) > 4 or (str((num_dest + 1)) != str(damier_prise[tdepl[1][i]][tdepl[2][i]])): #faire le test avec les valeur du tableau plus haut
                    nb_try += 1
                    if nb_try == nb_deplacement:
                        clear()
                        show_damier_prise()
                        console.print('\nERREUR : Valeur incorrecte !\n',style='bold red')
                        break
                else:
                    depl_ok = True
                    return(num_dest)
            

def in_case_dame(): # demande l'emplacement de destination d'une dame sans prise
    global ligne_dame,colonne_dame
    ok:bool = False
    while ok == False:
        console.print('Insérez l\'emplacement de destination de la dame (ligne colonne entre 0 et 9) (cases [bold green]marqueé(s)[/bold green] par un X)\n',end='',style='bold green')
        try:
            case_origine:str = str(input('>> '))
            ligne , colonne = case_origine.split()
            ligne_dame = int(ligne)
            colonne_dame = int(colonne)
        except ValueError:
            clear()
            show_damier_prise()
            console.print('\nERREUR : Valeur incorrecte !\n',style='bold red')
            break
        if damier_prise[ligne_dame][colonne_dame] == PRISE_DAME:
            ok = True
        if ok == False:
            clear()
            show_damier_prise()
            console.print('\nERREUR : Valeur incorrecte !\n',style='bold red')

def fcase_depl():   #deplacement d'un pion vers une case vide ou prise
    if doit_prendre == True:
        if joueur == BLANC_DAME or joueur == NOIR_DAME:
            damier[tdepl[1][num_dest]][tdepl[2][num_dest]] = damier[ligne_in][colonne_in]
            damier[ligne_in][colonne_in] = VIDE
            if num_dest == 0:
                damier[tdepl[1][num_dest]+1][tdepl[2][num_dest]+1] = VIDE
            elif num_dest == 1:
                damier[tdepl[1][num_dest]+1][tdepl[2][num_dest]-1] = VIDE
            elif num_dest == 2:
                damier[tdepl[1][num_dest]-1][tdepl[2][num_dest]+1] = VIDE
            elif num_dest == 3:
                damier[tdepl[1][num_dest]-1][tdepl[2][num_dest]-1] = VIDE
        else:
            damier[tdepl[1][num_dest]][tdepl[2][num_dest]] = damier[ligne_in][colonne_in]
            damier[ligne_in][colonne_in] = VIDE
            damier[int((tdepl[1][num_dest]+ligne_in)/2)][int((tdepl[2][num_dest]+colonne_in)/2)] = VIDE
    else:
        if joueur == BLANC or joueur == NOIR:
            damier[tdepl[1][num_dest]][tdepl[2][num_dest]] = damier[ligne_in][colonne_in]
            damier[ligne_in][colonne_in] = VIDE
        else:
            damier[ligne_dame][colonne_dame] = damier[ligne_in][colonne_in]
            damier[ligne_in][colonne_in] = VIDE

def ch_coord():
    global ligne_in,colonne_in
    ligne_in = tdepl[1][num_dest]
    colonne_in = tdepl[2][num_dest]

def show_damier():     #affichage du damier stylisé (rich console)
    if mode_dev == True:
        console.print('MODE DEV ACTIF\n\n',end='',style='bold red italic')
    console.print('Tour :',joueur,'    Blancs : ',(nb_blanc+nb_blanc_dame),'    Noirs :',(nb_noir+nb_noir_dame),'\n\n',end='', style = "bold blue")
    print('          ',end='')
    for i in range(DIM_DAMIER):
        console.print(i,'  ',end='')
    print('\n')
    for i in range(DIM_DAMIER):
        console.print('  ',i,'  ',end='')
        for j in range(DIM_DAMIER):
            console.print('[bold blue] |[/bold blue]',damier[i][j],end='', style = "bold white")
        console.print(' |',end='',style='bold blue')
        print('\n')

def show_damier_prise():     #affichage du damier alternatif stylisé (quand il y a proposition de prise) (rich console)
    clear()
    if mode_dev == True:
        console.print('MODE DEV ACTIF\n\n',end='',style='bold red italic')
    console.print('Tour :',joueur,'    Blancs : ',(nb_blanc+nb_blanc_dame),'    Noirs :',(nb_noir+nb_noir_dame),'\n\n',end='', style = "bold blue")
    print('          ',end='')
    for i in range(DIM_DAMIER):
        console.print(i,'  ',end='')
    print('\n')
    for i in range(DIM_DAMIER):
        console.print('  ',i,'  ',end='')
        for j in range(DIM_DAMIER):
            console.print(' ',end='')
            console.print('| ',end='',style="bold blue")
            if i == ligne_in and j == colonne_in:
                console.print(damier_prise[i][j],end='', style = "bold white reverse blink")
            elif damier_prise[i][j] == PRISE_DAME:
                console.print(damier_prise[i][j],end='', style = "bold cyan")
            else:
                console.print(damier_prise[i][j],end='', style = "bold white")
        console.print(' |',end='',style='bold blue')
        print('\n')

def entete():   #texte d'indication des pions
    console.print('\nLes pions ',NOIR,' sont les pions noirs.\nLes pions ',BLANC,' sont les pions blancs.\n',end='',style='blue')

def copie_damier(): #copie le damier dans le damier alternatif pour permettre l'affichage de propositions de deplacement
    for i in range(DIM_DAMIER):
        for j in range(DIM_DAMIER):
            damier_prise[i][j] = damier[i][j]

def ch_joueur():    #changement de joueur
    global joueur
    if joueur == BLANC or joueur == BLANC_DAME:
        joueur = NOIR
    else:
        joueur = BLANC

def compt_pion():   #compte le nombre de pions blanc / noirs dans le plateau -> nb_blanc/nb_noir
    global nb_blanc, nb_noir, nb_blanc_dame, nb_noir_dame
    nb_blanc = 0
    nb_blanc_dame = 0
    nb_noir = 0
    nb_noir_dame = 0
    for i in range(DIM_DAMIER):
        for j in range(DIM_DAMIER):
            if damier[i][j] == BLANC:
                nb_blanc += 1
            if damier[i][j] == BLANC_DAME:
                nb_blanc_dame +=1
            if damier[i][j] == NOIR:
                nb_noir += 1
            if damier[i][j] == NOIR_DAME:
                nb_noir_dame += 1
            
                
def tfin():
    end_game:bool = False
    agree:str = 'n'
    if nb_blanc == 0 and nb_blanc_dame == 0:
        clear()
        show_damier()
        console.print('\nLes pions noirs ont gagnés !\n',end='',style='bold blue blink')
        end_game = True
    elif nb_noir == 0 and nb_noir_dame == 0:
        clear()
        show_damier()
        console.print('\nLes pions blancs ont gagnés !\n',end='',style='bold blue blink')
        end_game = True
    elif nb_noir_dame == 1 and nb_blanc_dame == 1:
        clear()
        show_damier()
        console.print('\nEgalité !',end='',style='bold blue blink')
        end_game = True
    if end_game == True:
        console.print('\nRejouer ? (o/n)\n',end='',style='bold green')
        while 1:
            try:
                agree = str(input('>> '))
                break
            except ValueError:
                console.print('\nERREUR : Valeur incorrecte !\n',style='bold red')
        if agree == 'o':
            game()
        else:
            sys.exit()


def tdame():
    if (joueur == BLANC or joueur == BLANC_DAME):
        for i in range(10):
            if damier[0][i] == BLANC:
                damier[0][i] = BLANC_DAME
    elif (joueur == NOIR or joueur == NOIR_DAME):
        for i in range(10):
            if damier[9][i] == NOIR:
                damier[9][i] = NOIR_DAME

"""
FONCTIONS DE DEV
"""
def suppr_case():
    global damier
    clear()
    show_damier()
    temp:str
    console.print('\nCase à supprimer ? (<enter> pour passer)\n',end='', style = "bold red")
    test_case_origine:str = str(input('>> '))
    if test_case_origine != '':
        x , y = test_case_origine.split()
        test_ligne_origine = int(x)
        test_colonne_origine = int(y)
        damier[test_ligne_origine][test_colonne_origine] = VIDE
        suppr_case()

def test_intervertir_case():    #FONCTION DE DEV -> intervertir 2 cases sans contraintes
    global damier
    clear()
    show_damier()
    temp:str
    console.print('\ncase d\'origine (<enter> pour passer)\n',end='', style = "bold red")
    test_case_origine:str = str(input('>> '))
    if test_case_origine != '':
        x , y = test_case_origine.split()
        test_ligne_origine = int(x)
        test_colonne_origine = int(y)
        console.print('case de destination\n',end='', style = "bold red")
        test_case_dest:str = str(input('>> '))
        x,y = test_case_dest.split()
        test_ligne_dest = int(x)
        test_colonne_dest = int(y)
        a_dest:str = damier[test_ligne_dest][test_colonne_dest]
        b_or:str = damier[test_ligne_origine][test_colonne_origine]
        temp = a_dest
        damier[test_ligne_dest][test_colonne_dest] = b_or
        damier[test_ligne_origine][test_colonne_origine] = temp

def test_choix_joueur():    #FONCTION DE DEV -> choisir le joueur sans contraintes
    accept1:bool = False
    while accept1 == False:
        clear()
        show_damier()
        entete()                          
        console.print('\nJOUEUR ? (<enter> pour passer)\n',end='', style = "bold red")
        entree:str = str(input('>> '))
        if entree == 'blanc' or entree == 'BLANC':
            accept1 = True
            return(BLANC)
        elif entree == 'noir' or entree == 'NOIR':
            accept1 = True
            return(NOIR)
        elif entree == '':
            return(joueur)
        
def test_choix_pion():      #FONCTION DE DEV -> changer un pion
    global damier
    accept2:bool = False
    while accept2 == False:
        clear()
        show_damier()
        console.print('\nQUEL PION CHANGER ? (<enter> pour passer)\n',end='', style = "bold red")
        entree:str = str(input('>> '))
        if entree != '':
            x , y = entree.split()
            x = int(x)
            y = int(y)
            console.print('\nBLANC/BLANC_DAME/NOIR/NOIR_DAME ?\n',end='', style = "bold red")
            entree:str = str(input('>> '))
            if entree == 'NOIR':
                damier[x][y] = NOIR
            if entree == 'NOIR_DAME':
                damier[x][y] = NOIR_DAME
            if entree == 'BLANC':
                damier[x][y] = BLANC
            if entree == 'BLANC_DAME':
                damier[x][y] = BLANC_DAME
        accept2 = True
        

def dev():  #active le mode dev ou non
    global joueur, mode_dev    
    clear()
    console.print('Mode dev ? (o) [bold red]/ <enter> pour continuer...[/bold red]\n',end='', style = "bold red")
    rep = str(input('>> '))
    if rep == 'o':
        mode_dev = True
"""
FIN FONCTIONS DE DEV
"""
def game():
    global pion_select, ligne_in, colonne_in, num_dest, joueur
    damier = remplir_damier()

    clear_tdepl()

    dev()   #APPELER LES FONCTIONS DE DEV

    compt_pion()

    while True:
        if mode_dev == True:
            suppr_case()
            joueur = test_choix_joueur()  # type: ignore
            test_intervertir_case()
            test_choix_pion()
        
        
        global dbl_prise
        dbl_prise = False
        
        joueur , ligne_in , colonne_in = fcase_origine(damier,joueur)  # type: ignore

        while True:        
            copie_damier()

            test_prise(ligne_in,colonne_in,False)

            fdeplacement()
            
            tdame()
            
            compt_pion()
            
            if doit_prendre == False and dbl_prise == True:
                break
            
            show_damier_prise()
            
            if joueur == BLANC or joueur == NOIR or ((joueur == BLANC_DAME or joueur == NOIR_DAME) and doit_prendre == True):
                num_dest = in_case_dest()  # type: ignore
            if doit_prendre == False and (joueur == BLANC_DAME or joueur == NOIR_DAME):
                in_case_dame()
            
            fcase_depl()
            
            tdame()
            
            compt_pion()
            
            if doit_prendre == False:
                break
            
            dbl_prise = True
            
            ch_coord()
            
            tdame()
            
            compt_pion()
            
            tfin()
        
        ch_joueur()

game()

#TODO gestion fin de partie