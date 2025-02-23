# GUI
La GUI est encore trop lente, il existe encore des améliorations qui peuvent être faîtes.

## Polices d'écritures
Dans **pygame** les polices d'écriture sont des objets (classe : `pygame.font.Font`). Le problème étant qu'à chaque fois que du texte est chargé, il crée un tout nouvel objet `pygame.font.Font`.

<ins>Note</ins> : cet objet dépend du nom de la police mais aussi de sa taille, ainsi dans **pygame** les polices "arial" taille 10 et "arial" taille 25 sont différentes.

Où est-ce que cela est problématique ? Par exemple pour gérer une liste d'onglet, la même police sera rechargée à chaque fois pour chaque onglet, si on a 10 polices il y a 10 objets `pygame.font.Font` si il y a 100 onglets il y a 100 fois la même police chargée dans la mémoire (100 fois la même variable)...

Une idée pour améliorer cela est d'utiliser un système de "shared fonts" (je ne sais pas si le nom est officiel). En gros à traver tout le projet, des polices communes seront utilisées. Lorsqu'une police est demandée pour la toute première fois, alors elle est chargée. Ainsi tous les onglets utilisant la police "associate sans medium" taille 15 utiliseront exactement la même variable `pygame.font.Font` et cette variable ne sera pas dupliquée à chaque onglet.

Autre problème ? Imaginons qu'à certains endroits du programme, on utilise une police inédite ou alors dans une taille inédite (pour des bulles de dialogue, des boutons, etc...). On finira par charger beaucoup de polices dans la mémoire alors que celles-ci sont très peu utilisées voire pas du tout...

