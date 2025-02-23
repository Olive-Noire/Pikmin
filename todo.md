# GUI
La GUI est encore trop lente, il existe encore des améliorations qui peuvent être faîtes.

## Polices d'écritures
Dans **pygame** les polices d'écriture sont des objets (classe : `pygame.font.Font`). Le problème étant qu'à chaque fois que du texte est chargé, il crée un tout nouvel objet `pygame.font.Font`.

<ins>Remarque</ins> : cet objet dépend du nom de la police mais aussi de sa taille, ainsi dans **pygame** les polices "arial" taille 10 et "arial" taille 25 sont différentes.
