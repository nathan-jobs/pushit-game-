from upemtk import *
from copy import deepcopy
import os
from random import randint
def coin_bas(i, j, k, lb, hb):
    """
    Cette fonction calcule les coordonnées, en pixels, du coin le plus bas 
    d'un bloc représenté par le triplet (i, j, k), où i est le numéro de 
    ligne et j le numéro de colonne de la case sur laquelle est posé le bloc, 
    et k est sa hauteur. Elle reçoit également les dimensions lb et hb d'un 
    bloc. 
    """

   
    x = taille_x/2 + (j-i) * lb
    y = taille_y/2 + (j+i) * lb//2 - (k-1) * hb + lb
    return x, y


def affiche_bloc(i, j, k, lb, hb, couleur="white"):
    """
    Cette fonction affiche le bloc de coordonnées (i, j, k) conformément au
    
    
    schéma donné dans le sujet. Elle reçoit également les dimensions lb et hb 
    d'un bloc, la taille n du plateau ainsi qu'un paramètre optionnel c 
    indiquant la couleur de la face supérieure du bloc. 
    """

    # calcul des coordonnées du coin bas du bloc
    x, y = coin_bas(i, j, k, lb, hb)
    # calcul des coordonnées des autres sommets inférieurs du bloc
    xg, xd, ymb = x - lb, x + lb, y - lb//2
    # calcul des ordonnées des sommets supérieurs
    ybh, ymh, yhh = y - hb, y - lb//2 - hb, y - lb - hb

    # dessin de la face supérieure, en vert si c'est l'arrivée
    face_haut = [(x, ybh), (xd, ymh), (x,  yhh), (xg, ymh)]
    polygone(face_haut, remplissage=couleur, epaisseur=2)

    # dessin des faces latérales si hauteur non nulle
    if k > 0:
        face_gauche = [(x, y),   (xg, ymb), (xg, ymh), (x,  ybh)]
        face_droite = [(x, y),   (xd, ymb), (xd, ymh), (x,  ybh)]
        polygone(face_gauche, remplissage='white')
        polygone(face_droite, remplissage='white')