Ainsi il on pourrait être sympa rajouter un système de compteurs pour les polices utiliser. Par exemple si on a 3 onglets, alors le compteur de la police "associate sans medium" taille 15 vaut 3 (si on suppose qu'il y a que ces onglets qui utilise cette police avec cette taille). Pour mettre à jour ce compteur on peut utiliser les constructeurs et destructeurs de la classe `gui.Text`. Lorsqu'un de ces compteurs tombe à 0 alors on pourrait supprimer la police (ou alors attendre un certain délai relativement court avant de supprimer la police).

Les polices utilisées se trouvent dans le dossier datas/fonts.

## Textures
Il existe déjà un prototype de shared textures (même principe que les shared fonts) mis en place dans le code.
Il y a trois améliorations attendues.

<ul>
  <li>Mettre en place un système de compteurs comme mentionné plus haut.</li>
  <li>Accéder automatiquement à des textures via leur nom dans le dossier datas/textures/gui (peut se faire via l'intermédiaire d'un dictionnaire).</li>
  <li>Automatiser la génération de certaines textures par des transformations (je vais expliquer ça juste en dessous).</li>
</ul>

Pour le deuxième point, on pourrait par exemple accéder à das textures dans le programme via `gui.textures["close_button", (12, 12)]` pour avoir la texture "datas/textures/gui/close_button/12x12.png". Ou encore mieux, on pourrait utiliser une texture d'une seule et unique résolution pour chaque texture mais grâce à la fonction `pygame.transform.smooth_scale` on adaptera sa taille.

Enfin pour le troisième point, on veut que certaines textures comme "arrow" soient disponibles dans plusieurs sens. L'idée est de n'utiliser qu'un seul fichier "arrow.png" ou plutôt "datas/textures/gui/arrow/20x20.png" mais on pourra utiliser la texture `gui.textures["arrow_right", (20, 20)]` ou bien encore la texture `gui.textures["arrow_up", (20, 20)]` en utilisant la fonction `pygame.transform.rotate`.

<ins>Note :</ins> je sais pas encore qu'elle est la meilleure syntaxe pour ça, on pourrait aussi utiliser `gui.textures.load("arrow", (20, 20), angle = 270)` sous forme de fonction (qui manipulerait un dictionnaire en interne pour les shared textures et les compteurs).

Enfin, on pourrait utiliser une texture "par défaut" lorsque l'on essaye de charger une texture qui n'existe pas comme par exemple `gui.textures["skibidi", (16, 16)]` (vous pouvez vérifier que cette texture ne se trouve pas dans datas/textures/gui) : cette texture par défaut est datas/textures/missing.png.

<ins>Note :</ins> il n'y a pas de raison que l'on séprate les textures pour la gui des autres textures du programme, peut être qu'il faudrait généraliser ça sur tout le programme ? Utiliser des appelles du type `textures.load("gui/close_button", (12, 12))`.

## Onglets
Il reste encore beaucoup de choses à améliorer avec les onglets. J'ai fait de mon mieux pour qu'ils soient responsive mais on peut encore faire d'autres choses.
Une autre amélioration (qui viendra beaucoup plus tard) ça sera des boutons "play/pause" sur les onglets eux mêmes (pour mettre en pause/jouer une simulation sans aller dans l'onglet en question). Vous en conviendrez c'est très optionnel...

## Interfaces
Les interfaces sont des objets contenant des objets du style bouton, liste d'onglets, etc...
Elles possederont une méthode `update(mouse, keyboard)` qui se chargera d'update chacun des trucs qui la compose.

## Organisation général des éléments de GUI
Tous les éléments de GUI possèdent une méthode `surface` retournant la surface qui permet de les afficher.
Ils ont également des setters et des getters pour quasi tous leurs attributs (sauf ceux qui sont utiliser pour le fonctionnement interne).
Un exemple de fonction interne commune à tous les éléments de GUI est `_upgrade_surface` qui permet de mettre à jour la surface (uniquement lorsque c'est nécessaire).

## Le moins c'est le mieux
Une dernière chose à améliorer (et qui rendra la GUI beaucoup plus rapide) c'est la mise à jour des surfaces UNIQUEMENT lorsqu'elles ont été modifiées et dans ce cas on utilise le moins de modifications possibles.
Prenons les onglets par exemple, actuellement lorsque l'on passe la souris sur un onglet voici ce qu'il se passe :
<ul>
  <li>Tout la surface est remplie avec du blanc.</li>
  <li>Le texte est mis-à-jour (couleur mise-à-jour si la souris est dessus) puis ajouter sur la surface.</li>
  <li>Un carré blanc sur l'emplacement de la croix est mise-à-jour (couleur modifiée si jamais y a un clique) puis ajouter sur la surface.</li>
  <li>La croix est mise-à-jour (rouge si la souris est dessus et noire sinon) puis ajouter sur la surface.</li>
</ul>
Bien évidemment il faudrait faire ça de manière plus intelligente : si la souris est passée sur le bouton, il faut modifier UNIQUEMENT le texte, si la souris est passée sur la croix il faut modifier UNIQUEMENT la croix, etc...

Il faudrait faire du cas par cas pour chaque élément de GUI et leurs intéractions...

<ins>Note :</ins> peut être qu'il faudrait supprimer les fonctions `_update_surface` et gérer ça uniquement dans les fonctions `update` pour que ce soit plus fin...

## Quelques options de GUI
Le fichier `gui.__init__.py` est spécial car il permet la configuration et le debugging de la GUI.

### Les fonctions utilitaires
Pour l'instant il n'y en a qu'une seule : `gui.log` qui permet d'écrire dans la console un message (avec le préfixe "GUI :" en bleu).

<ins>Note :</ins> on peut penser à ajouter une fonction `gui.log_error` qui pourrait log les erreurs on encore copier les logs dans un fichier.

### Les flags
Il existe un seul flag pour l'instant : `gui.track_updates` qui une fois sur `True`, permet de tracker à chaque fois qu'une texture est mise à jour (via `gui.log`). Vous l'aurez compris il sert à vérifier qu'une texture n'est pas modifiée 40 fois par seconde (ça m'a déjà beaucoup servi).

### Un framerate indépendant
À priori, le programme disposera de quatre types de framerate : ceux pour l'affichage d'une simulation (objectif : 24 par simulation), ceux pour la mise à jour d'une simulation (objectif : 60 par simulation), un pour l'affichage de la GUI (objectif : 10) et un pour la mise à jour de la GUI (objectif : 5).

En effet je pense que vérifier 5 fois par seconde si les boutons sont cliqués ou des trucs du genre est largement suffisant (ça représente une vérification toutes les 0.2 secondes). Pour l'affichage je pense un petit plus pour pas qu'il y ait un délai trop gros en une action et son affichage. Seul petit bémol ça pourrait être les slidebars/scrollbars ou les trucs du genre (dans ce cas on pourra augmenter leur sensibilité)...

## Couplage avec pygame_gui ?
Je pense qu'on pourrait utiliser la librairie pygame_gui pour une grosse partie de la GUI (les text input, les slidebars, etc...) car ça représente beaucoup de travail de faire tout ça à la main... Il semblerait que `pygame_gui` fonctionne de manière assez similaire (un framerate indépendant, des interfaces customisables, etc...) donc il devrait y avoir moyen de le faire fonctionner assez bien avec nos classes fait maison (il y a juste quelques trucs que cette librairie fait pas comme les onglets, etc...).

Idéalement toutes les classes seraient fait maison mais je pense qu'on s'y prend trop tard...
