import numpy as np
from typing import Final
import sys
import os

# python -m pip install rich
# module pour colorer le texte
from rich.console import Console
console = Console()

#constantes
DIM_DAMIER:Final[int] = 10  #dimension damier
DIM_DEPL:int = 4
NOIR:str = '○'
NOIR_DAME:str = '▨'
BLANC:str = '●'
BLANC_DAME:str = '▢'
VIDE:str = ' '

#variables
mode_dev:bool = False
ligne_in:int
colonne_in:int
ligne_dest:int
colonne_dest:int
nb_blanc:int
nb_noir:int
joueur:str = BLANC  #definit à qui le tour
nb_pion_adverse:int = 0 #pour connaitre le nombre de pions à prendre ->
pion_select:str
doit_prendre:bool = False
num_dest:int #numero pour le tableau de deplacement (tdepl)

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


#fonctions
def clear():    #efface ce qui est affiché dans la console (fonctionne sur windows, mac et linux)
    os.system('cls' if os.name == 'nt' else 'clear')

def clear_tdepl():    #initialise ou reset le tableau de deplacement
    for i in range(DIM_DEPL):
        tdepl[0][i] = 0
        tdepl[1][i] = -1
        tdepl[2][i] = -1

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

    clear()
    show_damier()

    accept:str = 'n'
    select_pion:bool = False
    bon_pion:bool = False
    is_correct:bool = False
    deplacement_possible:bool = False

    #demande case d'origine
    while accept != 'o' or is_correct != True or deplacement_possible != True or select_pion != True or bon_pion != True:
        accept = 'n'
        select_pion:bool = False
        bon_pion:bool = False
        is_correct = False
        deplacement_possible = False
        while True:
            console.print('Insérez l\'emplacement d\'origine d\'une pièce (ligne colonne entre 0 et 9)\n',end='',style='bold green')
            try:
                case_origine:str = str(input('>> '))
                ligne , colonne = case_origine.split()
                ligne_in = int(ligne)
                colonne_in = int(colonne)
                break
            except ValueError:
                console.print('\nERREUR : Valeur incorrecte !\n',style='bold red')
        if (colonne_in > 9 or ligne_in > 9):
            console.print('\nERREUR : Valeur en dehors des limites du damier !\n',style='bold red')
        else:
            is_correct = True
            if damier[ligne_in][colonne_in] == VIDE:
                console.print('\nERREUR : Vous devez sélectionner un pion !\n',style='bold red')
            else:
                select_pion = True
                if (damier[ligne_in][colonne_in] != joueur):
                    console.print('\nERREUR : Ce n\'est pas votre tour !\n',style='bold red')
                else:
                    bon_pion = True
                    
                    #SI JOUEUR == BLANC
                    if joueur == BLANC:
                        if colonne_in == 0:
                            if (damier[ligne_in - 1][colonne_in + 1] == BLANC) or ((colonne_in == 0) and (damier[ligne_in - 1][colonne_in + 1] == BLANC_DAME)):
                                console.print('\nERREUR : Vous ne pouvez pas bouger ce pion !\n',style='bold red')
                            elif (damier[ligne_in - 1][colonne_in + 1] == NOIR or damier[ligne_in - 1][colonne_in + 1] == NOIR_DAME) and (damier[ligne_in - 2][colonne_in + 2] == NOIR or damier[ligne_in - 2][colonne_in + 2] == NOIR_DAME or damier[ligne_in - 2][colonne_in + 2] == BLANC or damier[ligne_in - 2][colonne_in + 2] == BLANC_DAME):
                                console.print('\nERREUR : Vous ne pouvez pas bouger ce pion !\n',style='bold red')
                            else:
                                deplacement_possible = True
                        elif colonne_in == 9:
                            if (damier[ligne_in - 1][colonne_in - 1] == BLANC) or (damier[ligne_in - 1][colonne_in - 1] == BLANC_DAME):
                                console.print('\nERREUR : Vous ne pouvez pas bouger ce pion !\n',style='bold red')
                            elif (damier[ligne_in - 1][colonne_in - 1] == NOIR or damier[ligne_in - 1][colonne_in - 1] == NOIR_DAME) and (damier[ligne_in - 2][colonne_in - 2] == NOIR or damier[ligne_in - 2][colonne_in - 2] == NOIR_DAME or damier[ligne_in - 2][colonne_in - 2] == BLANC or damier[ligne_in - 2][colonne_in - 2] == BLANC_DAME):
                                console.print('\nERREUR : Vous ne pouvez pas bouger ce pion !\n',style='bold red')
                            else:
                                deplacement_possible = True
                        elif (damier[ligne_in - 1][colonne_in - 1] == BLANC and damier[ligne_in - 1][colonne_in + 1] == BLANC) or (damier[ligne_in - 1][colonne_in - 1] == BLANC_DAME and damier[ligne_in - 1][colonne_in + 1] == BLANC_DAME):
                            console.print('\nERREUR : Vous ne pouvez pas bouger ce pion !\n',style='bold red')
                        elif colonne_in == 1 and (damier[ligne_in - 1][colonne_in - 1] == BLANC or damier[ligne_in - 1][colonne_in - 1] == BLANC_DAME or damier[ligne_in - 1][colonne_in - 1] == NOIR or damier[ligne_in - 1][colonne_in - 1] == NOIR_DAME) and ((damier[ligne_in - 1][colonne_in + 1] == BLANC or damier[ligne_in - 1][colonne_in + 1] == BLANC_DAME or damier[ligne_in - 1][colonne_in + 1] == NOIR or damier[ligne_in - 1][colonne_in + 1] == NOIR_DAME) and (damier[ligne_in - 2][colonne_in + 2] == BLANC or damier[ligne_in - 2][colonne_in + 2] == BLANC_DAME or damier[ligne_in - 2][colonne_in + 2] == NOIR or damier[ligne_in - 2][colonne_in + 2] == NOIR_DAME)):
                            console.print('\nERREUR : Vous ne pouvez pas bouger ce pion !\n',style='bold red')
                        elif colonne_in == 8 and (damier[ligne_in - 1][colonne_in + 1] == BLANC or damier[ligne_in - 1][colonne_in + 1] == BLANC_DAME or damier[ligne_in - 1][colonne_in + 1] == NOIR or damier[ligne_in - 1][colonne_in + 1] == NOIR_DAME) and (damier[ligne_in - 1][colonne_in - 1] == BLANC or damier[ligne_in - 1][colonne_in - 1] == BLANC_DAME or damier[ligne_in - 1][colonne_in - 1] == NOIR or damier[ligne_in - 1][colonne_in - 1] == NOIR_DAME) and (damier[ligne_in - 2][colonne_in - 2] == BLANC or damier[ligne_in - 2][colonne_in - 2] == BLANC_DAME or damier[ligne_in - 2][colonne_in - 2] == NOIR or damier[ligne_in - 2][colonne_in - 2] == NOIR_DAME):
                            console.print('\nERREUR : Vous ne pouvez pas bouger ce pion !\n',style='bold red')
                        elif (damier[ligne_in - 1][colonne_in - 1] == BLANC or damier[ligne_in - 1][colonne_in - 1] == BLANC_DAME or damier[ligne_in - 1][colonne_in - 1] == NOIR or damier[ligne_in - 1][colonne_in - 1] == NOIR_DAME) and (damier[ligne_in - 1][colonne_in + 1] == BLANC or damier[ligne_in - 1][colonne_in + 1] == BLANC_DAME or damier[ligne_in - 1][colonne_in + 1] == NOIR or damier[ligne_in - 1][colonne_in + 1] == NOIR_DAME) and (damier[ligne_in - 2][colonne_in - 2] == BLANC or damier[ligne_in - 2][colonne_in - 2] == BLANC_DAME or damier[ligne_in - 2][colonne_in - 2] == NOIR or damier[ligne_in - 2][colonne_in - 2] == NOIR_DAME) and (damier[ligne_in - 2][colonne_in + 2] == BLANC or damier[ligne_in - 2][colonne_in + 2] == BLANC_DAME or damier[ligne_in - 2][colonne_in + 2] == NOIR or damier[ligne_in - 2][colonne_in + 2] == NOIR_DAME):
                            console.print('\nERREUR : Vous ne pouvez pas bouger ce pion !\n',style='bold red')
                        else:
                            deplacement_possible = True
                            
                    #SI JOUEUR == NOIR
                    else:
                        if colonne_in == 0:
                            if (damier[ligne_in + 1][colonne_in + 1] == NOIR) or (damier[ligne_in + 1][colonne_in + 1] == NOIR_DAME):
                                console.print('\nERREUR : Vous ne pouvez pas bouger ce pion !\n',style='bold red')
                            elif (damier[ligne_in + 1][colonne_in + 1] == BLANC or damier[ligne_in + 1][colonne_in + 1] == BLANC_DAME) and (damier[ligne_in + 2][colonne_in + 2] == NOIR or damier[ligne_in + 2][colonne_in + 2] == NOIR_DAME or damier[ligne_in + 2][colonne_in + 2] == BLANC or damier[ligne_in + 2][colonne_in + 2] == BLANC_DAME):
                                console.print('\nERREUR : Vous ne pouvez pas bouger ce pion !\n',style='bold red')
                            else:
                                deplacement_possible = True
                        elif colonne_in == 9:
                            if (damier[ligne_in + 1][colonne_in - 1] == NOIR) or (damier[ligne_in + 1][colonne_in - 1] == NOIR_DAME):
                                console.print('\nERREUR : Vous ne pouvez pas bouger ce pion !\n',style='bold red')
                            elif (damier[ligne_in + 1][colonne_in - 1] == BLANC or damier[ligne_in + 1][colonne_in - 1] == BLANC_DAME) and (damier[ligne_in + 2][colonne_in - 2] == NOIR or damier[ligne_in + 2][colonne_in - 2] == NOIR_DAME or damier[ligne_in + 2][colonne_in - 2] == BLANC or damier[ligne_in + 2][colonne_in - 2] == BLANC_DAME):
                                console.print('\nERREUR : Vous ne pouvez pas bouger ce pion !\n',style='bold red')
                            else:
                                deplacement_possible = True
                        elif (damier[ligne_in + 1][colonne_in - 1] == NOIR and damier[ligne_in + 1][colonne_in + 1] == NOIR) or (damier[ligne_in + 1][colonne_in - 1] == NOIR_DAME and damier[ligne_in + 1][colonne_in + 1] == NOIR_DAME):
                            console.print('\nERREUR : Vous ne pouvez pas bouger ce pion !\n',style='bold red')
                        elif colonne_in == 1 and (damier[ligne_in + 1][colonne_in - 1] == NOIR or damier[ligne_in + 1][colonne_in - 1] == NOIR_DAME or damier[ligne_in + 1][colonne_in - 1] == BLANC or damier[ligne_in + 1][colonne_in - 1] == BLANC_DAME) and (damier[ligne_in + 1][colonne_in + 1] == NOIR or damier[ligne_in + 1][colonne_in + 1] == NOIR_DAME or damier[ligne_in + 1][colonne_in + 1] == BLANC or damier[ligne_in + 1][colonne_in + 1] == BLANC_DAME) and (damier[ligne_in + 2][colonne_in + 2] == NOIR or damier[ligne_in + 2][colonne_in + 2] == NOIR_DAME or damier[ligne_in + 2][colonne_in + 2] == BLANC or damier[ligne_in + 2][colonne_in + 2] == BLANC_DAME):
                            console.print('\nERREUR : Vous ne pouvez pas bouger ce pion !\n',style='bold red')
                        elif colonne_in == 8 and (damier[ligne_in + 1][colonne_in - 1] == NOIR or damier[ligne_in + 1][colonne_in - 1] == NOIR_DAME or damier[ligne_in + 1][colonne_in - 1] == BLANC or damier[ligne_in + 1][colonne_in - 1] == BLANC_DAME) and (damier[ligne_in + 2][colonne_in - 2] == NOIR or damier[ligne_in + 2][colonne_in - 2] == NOIR_DAME or damier[ligne_in + 2][colonne_in - 2] == BLANC or damier[ligne_in + 2][colonne_in - 2] == BLANC_DAME) and (damier[ligne_in + 1][colonne_in + 1] == NOIR or damier[ligne_in + 1][colonne_in + 1] == NOIR_DAME or damier[ligne_in + 1][colonne_in + 1] == BLANC or damier[ligne_in + 1][colonne_in + 1] == BLANC_DAME):
                            console.print('\nERREUR : Vous ne pouvez pas bouger ce pion !\n',style='bold red')
                        elif (damier[ligne_in + 1][colonne_in - 1] == NOIR or damier[ligne_in + 1][colonne_in - 1] == NOIR_DAME or damier[ligne_in + 1][colonne_in - 1] == BLANC or damier[ligne_in + 1][colonne_in - 1] == BLANC_DAME) and (damier[ligne_in + 2][colonne_in - 2] == NOIR or damier[ligne_in + 2][colonne_in - 2] == NOIR_DAME or damier[ligne_in + 2][colonne_in - 2] == BLANC or damier[ligne_in + 2][colonne_in - 2] == BLANC_DAME) and (damier[ligne_in + 1][colonne_in + 1] == NOIR or damier[ligne_in + 1][colonne_in + 1] == NOIR_DAME or damier[ligne_in + 1][colonne_in + 1] == BLANC or damier[ligne_in + 1][colonne_in + 1] == BLANC_DAME) and (damier[ligne_in + 2][colonne_in + 2] == NOIR or damier[ligne_in + 2][colonne_in + 2] == NOIR_DAME or damier[ligne_in + 2][colonne_in + 2] == BLANC or damier[ligne_in + 2][colonne_in + 2] == BLANC_DAME):
                            console.print('\nERREUR : Vous ne pouvez pas bouger ce pion !\n',style='bold red')
                        else:
                            deplacement_possible = True 
                    if deplacement_possible == True:
                        console.print('\nVous avez sélectionné la pièce |',damier[ligne_in][colonne_in],'| se situant ligne ',ligne_in,', colonne ',colonne_in,'. Confirmer ? [cyan](o/n)[/cyan]',sep='',style='bold green')
                        accept = str(input('>> '))
                        if accept == 'o':                        
                            return(damier[ligne_in][colonne_in],ligne_in,colonne_in)

