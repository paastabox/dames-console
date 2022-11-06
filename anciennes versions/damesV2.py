import numpy as np
from typing import Final
import sys
import os

# python -m pip install rich
# module pour colorer le texte
from rich.console import Console
console = Console()

# os.system('mode con: cols=200 lines=49')

#constantes
DIM_DAMIER:Final[int] = 10  #dimension damier
DIM_PRISE:Final[int] = 5 
NOIR:str = '●'
NOIR_DAME:str = '▨'
BLANC:str = '○'
BLANC_DAME:str = '▢'
VIDE:str = ' '
PRISE_NONE:str = 'X'

#variables
ligne_in:int
colonne_in:int
ligne_dest:int
colonne_dest:int
joueur:str = BLANC  #definit à qui le tour
nb_pion_adverse:int = 0 #pour connaitre le nombre de pions à prendre ->
pion_select:str
doit_prendre:bool = False
prise_str:str
mode_dev:str

#creation damier 10x10
damier = np.empty([DIM_DAMIER,DIM_DAMIER],dtype = np.str_) 

#création d'un petit damier 3x3 pour afficher les propositions de prise
prise = np.empty([DIM_PRISE,DIM_PRISE],dtype = np.str_) 

#fonctions
def clear():    #efface ce qui est affiché dans la console (fonctionne sur windows, mac et linux)
    os.system('cls' if os.name == 'nt' else 'clear')

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

def fcase_origine(damier:np.ndarray,joueur:str):  #déroulé d'un tour

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
            print('\nInsérez l\'emplacement d\'origine d\'une pièce (ligne colonne entre 0 et 9)')
            try:
                case_origine:str = str(input('>> '))
                ligne , colonne = case_origine.split()
                ligne_in = int(ligne)
                colonne_in = int(colonne)
                break
            except ValueError:
                print('\nERREUR : Valeur incorrecte !\n')
        if (colonne_in and ligne_in > 9):
            print('\nERREUR : Valeur en dehors des limites du damier !\n')
        else:
            is_correct = True
            if damier[ligne_in][colonne_in] == VIDE:
                print('\nERREUR : Vous devez sélectionner un pion !\n')
            else:
                select_pion = True
                if (damier[ligne_in][colonne_in] != joueur):
                    print('\nERREUR : Ce n\'est pas votre tour !\n')
                else:
                    bon_pion = True
                    if joueur == BLANC:
                        if colonne_in == 0:
                            if (damier[ligne_in - 1][colonne_in + 1] == BLANC) or ((colonne_in == 0) and (damier[ligne_in - 1][colonne_in + 1] == BLANC_DAME)):
                                print('\nERREUR : Vous ne pouvez pas bouger ce pion !\n')
                            else:
                                deplacement_possible = True
                        elif colonne_in == 9:
                            if (colonne_in == 9 and (damier[ligne_in - 1][colonne_in - 1] == BLANC)) or (colonne_in == 9 and (damier[ligne_in - 1][colonne_in - 1] == BLANC_DAME)):
                                print('\nERREUR : Vous ne pouvez pas bouger ce pion !\n')
                            else:
                                deplacement_possible = True
                        elif (damier[ligne_in - 1][colonne_in - 1] and damier[ligne_in - 1][colonne_in + 1] == BLANC) or (damier[ligne_in - 1][colonne_in - 1] and damier[ligne_in - 1][colonne_in + 1] == BLANC_DAME):
                            print('\nERREUR : Vous ne pouvez pas bouger ce pion !\n')
                        else:
                            deplacement_possible = True
                    else:  
                        if colonne_in == 0:
                            if (damier[ligne_in + 1][colonne_in + 1] == NOIR) or (damier[ligne_in + 1][colonne_in + 1] == NOIR_DAME):
                                print('\nERREUR : Vous ne pouvez pas bouger ce pion !\n')
                            else:
                                deplacement_possible = True
                        elif colonne_in == 9:
                            if (damier[ligne_in + 1][colonne_in - 1] == NOIR) or (damier[ligne_in + 1][colonne_in - 1] == NOIR_DAME):
                                print('\nERREUR : Vous ne pouvez pas bouger ce pion !\n')
                            else:
                                deplacement_possible = True
                        elif (damier[ligne_in + 1][colonne_in - 1] and damier[ligne_in + 1][colonne_in + 1] == NOIR) or (damier[ligne_in + 1][colonne_in - 1] and damier[ligne_in + 1][colonne_in + 1] == NOIR_DAME):
                            print('\nERREUR : Vous ne pouvez pas bouger ce pion !\n')
                        else:
                            deplacement_possible = True 
                    if deplacement_possible == True:
                        print('Vous avez sélectionné la pièce |',damier[ligne_in][colonne_in],'| se situant ligne ',ligne_in,', colonne ',colonne_in,'. Confirmer ? (o/n)',sep='')
                        accept = str(input('>> '))
                        if accept == 'o':                        
                            return(damier[ligne_in][colonne_in],ligne_in,colonne_in)