def affiche_bille(i, j, k, lb, hb, n):
    """
    Cette fonction affiche la bille aux coordonnées (i, j, k). Elle reçoit 
    également les dimensions lb et hb d'un bloc ainsi que la taille n du 
    plateau. 
    """

    # dessin de la bille proprement dite
    x, y = coin_bas(i, j, k, lb, hb)
    cercle(x, y - 2*lb//3, lb//3, couleur="red", remplissage="red")

    # repère vertical pour une meilleure visibilité
    ligne(x, y - 2*lb//3, x, 20, couleur='red')

    # flèche-repère de gauche
    x, y = coin_bas(n-1, j-0.5, 1, lb, hb)
    fleche(x - 20, y + 20, x - 10, y + 10,
           couleur="red", epaisseur=3)

    # flèche-repère  de droite
    x, y = coin_bas(i-0.5, n-1, 1, lb, hb)
    fleche(x + 20, y + 20, x + 10, y + 10,
           couleur="red", epaisseur=3)


def lecture_fichier(mon_fichier):
	"""cette fonction permet de lire le fichier txt pris en paramètre renvoie une liste des listes et la hauteur max"""
	liste_retour = []
	maxi_retour =  0
	element = open(mon_fichier , "r")
	for elem in element :
		elem2 = elem.split()
		for car in range(len(elem2)):
			elem2[car] = int(elem2[car])
		maxi = max(elem2)
		if maxi>maxi_retour:
			maxi_retour = maxi
		liste_retour.append(elem2)
	return liste_retour , maxi_retour

def dessine_stage(lb, hb, n, i, j):
	"""dessine le stage du jeu on utilise deux compteurs parce que c'est le moyen le plus simple de gerer une liste des listes"""
	for cmpt in range(n) :
		for cmpt1 in range(n) :
			for c in range(bloc[cmpt][cmpt1]) :
				affiche_bloc(cmpt, cmpt1, c, lb, hb)
			affiche_bloc(cmpt, cmpt1, bloc[cmpt][cmpt1], lb, hb, couleur = 'gray')
			if i == cmpt and j == cmpt1 :
				affiche_bille(i, j, bloc[i][j] + 1, lb, hb, n)
			elif cmpt == (n - 1) and cmpt1 == (n - 1) :
				affiche_bloc(cmpt, cmpt1, bloc[cmpt][cmpt1], lb, hb, couleur = "green")
			
		

def mon_jeu (evt,n,i,j,bloc):
	"""c'est la fonction qui gère les deplacements avec plusieurs tests pour eviter le debordement de la bille"""
	coup=-1# on commence à -1 parce qu au premier appel de la fonction on veut avoir 0 comme nombre de coup
	while True :
		coup+=1
		efface_tout() 
		affiche_texte_bis()
		texte(200, 20, 'stage' + str(stage + 1), 'grey', taille = 30)
		texte(25, 0, str(coup)+ " " +'COUP(S)',police = "Garamond")#le nombre de coups
		dessine_stage(lb, hb, n, i, j)
		evt = attente_touche()#on attend la touche de l'utilisateur
		a=[i,j] # on recupère la liste des tuples de nouvelles positions
		stock.append(a) #on copie sur une liste stock
		
		if evt == "Left":			
			if j == 0 :
				bloc[i][j] = bloc[i][j]
			elif bloc[i][j - 1] > bloc[i][j] + 1 :
				bloc[i][j-1] = bloc[i][j]+1
			elif bloc[i][j - 1] == bloc[i][j] + 1 :
				if (j - 1) == 0 :
					bloc[i][j-1] = bloc[i][j]+1
				elif bloc[i][j - 2] < bloc[i][j - 1] :
					bloc[i][j - 2] += 1
					bloc[i][j - 1] -= 1
			elif bloc[i][j - 1] < (bloc[i][j] - 1) :
				bloc[i][j-1] = bloc[i][j]-1       
			else :
				j = j - 1
				if i == n-1 and j== n-1:
					return ["winner",coup] #ce resultat sera recupérer dans le main cette façon de faire nous epargne des erreurs 
					#dans le terminal
		elif evt == "Right":		
			if j == (n - 1) :
				bloc[i][j] = bloc[i][j]    
			elif bloc[i][j + 1] > bloc[i][j] +1 :
				bloc[i][j+1] = bloc[i][j]+1
			elif bloc[i][j + 1] == bloc[i][j] + 1 :
				if (j + 1) == (n - 1):
					pass 
				elif bloc[i][j + 2] < bloc[i][j + 1] :
					bloc[i][j + 2] += 1
					bloc[i][j + 1] -= 1
			elif bloc[i][j + 1] < (bloc[i][j] - 1) :
				pass
			else :
				j = j + 1
				if i == n-1 and j== n-1:
					return ["winner",coup]
		elif evt == "Up":
			
			if i == 0 :
				bloc[i][j] = bloc[i][j]
			elif bloc[i - 1][j] > bloc[i][j] + 1 :
				bloc[i-1][j] = bloc[i][j]+1
			elif bloc[i - 1][j] == bloc[i][j] + 1 :
				if (i - 1) == 0 :
					bloc[i-1][j] =  bloc[i][j]+1
				elif bloc[i - 2][j] < bloc[i - 1][j] :
				
					bloc[i - 2][j] += 1
					bloc[i - 1][j] -= 1
			elif bloc[i - 1][j] < (bloc[i][j] - 1) :
				bloc[i-1][j] = bloc[i][j]-1
			else :
				i = i - 1
				if i == n-1 and j== n-1:
					return ["winner",coup]
		elif evt == "Down":
			if i == (n - 1) :
				bloc[i][j] = bloc[i][j]
			elif bloc[i + 1][j] > bloc[i][j] + 1 :
				bloc[i+1][j] = bloc[i][j]+1
			elif bloc[i + 1][j] == bloc[i][j] + 1 :
				if (i + 1) == (n - 1) :
					bloc[i+1][j] = bloc[i+1][j]+1
				elif bloc[i + 2][j] < bloc[i + 1][j] :
					bloc[i + 2][j] += 1
					bloc[i + 1][j] -= 1
			elif bloc[i + 1][j] < (bloc[i][j] - 1) :
				bloc[i+1][j] = bloc[i][j]-1
			else :
				i = i + 1
				if i == n-1 and j== n-1:
					return ["winner",coup]
					
		elif evt == "a":
			stock.pop()
			i,j=stock[-1]
			stock.pop()			
			coup-=2 # lorsqu'on annule un deplacement on retranche le nombre de coups
		
		else:
			return evt  #si l'utilisateur appuie sur une autre touche 
		mise_a_jour()
def victoire(coup) :
	"""une petite fonction optionnelle qui affiche un message à chaque stage reussi"""
	efface_tout()	
	texte(210, 260, 'Félicitation !', 'brown', police='Garamond')
	texte(0, 300, 'Vous avez gagné ce niveau en '+str(coup)+' coups','darkblue', taille = 22, police='Garamond')
	texte(450, 10, 'R : Retry\nN : Next\nQ : Quit', 'brown', taille=22, police = 'Garamond')
	evt = attente_touche()
	return evt 
	mise_a_jour()
def affiche_texte() :
    texte(300, 300, 'Push it Down !', 'brown',ancrage = "center", taille = 35, police = 'Garamond')
    attente_clic()
    efface_tout()
    texte(300,300, 'Cliquer pour commencer le jeu', 'brown', ancrage = "center", police = "Garamond")
    attente_clic()
    efface_tout()

def affiche_texte_bis() :
    """un petit manuel d'utilisation"""
    largeur = 150
    texte(450, 10, 'R : Retry\nN : Next\nP : Previous\nA : Annuler\nQ : Quit',taille = 15, police = 'Tahoma')
def affiche_menu() :
		"""notre menu au debut du jeu"""
		texte(300,300,"Mode normal avec mes niveaux : appuie sur  m",'darkblue',ancrage = "center",taille = 17,police = "Tahoma")
		texte(300,350,"Mode aléatoire avec un générateur : appuie sur g",'darkblue',ancrage = "center",taille = 17,police = "Tahoma")
		touche = attente_touche()
		return touche
		attente_clic()
		efface_cercle()
        			
def generateur(lst):
	"""mon generateur aléatoire de stage avec un nombre aléatoire"""
	maxi_retour = 0
	x = randint(3,8) # un nombre aléatoire fixé pour la longueur de la liste
	for i in range(x):
		liste = []
		for j in range(x):
			nombre=randint(0,5)# à chaque tour un nombre est choisi pour eviter la redondance des éléments
			liste.append(nombre)
		"""maxi = max(liste) # on récupère le max de chaque liste 
		if maxi>maxi_retour:#un petit test pour s'assurer qu'on a bel et bien le max
			maxi_retour = maxi"""
		lst.append(liste)
	return lst #, maxi_retour
def restart_game():
	"""pour eviter l'erreur " liste index out of range" on crée une fonction qu'on appelera à la fin du jeu"""
	efface_tout()
	texte(200,260, 'THE END !', couleur='brown', taille=20, police = 'Garamond') 
	texte(300, 10, 'w : Retry the Game\n   Q : Quit', couleur = "brown", taille=20, police = 'Garamond')
	evt = attente_touche()
	return evt
	mise_a_jour()
def solver ( lst , position , N ):
	 #mauvais solver il renvoie toujours None
	if position == ( N - 1 , N - 1 ):
		return [ ( N - 1 , N - 1 ) ] 
	x , y = position 
	if x + 1 < N and lst [ x + 1 ][ y ] >= 1 : 
		a = solver ( lst, ( x + 1 , y ) , N ) 
		if a != None : 
			return [ ( x , y ) ] + a
	if y + 1 < N and lst [ x ][ y + 1 ] >= 1 : 
		b = solver ( lst , ( x , y + 1 ) , N ) 
		if b != None : 
			return [ ( x , y ) ] +b 
	if x - 1 < N and lst [ x - 1 ][ y ] >= 1 : 
		a = solver ( lst , ( x - 1 , y ) , N ) 
		if a != None : 
			return [ ( x , y ) ] + a
	if y - 1 < N and lst [ x ][ y - 1 ] >= 1 : 
		b = solver ( lst , ( x , y - 1 ) , N ) 
		if b != None : 
			return [ ( x , y ) ] + b 
	
if __name__ == "__main__":
	taille_x = 600
	taille_y = 600
	cree_fenetre(taille_x, taille_y)
	affiche_texte()
    # Chemin pour accéder aux fichiers qui contient les stages
	chemin = "../fichiers/maps/"
    # La fonction "os.listdir" prend un nom de chemin en paramètre et renvoie une liste des fichers que contient le répertoire
    # de façon aléatoire
	fichiers = os.listdir(chemin)
	fichiers.sort() 
	stage = 0
	lst = []
	i =0
	stock = []
	if affiche_menu() == "m":# si l'utilisateur a choisi "m" alors on procède à la lecture de stage
		while stage <= (len(fichiers)) :
			bloc, hauteurmax = lecture_fichier(chemin + fichiers[stage]) # on récupère le plateau et la hauteur
			n = len(bloc)
			lb = ((taille_x // 2) - 30) / (len(bloc))
			hb = min(1.5*lb, ((taille_y//2) - 70)/(hauteurmax + 1))
			dessine_stage(lb, hb, n, 0, 0)# on dessine le stage
			retour = mon_jeu(None,n,0,0,bloc)
			if retour == 'r' :
				stage-=1 # pour recommencer
			elif retour == 'q' :
				break
			elif retour == 'n' :
				pass # vu que le compteur existe il faut juste passer au niveau suivant
			elif retour == 'p' :
				if stage != 0 :
					stage -= 2
			elif retour[0] == "winner":#si l'utilisateur gagne
				coup = retour[1] # on récupère le nombre de coup
				retour[0] = victoire(coup) #on appel la fonction victoire avec le coup récupéré
				if retour[0] == "r":
					stage-=1
				elif retour[0] == "q":
					break			
			stage+=1
			if len(fichiers) == stage:
				reponse = restart_game()
				if reponse == "w": # l'utilisateur reprend le jeu
					stage = 0
				
				elif reponse == "q":# quitter
					break
				
	
	if affiche_menu() == "g": #si la fonction renvoie g alors on utilise le mode aléatoire pas très bien réalisé
		"""lst = generateur(lst)
		print(lst)
		longueur= len(lst)
		valeur =solver(lst,(0,0),longueur)
		if valeur != None:"""
		reponse =0
		while i<= 10 :
				bloc= generateur(lst)
				bloc2=max(bloc)
				hauteurmax = max(bloc2)
				n = len(bloc)
				lb = ((taille_x // 2) - 30) / (len(bloc))
				hb = min(1.5*lb, ((taille_y//2) - 70)/(hauteurmax + 1))
				dessine_stage(lb, hb, n, 0, 0)
				retour = mon_jeu(None,n,0,0,bloc)
				if retour == 'r' :
					i-=1 
				elif retour == 'q' :
					break
				elif retour == 'n' :
					pass
				elif retour == 'p' :
					if i == 0 :
						i = 0
					else:
						i -= 2
				elif retour[0] == "winner":
					coup = retour[1]
					retour[0] = victoire(coup)
				if retour[0] == "r":
					i-=1
				elif retour[0] == "q":
					break			
			
				i+=1
				if i == 10:
					reponse = restart_game()
				if reponse == "w":
					i = 0
				elif reponse == "q":
					break
		ferme_fenetre()