def test_prise():   #test si il y a des pions adverse à prendre
    clear_tdepl()
    global doit_prendre, nb_pion_adverse
    nb_pion_adverse = 0
    doit_prendre = False
    if joueur == BLANC:
        if (colonne_in == 0 or colonne_in == 1):
            if ligne_in == 9:
                if (damier[ligne_in - 1][colonne_in + 1] == NOIR or damier[ligne_in - 1][colonne_in + 1] == NOIR_DAME) and damier[ligne_in - 2][colonne_in + 2] == VIDE:
                    doit_prendre = True
                    nb_pion_adverse += 1
                    tdepl[0][1] = 1
                    tdepl[1][1] = ligne_in - 2
                    tdepl[2][1] = colonne_in + 2
            else:
                for i in range(0,4,2):
                    if ((damier[ligne_in - 1 + i][colonne_in + 1] == NOIR) or (damier[ligne_in - 1 + i][colonne_in + 1] == NOIR_DAME)) and damier[ligne_in - 2 + (i*2)][colonne_in + 2] == VIDE:
                        doit_prendre = True
                        nb_pion_adverse += 1
                        tdepl[0][1+i] = 1
                        tdepl[1][1+i] = ligne_in - 2 + i * 2
                        tdepl[2][1+i] = colonne_in + 2
        elif (colonne_in == 9 or colonne_in == 8):
            if ligne_in == 9:
                if (damier[ligne_in - 1][colonne_in - 1] == NOIR or damier[ligne_in - 1][colonne_in - 1] == NOIR_DAME) and damier[ligne_in - 2][colonne_in - 2] == VIDE:
                    doit_prendre = True
                    nb_pion_adverse += 1
                    tdepl[0][0] = 1
                    tdepl[1][0] = ligne_in - 2
                    tdepl[2][0] = colonne_in - 2
            else:
                for i in range(0,4,2):
                    if ((damier[ligne_in - 1 + i][colonne_in - 1] == NOIR) or (damier[ligne_in - 1 + i][colonne_in - 1] == NOIR_DAME)) and damier[ligne_in - 2 + (i*2)][colonne_in - 2] == VIDE:
                        doit_prendre = True
                        nb_pion_adverse += 1
                        tdepl[0][0+i] = 1
                        tdepl[1][0+i] = ligne_in - 2 + i * 2
                        tdepl[2][0+i] = colonne_in - 2
        else:
            if ligne_in == 9:
                for i in range(0,4,2):
                    if (damier[ligne_in - 1][colonne_in - 1 + i] == NOIR or damier[ligne_in - 1][colonne_in - 1 + i] == NOIR_DAME) and damier[ligne_in - 2][colonne_in - 2 + (i*2)] == VIDE:
                        doit_prendre = True
                        nb_pion_adverse += 1
                        tdepl[0][0+int(i/2)] = 1
                        tdepl[1][0+int(i/2)] = ligne_in - 2
                        tdepl[2][0+int(i/2)] = colonne_in - 2 + i * 2
            else:
                for i in range(0,4,2):
                    for j in range(0,4,2):
                        if ((damier[ligne_in - 1 + i][colonne_in - 1 + j] == NOIR) or (damier[ligne_in - 1 + i][colonne_in - 1 + j] == NOIR_DAME)) and damier[ligne_in - 2 + (i * 2)][colonne_in - 2 + (j*2)] == VIDE:
                            doit_prendre = True
                            nb_pion_adverse += 1
                            tdepl[0][0+int(j/2)+i] = 1
                            tdepl[1][0+int(j/2)+i] = ligne_in - 2 + i * 2
                            tdepl[2][0+int(j/2)+i] = colonne_in - 2 + j * 2
                            
    elif joueur == NOIR:
        if colonne_in == 0 or colonne_in == 1:
            if ligne_in == 0:
                if (damier[ligne_in + 1][colonne_in + 1] == BLANC or damier[ligne_in + 1][colonne_in + 1] == BLANC_DAME) and damier[ligne_in + 2][colonne_in + 2] == VIDE:
                    doit_prendre = True
                    nb_pion_adverse += 1
                    tdepl[0][3] = 1
                    tdepl[1][3] = ligne_in + 2
                    tdepl[2][3] = colonne_in + 2
            else:
                for i in range(0,4,2):
                    if (damier[ligne_in - 1 + i][colonne_in + 1] == BLANC) or (damier[ligne_in - 1 + i][colonne_in + 1] == BLANC_DAME) and damier[ligne_in - 1 + (i*2)][colonne_in + 2] == VIDE:
                        doit_prendre = True
                        nb_pion_adverse += 1
                        tdepl[0][1+i] = 1
                        tdepl[1][1+i] = ligne_in - 2 + i * 2
                        tdepl[2][1+i] = colonne_in + 2
        elif (colonne_in == 9 or colonne_in == 8):
            if ligne_in == 0:
                if (damier[ligne_in + 1][colonne_in - 1] == BLANC or damier[ligne_in + 1][colonne_in - 1] == BLANC_DAME) and damier[ligne_in + 2][colonne_in - 2] == VIDE:
                    doit_prendre = True
                    nb_pion_adverse += 1
                    tdepl[0][2] = 1
                    tdepl[1][2] = ligne_in + 2
                    tdepl[2][2] = colonne_in - 2
            else:
                for i in range(0,4,2):
                    if (damier[ligne_in - 1 + i][colonne_in - 1] == BLANC) or (damier[ligne_in - 1 + i][colonne_in - 1] == BLANC_DAME) and (damier[ligne_in - 2 + (i*2)][colonne_in - 2] == VIDE):
                        doit_prendre = True
                        nb_pion_adverse += 1
                        tdepl[0][0+i] = 1
                        tdepl[1][0+i] = ligne_in - 2 + i * 2
                        tdepl[2][0+i] = colonne_in - 2
        else:
            if ligne_in == 0:
                for i in range(0,4,2):
                    if (damier[ligne_in + 1][colonne_in - 1 + i] == NOIR or damier[ligne_in + 1][colonne_in - 1 + i] == NOIR_DAME) and damier[ligne_in + 2][colonne_in - 2 + (i*2)] == VIDE:
                        doit_prendre = True
                        nb_pion_adverse += 1
                        tdepl[0][2+int(i/2)] = 1
                        tdepl[1][2+int(i/2)] = ligne_in + 2
                        tdepl[2][2+int(i/2)] = colonne_in - 2 + i * 2
            else:
                for i in range(0,4,2):
                    for j in range(0,4,2):
                        if ((damier[ligne_in - 1 + i][colonne_in - 1 + j] == BLANC) or (damier[ligne_in - 1 + i][colonne_in - 1 + j] == BLANC_DAME)) and damier[ligne_in - 2 + (i * 2)][colonne_in - 2 + (j*2)] == VIDE:
                            doit_prendre = True
                            nb_pion_adverse += 1
                            tdepl[0][0+int(j/2)+i] = 1
                            tdepl[1][0+int(j/2)+i] = ligne_in - 2 + i * 2
                            tdepl[2][0+int(j/2)+i] = colonne_in - 2 + j * 2

