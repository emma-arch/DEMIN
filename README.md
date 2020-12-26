# Mini_projet_ludique_python
Description du code du jeu en ligne le démineur.
***
## Informations génerales
Le but du jeu du démineur est de découvrir toutes les cases vides du plateau sans faire exploser les mines.
***
Ici, le plateau est représenté par un liste de liste de dictionnaire.

La case de coordonnée (x,y) est un dictionnaire donc une paire clé valeur.
  - "mine" (une clé) qui est un booléen et qui indique si la case contient une mine 
  - "etat" (une clé) indique l'état de la case :
      - INCONNU quand le joueur n'a pas découvert la case
      - Un entier compris entre 0 et 8 qui indique le nombre de mines voisines, quand le joueur a decouvert la case.
      - PERDU quand il s'agit d'une case avec une mine, que le joueur a séléctionné.
      - DRAPEAU si le joueur a mis un drapeau.

Pour rendre le jeu plus visuel on attribut les symboles suivant à ces étiquettes :  

- INCONNU = _
- PERDU = !
- DRAPEAU = *

3 différents choix de niveaux de jeux pour le joueur : 
- Niveau 1 --> Facile : plateau de taille 9*9
- Niveau 2 --> intermédiaire : plateau de taille 16*16
- Niveau 3 --> Expert : plateau de taille 24*24 

A chaque partie le joueur décide du niveau qu'il veut.
Dans le fichier scores.txt on stock les scores. Au démarrage le score du joueur est de 0 puis il augmente de 1 à chaque fois que le joueur gagne une partie.

### Collaboration
Le projet à été mené à bien par Emma Brillat.
Réalisation de octobre à janvier 2020.

### Explications des fonctions
La fonction `genere_plateau_vide(level)` créée un plateau vide de taille : 
- (9,9) pour le niveau 1
- (16,16) pour le niveau 2
- (24,24) pour le niveau 3

La fonction `place_mines(plateau, level, alea = True)` place par défaut n mines sur le plateau aléatoirement, avec n = nombre de ligne du plateau.
Et si alea = False, place n mines sur la diagonal. 

La fonction `construire_plateau(level, alea = True)` génère le plateau.

la fonction `coup-joueur(x,y)` demande au joueur qu'elle niveau de jeu il veut, les coordonnées de la case qu'il veut découvrir et s'il veut y mettre un drapeau.

La fonction `case_voisines(plateau,x,y)` renvoie une liste de liste de coordonnées des cases voisine de la case (x,y). La taille de cette liste est donc de 3 de 5 ou de 8.

la fonction `decouvre_case(plateau,x,y)` est à la fois une procédure et une fonction car elle renvoie False si la case contient une mine et True sinon, tous ça en changent la variable plateau. En effet, si False alors l'état de la case devient PERDU et sinon l'état devient égal au nombre de mine qu'il y a autour de la case (grâce à l'execution de la fonction composante_connexe).

La fonction `composante_connexe(plateau,x,y)` modifie l'état de la case que l'on découvre et celle de ses voisines si elles ne sont inconnues et que la case découverte n'as pas de mine autour d'elle.

La fonction `check(plateau)` retourne le nombre de case inconnue et de case avec un drapeau. Si ce nombre est égal à celui retourné par le fonction `totale_mines(plateau)` (qui compte le nombre totale de mine sur le plateau), alors le joueur à gagné. 

La fonction `display(plateau)` permet d'afficher le plateau et ainsi de rendre la partie de jeu beaucoup plus visuelle.

Les fonctions `write_score(filename,score)` et `read_scores(filename)` permettent respectivement d'écrire les scores dans le fichier scores.txt et de les lire.

#### Appel des fonctions

La boucle while True est une boucle infinie qui permet de jouer au démineur.
Le déroulement d'une partie de jeu est la suivante : 

1) Affichage du plateau avec en haut à gauche le compteur qui indique le nombre de mine qu'il reste à trouver.

2) Choix de la case à découvrir.

3) 
  - Si elle contenait une mine alors le joueur à perdu. Et recommence une partie.
  - Si le nombre totale de mine sur le plateau est égal a celui du nombre de drapeau + de case inconnu alors le joueur à gagné et son score augmente de 1.
  - Sinon on compte le nombre de mines qu'il y a autour de cette case.
      - Et si il n'y en a pas on continue de découvrir les cases voisines des cases voisines.
      - Sinon on s'arrête.

4) Affiche le plateau avec la/les case(s) qui a/ont été découverte(s). Et mise à jour du compteur.

5) Choix de la case à découvir.

6) Refait les étapes 3), 4), 5) jusqu'à l'infini.


