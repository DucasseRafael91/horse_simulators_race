🐴 Simulation de Course de Trot Attelé

Ce projet est un simulateur de course de trot attelé, inspiré des courses hippiques réelles. Il s'agit d'un jeu au tour par tour, dans lequel chaque cheval progresse en fonction d’un jet de dé, simulant les variations de vitesse tout au long d’une course de 2 400 mètres.

📜 Règles de la course

La course se déroule sur un hippodrome rectiligne de 2400 m.

Chaque cheval est mené par un driver dans un sulky, dans un couloir séparé.

Chaque cheval commence à l’arrêt (vitesse = 0).

À chaque tour de jeu (équivalent à 10 secondes dans la course), un dé à 6 faces est lancé pour chaque cheval.

Le jet de dé modifie la vitesse du cheval, selon un tableau prédéfini.

La vitesse détermine la distance parcourue par le cheval à ce tour.

Si un cheval atteint une vitesse de 6 et obtient un 6 au dé, il est disqualifié pour passage au galop.

🎲 Évolution de la vitesse

La vitesse de chaque cheval est mise à jour à chaque tour selon le tableau d’évolution suivant :

| Vitesse actuelle | Dé = 1 | Dé = 2 | Dé = 3 | Dé = 4 | Dé = 5 | Dé = 6 |
| ---------------- | ------ | ------ | ------ | ------ | ------ | ------ |
| 0                | 0      | +1     | +1     | +1     | +2     | +2     |
| 1                | 0      | 0      | +1     | +1     | +1     | +2     |
| 2                | 0      | 0      | +1     | +1     | +1     | +2     |
| 3                | -1     | 0      | 0      | +1     | +1     | +1     |
| 4                | -1     | 0      | 0      | 0      | +1     | +1     |
| 5                | -2     | -1     | 0      | 0      | 0      | +1     |
| 6                | -2     | -1     | 0      | 0      | 0      | DQ     |


DQ = Disqualification (passage au galop interdit)

🏁 Distance parcourue selon la vitesse
| Vitesse | Distance (m) / tour (10s) |
| ------- | ------------------------- |
| 0       | 0                         |
| 1       | 23                        |
| 2       | 46                        |
| 3       | 69                        |
| 4       | 92                        |
| 5       | 115                       |
| 6       | 138                       |

⚙️ Fonctionnement du programme

Au démarrage, l’utilisateur saisit :

Le nombre de chevaux (entre 12 et 20),

Le type de course : tiercé (3 premiers), quarté (4 premiers), quinté (5 premiers).

La course se joue en tours successifs :

À chaque tour, le programme affiche :

Le numéro du tour,

La vitesse actuelle de chaque cheval,

La distance totale parcourue,

Une éventuelle disqualification.

L’utilisateur appuie sur une touche pour passer au tour suivant.

La course se termine lorsque tous les chevaux non disqualifiés ont franchi la ligne d’arrivée (2400 m).

Le programme affiche alors :

Les 3, 4 ou 5 premiers chevaux arrivés, selon le type de course choisi.

🖥️ (Optionnel) Affichage visuel

Il existe un affiche visuel permettant de savoir ou est chaque cheval à chaque tour

=

🛠️ Technologies utilisées

Langage : Python 3.13

Bibliothéque Random
Bibliothéque Colorama

📂 Structure du projet
trot-course/
│
├── horse_simulators_race.py         # Code principal de la simulation
├── README.md                        # Ce fichier
└── .gitignore                       # Gitignore

📌 Remarques

Le programme est basé sur une logique de jeu de plateau.

La progression dépend uniquement du hasard (jets de dé).

Le passage au galop est interdit → attention aux disqualifications !