def fdeplacement():   #fait les propositions quand il n'y a pas de pion à prendre
    if doit_prendre == False:
        global num_dest
        clear_tdepl()
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
        else:
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
    for i in range(4):
        if tdepl[0][i] == 1:
            damier_prise[tdepl[1][i]][tdepl[2][i]] = str(i + 1)

def in_case_dest(): #demande le numero de deplacement proposé avec tests (num_dest = in_case_dest())
    depl_ok:bool = False
    nb_deplacement:int = 0
    for i in range(4):
        if tdepl[0][i] == 1:
            nb_deplacement += 1
    while depl_ok == False:
        while True:
            nb_try:int = 0
            console.print('\nInsérez le numéro de la case de destination\n',end='',style='bold green')
            try:
                num_dest = int(input('>> ')) - 1
                break
            except ValueError:
                console.print('\nERREUR : Valeur incorrecte !\n',style='bold red')
        for i in range(4):
            if tdepl[0][i] == 1:
                if (num_dest + 1) < 1 or (num_dest + 1) > 4 or (str((num_dest + 1)) != str(damier_prise[tdepl[1][i]][tdepl[2][i]])): #faire le test avec les valeur sdu tableau plus haut
                    nb_try += 1
                    if nb_try == nb_deplacement:
                        console.print('\nERREUR : Valeur incorrecte !\n',style='bold red')
                        break
                else:
                    depl_ok = True
                    return(num_dest)

