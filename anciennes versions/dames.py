import numpy as np
from typing import Final
import sys

#constantes
DIM_DAMIER:Final[int] = 10  #dimension damier
NOIR:str = 'o'
NOIR_DAME:str = 'O'
BLANC:str = 'x'
BLANC_DAME:str = 'X'

#variables
case_dest:int
ligne_in:int
colonne_in:int
ligne_dest:int
colonne_dest:int

#creation damier 10x10
damier = np.empty([DIM_DAMIER,DIM_DAMIER],dtype = np.str_) 

#fonctions
def in_case_origine(damier:np.ndarray):  #demande de la case d'origine du pion + confirmation
    accept:str = 'n'
    while accept != 'o':
        case_origine:str = str(input('Insérez l\'emplacement d\'origine d\'une pièce (ligne colonne entre 0 et 9) : '))
        ligne , colonne = case_origine.split()
        ligne_in = int(ligne)
        colonne_in = int(colonne)
        while (colonne_in and ligne_in > 9) or (damier[ligne_in][colonne_in] == ' '):
            print('\n\nERREUR : Valeur incorecte !\n\n')
            print(damier)
            ligne = str(ligne_in)
            colonne = str(colonne_in)
            case_origine = input('Insérez l\'emplacement d\'origine d\'une pièce (ligne colonne entre 0 et 9) : ')
            ligne , colonne = case_origine.split()
            ligne_in = int(ligne)
            colonne_in = int(colonne)
            if colonne_in and ligne_in <= 9 or (damier[ligne_in][colonne_in] != ' '):
                print('Vous avez sélectionné la pièce |',damier[ligne_in][colonne_in],'| se situant ligne ',ligne_in,', colonne ',colonne_in,'. Confirmer ? (o/n)',sep='')
                accept = str(input('-> '))
                if accept == 'o':
                    return(ligne_in,colonne_in)
        if (colonne_in and ligne_in <= 9) or (damier[ligne_in][colonne_in] != ' '):
                print('Vous avez sélectionné la pièce |',damier[ligne_in][colonne_in],'| se situant ligne ',ligne_in,', colonne ',colonne_in,'. Confirmer ? (o/n)',sep='')
                accept = str(input('-> '))
                if accept == 'o':
                    return(ligne_in,colonne_in)

        #TODO : faire le test si la case est à côté en diagonale

def in_case_dest(damier:np.ndarray,ligne_in:int,colonne_in:int):    #demande de la case de destination + confirmation
    ligne_in = ligne_in
    colonne_in = colonne_in
    accept:str = 'n'
    test_dest_range:bool = False
    while accept != 'o':
        case_origine:str = str(input('Insérez l\'emplacement de destination d\'une pièce (ligne colonne entre 0 et 9) : '))
        ligne , colonne = case_origine.split()
        ligne_dest:int = int(ligne)
        colonne_dest:int = int(colonne)
        if (colonne_dest <= 9) and (ligne_dest <= 9) and (colonne_dest != colonne_in or ligne_dest != ligne_in):
            test_dest_range = True
            if damier[ligne_dest][colonne_dest] == ' ':
                print('Vous avez sélectionné l\'emplacement vide ligne ',ligne_dest,', colonne ',colonne_dest,'. Confirmer ? (o/n)',sep='')
            else:
                print('Vous avez sélectionné l\'emplacement contenant déjà le pion |',damier[ligne_dest][colonne_dest],'| ligne ',ligne_dest,', colonne ',colonne_dest,'. Confirmer ? (o/n)',sep='')
            accept = str(input('-> '))
            if accept == 'o':
                return(ligne_dest,colonne_dest)
        if (colonne_dest == colonne_in and ligne_dest == ligne_in):
            print('\n\nERREUR : Impossible de sélectionner le même emplacement que la pièce d\'origine !\n\n')
            print(damier)
        while (test_dest_range == False):
            if (colonne_dest != colonne_in or ligne_dest != ligne_in):
                print('\n\nERREUR : Valeur incorecte !\n\n')
                print(damier)
            ligne = str(ligne_dest)
            colonne = str(colonne_dest)
            case_origine = input('Insérez l\'emplacement d\'origine d\'une pièce (ligne colonne entre 0 et 9) : ')
            ligne , colonne = case_origine.split()
            ligne_dest:int = int(ligne)
            colonne_dest:int = int(colonne)
            if (colonne_dest <= 9) and (ligne_dest <= 9) and (colonne_dest != colonne_in or ligne_dest != ligne_in):
                test_dest_range = True
                if damier[ligne_dest][colonne_dest] == ' ':
                    print('Vous avez sélectionné l\'emplacement vide ligne ',ligne_dest,', colonne ',colonne_dest,'. Confirmer ? (o/n)',sep='')
                else:
                    print('Vous avez sélectionné l\'emplacement contenant déjà le pion |',damier[ligne_dest][colonne_dest],'| ligne ',ligne_dest,', colonne ',colonne_dest,'. Confirmer ? (o/n)',sep='')
                accept = str(input('-> '))
                if accept == 'o':
                    return(ligne_dest,colonne_dest)
            if (colonne_dest == colonne_in and ligne_dest == ligne_in):
                print('\n\nERREUR : Impossible de sélectionner le même emplacement que la pièce d\'origine !\n\n')
                print(damier)

#remplissage du damier
for i in range(0,4):    #les X
    for j in range(0,10):
        if i%2 == 0:
            if j%2 == 1:
                damier[i][j] = NOIR
            else:
                damier[i][j] = ' '
        else:
            if j%2 == 0:
                damier[i][j] = NOIR
            else:
                damier[i][j] = ' '

for i in range(0,2):    #espace entre X et O
    for j in range(1,10):
        damier[4+i] = ' '

for i in range(6,10):   #les O
    for j in range(0,10):
        if i%2 == 0:
            if j%2 == 1:
                damier[i][j] = BLANC
            else:
                damier[i][j] = ' '
        else:
            if j%2 == 0:
                damier[i][j] = BLANC
            else:
                damier[i][j] = ' '

print(damier)

#demande case d'origine
ligne_in , colonne_in = in_case_origine(damier)  # type: ignore

ligne_dest , colonne_dest = in_case_dest(damier,ligne_in,colonne_in)  # type: ignore

#TODO : vérifier lemplacement de destination du pion si elle est bien à côté en diagonale

#if __name__ == '__main__':
#    sys.exit(0)