def show_damier():     #affichage du damier
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

def clear_prise():  #clear le petit damier 3x3
    for i in range(DIM_PRISE):
        for j in range(DIM_PRISE):
            prise[i][j] = VIDE

def show_prise():   #Affiche le petit damier de prise 3x3 + remplit une chaine de caractère avec le petit damier 3x3
    global prise_str
    print('          ',end='')
    for i in range(DIM_PRISE):
        console.print(i,'  ',end='')
    print('\n')
    for i in range(DIM_PRISE):
        console.print('  ',i,'  ',end='')
        for j in range(DIM_PRISE):
            console.print('[bold blue] |[/bold blue]',prise[i][j],end='', style = "bold white")
        console.print(' |',end='',style='bold blue')
        print('\n')
    
    prise_str = '   '
    for i in range(DIM_PRISE):
        prise_str = prise_str + ' '
        prise_str = prise_str + str(i)
    prise_str = prise_str + '\n'
    for i in range(DIM_PRISE):
        prise_str = prise_str + '  '
        prise_str = prise_str + str(i)
        for j in range(DIM_PRISE):
            prise_str = prise_str + '|'
            prise_str = prise_str + prise[i][j]
        prise_str = prise_str + '|'
        prise_str = prise_str + '\n'

def ftest_prise():   #test si il y a des pions adverse à prendre pour le mettre dans le damier prise 3x3
    global doit_prendre, nb_pion_adverse
    clear_prise()
    if joueur == BLANC or joueur == BLANC_DAME: #test quand joueur = BLANC
        prise[2][2] = BLANC
        if (colonne_in == 0):
            for i in range(0,5):
                prise[i][0] = PRISE_NONE
            for i in range(0,4,2):
                if (damier[ligne_in - 1 + i][colonne_in + 1] == NOIR) or (damier[ligne_in - 1 + i][colonne_in + 1] == NOIR_DAME):
                    doit_prendre = True
                    nb_pion_adverse =+ 1
                    prise[i+1][3] = damier[ligne_in - 1 + i][colonne_in + 1]
        elif (colonne_in == 9):
            for i in range(0,5):
                prise[i][4] = PRISE_NONE
            for i in range(0,4,2):
                if (damier[ligne_in - 1 + i][colonne_in - 1] == NOIR) or (damier[ligne_in - 1 + i][colonne_in - 1] == NOIR_DAME):
                    doit_prendre = True
                    nb_pion_adverse =+ 1
                    prise[i+1][1] = damier[ligne_in - 1 + i][colonne_in - 1]
        else:
            for i in range(0,4,2):
                for j in range(0,4,2):
                    if (damier[ligne_in - 1 + i][colonne_in - 1 + j] == NOIR) or (damier[ligne_in - 1 + i][colonne_in - 1 + j] == NOIR_DAME):
                        doit_prendre = True
                        nb_pion_adverse =+ 1
                        prise[i+1][j+1] = damier[ligne_in - 1 + i][colonne_in - 1 + j]

    elif joueur == NOIR or joueur == NOIR_DAME:
        prise[2][2] = NOIR
        if colonne_in == 0:
            for i in range(0,4,2):
                if (damier[ligne_in - 1 + i][colonne_in + 1] == BLANC) or (damier[ligne_in - 1 + i][colonne_in + 1] == BLANC_DAME):
                    doit_prendre = True
                    nb_pion_adverse =+ 1
                    prise[i+1][3] = damier[ligne_in - 1 + i][colonne_in + 1]
        elif (colonne_in == 9):
            for i in range(0,4,2):
                if (damier[ligne_in - 1 + i][colonne_in - 1] == BLANC) or (damier[ligne_in - 1 + i][colonne_in - 1] == BLANC_DAME):
                    doit_prendre = True
                    nb_pion_adverse =+ 1
                    prise[i+1][1] = damier[ligne_in - 1 + i][colonne_in - 1]
        else:
            for i in range(0,4,2):
                for j in range(0,4,2):
                    if (damier[ligne_in - 1 + i][colonne_in - 1 + j] == BLANC) or (damier[ligne_in - 1 + i][colonne_in - 1 + j] == BLANC_DAME):
                        doit_prendre = True
                        nb_pion_adverse =+ 1
                        prise[i+1][j+1] = damier[ligne_in - 1 + i][colonne_in - 1 + j]