def fcase_depl():   #deplacement d'un pion vers une case vide
    if doit_prendre == True:
        damier[tdepl[1][num_dest]][tdepl[2][num_dest]] = damier[ligne_in][colonne_in]
        damier[ligne_in][colonne_in] = VIDE
        damier[int((tdepl[1][num_dest]+ligne_in)/2)][int((tdepl[2][num_dest]+colonne_in)/2)] = VIDE
    else:
        damier[tdepl[1][num_dest]][tdepl[2][num_dest]] = damier[ligne_in][colonne_in]
        damier[ligne_in][colonne_in] = VIDE

def show_damier():     #affichage du damier stylisé (rich console)
    if mode_dev == True:
        console.print('MODE DEV ACTIF\n\n',end='',style='bold red italic')
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
    if mode_dev == True:
        console.print('MODE DEV ACTIF\n\n',end='',style='bold red italic')
    clear()
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
    if joueur == BLANC:
        joueur = NOIR
    else:
        joueur = BLANC

def compt_pion():   #compte le nombre de pions blanc / noirs dans le plateau -> nb_blanc/nb_noir
    global nb_blanc, nb_noir
    nb_blanc = 0
    nb_noir = 0
    for i in range(DIM_DAMIER):
        for j in range(DIM_DAMIER):
            if damier[i][j] == BLANC:
                nb_blanc += 1
            elif damier[i][j] == NOIR:
                nb_noir += 1

"""
FONCTIONS DE DEV
"""
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

damier = remplir_damier()

clear_tdepl()

dev()   #APPELER LES FONCTIONS DE DEV

show_damier()

entete()

while 1:
    if mode_dev == True:
        joueur = test_choix_joueur()  # type: ignore
        test_intervertir_case()
    

    copie_damier()
    
    pion_select , ligne_in , colonne_in = fcase_origine(damier,joueur)  # type: ignore

    test_prise()

    fdeplacement()
    
    show_damier_prise()
    
    num_dest = in_case_dest()  # type: ignore
    
    fcase_depl()
    
    compt_pion()
    
    ch_joueur()

    show_damier()
    
    #TODO prise obligatoire
    #TODO gestion fin de partie
    #TODO dames au bout du plateau
    