# def proposition_prise():
    

def test_intervertir_case():    #FONCTION DE TEST -> intervertir 2 cases
    clear()
    show_damier()
    temp:str
    console.print('case d\'origine\n',end='', style = "bold red")
    test_case_origine:str = str(input('>> '))
    x , y = test_case_origine.split()
    test_ligne_origine = int(x)
    test_colonne_origine = int(y)
    console.print('case de destination\n',end='', style = "bold red")
    test_case_dest:str = str(input('>> '))
    x,y = test_case_dest.split()
    test_ligne_dest = int(x)
    test_colonne_dest = int(y)
    test_pion_dest:str = damier[test_ligne_dest][test_colonne_dest]
    test_pion_origine:str = damier[test_ligne_origine][test_colonne_origine]

    temp = test_pion_dest
    damier[test_ligne_dest][test_colonne_dest] = test_pion_origine
    damier[test_ligne_origine][test_colonne_dest] = temp

def test_choix_joueur():    #FONCTION DE TEST -> choisir le joueur
    clear()
    show_damier()
    entete()
    console.print('choix du pion de départ\n',end='', style = "bold red")
    joueur:str = str(input('>> '))
    if joueur == 'blanc':
        return(BLANC)
    else:
        return(NOIR)

def entete():
    console.print('Les pions ',BLANC,' sont les pions blancs.\nLes pions ',NOIR,' sont les pions noirs.\n\n',end='',style='blue')

damier = remplir_damier()

if __name__ == '__main__':  #TOUT CE QUI EST DANS CE IF EST DESTINE A DU TEST ET DOIT ETRE IGNORE
    clear()
    console.print('Mode dev ? (o)\n',end='', style = "bold red")
    mode_dev = str(input('>> '))
    if mode_dev == 'o':
        joueur = test_choix_joueur()
        test_intervertir_case()

pion_select , ligne_in , colonne_in = fcase_origine(damier,joueur)  # type: ignore

ftest_prise()

show_prise()



#pip install console-menu
# Import the necessary packages
from consolemenu import *
from consolemenu.items import *

# Create the menu
menu = ConsoleMenu(prise_str)  # type: ignore

# Create some items

# MenuItem is the base class for all items, it doesn't do anything when selected
menu_item = MenuItem("Menu Item")

# A FunctionItem runs a Python function when selected
function_item = FunctionItem("Call a Python function", input, ["Enter an input"])

# A CommandItem runs a console command
command_item = CommandItem("Run a console command",  "touch hello.txt")

# A SelectionMenu constructs a menu from a list of strings
selection_menu = SelectionMenu(["item1", "item2", "item3"])


# Once we're done creating them, we just add the items to the menu
menu.append_item(menu_item)
menu.append_item(function_item)
menu.append_item(command_item)

# Finally, we call show to show the menu and allow the user to interact
menu.show()



from pick import pick
options = ['Java', 'JavaScript', 'Python', 'PHP', 'C++', 'Erlang', 'Haskell']

option, index = pick(options, prise_str, indicator='>> ', default_index=2)

print(prise)