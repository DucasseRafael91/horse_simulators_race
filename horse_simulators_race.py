#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random

SPEED_MODIFICATION_GRID = {
    0: {1: 0, 2: 0, 3: +1, 4: +1, 5: +1, 6: +2},
    1: {1: 0, 2: 0, 3: +1, 4: +1, 5: +1, 6: +2},
    2: {1: 0, 2: 0, 3: +1, 4: +1, 5: +1, 6: +2},
    3: {1: -1, 2: 0, 3: 0, 4: +1, 5: +1, 6: +1},
    4: {1: -1, 2: 0, 3: 0, 4: 0, 5: +1, 6: +1},
    5: {1: -2, 2: -1, 3: 0, 4: 0, 5: 0, 6: +1},
    6: {1: -2, 2: -1, 3: 0, 4: 0, 5: 0, 6: 'DQ'},
}

DISTANCE_BY_SPEED = {0: 0, 1: 23, 2: 46, 3: 69, 4: 92, 5: 115, 6: 138}
RACE_LENGTH = 2400
LAP_TIME = 10

def get_number_of_horses():
    """
       Permet de savoir combien de chevaux participeront à la course
       :return: nombre de chevaux entre 12 et 20 qui participeront à la course
    """
    while True:
        value = input("Entrer le nombre de chevaux (12-20) : ")
        if value.isdigit() and 12 <= int(value) <= 20:
            return int(value)
        print("Valeur non valide.")

def get_race_type():
    """
       Permet de savoir quel type de course, cela sera (tierce, quarte ou quinte )
       :return: 3,4,5 selon si cela est une tierce, un quarté ou un quinté
    """
    types = {"tierce": 3, "quarte": 4, "quinte": 5}
    while True:
        race = input("Type de course (tierce, quarte, quinte) : ").lower()
        if race in types:
            return types[race]
        print("Type invalide.")


def initialize_horses(nb_horses):
    """
     Crée un dictionnaire représentant les chevaux d'une course.
    :param nb_horses: Nombre de chevaux dans la course
    :return: Dictionnaire des chevaux avec leurs attributs initialisés
    """
    horses = {}
    for horse_number in range(1, nb_horses + 1):
        horses[horse_number] = {
            "speed": 0,
            "distance": 0,
            "actif": True,
            "lap_arrived": None
        }
    return horses

def update_horse(horse, roll, lap):
    if not horse["actif"] or horse["lap_arrived"]:
        return

    mod = SPEED_MODIFICATION_GRID[horse["speed"]][roll]
    if mod == 'DQ':
        horse["actif"] = False
        return

    horse["speed"] = max(0, min(horse["speed"] + mod, 6))
    horse["distance"] += DISTANCE_BY_SPEED[horse["speed"]]

    if horse["distance"] >= RACE_LENGTH and not horse["lap_arrived"]:
        horse["lap_arrived"] = lap

def is_race_over(horses):
    return all(not h["actif"] or h["lap_arrived"] for h in horses.values())

def get_final_ranking(horses):
    return sorted(
        horses.items(),
        key=lambda x: (
            x[1]["lap_arrived"] if x[1]["lap_arrived"] else float('inf'),
            -x[1]["distance"]
        )
    )

def display_ranking(ranking, race_type):
    print("\nClassement final :\n")
    for place, (num, ch) in enumerate(ranking, 1):
        if ch["lap_arrived"]:
            t = ch["lap_arrived"] * LAP_TIME
            print(f"{place}. Cheval {num} en {t} s")
        elif not ch["actif"]:
            print(f"{place}. Cheval {num} disqualifié")
        else:
            print(f"{place}. Cheval {num} - {ch['distance']} m")

    print(f"\nTop {race_type} :")
    for i, (num, ch) in enumerate(ranking[:race_type], 1):
        if ch["lap_arrived"]:
            t = ch["lap_arrived"] * LAP_TIME
            print(f"{i}. Cheval {num} - {t//60} min {t%60} s")
        elif not ch["actif"]:
            print(f"{i}. Cheval {num} disqualifié")
        else:
            print(f"{i}. Cheval {num} - {ch['distance']} m")

def run_race(nb_horses, race_type):
    horses = initialize_horses(nb_horses)
    lap = 1

    print(f"\nDébut de la course\n")

    while True:
        input(f"\nTour {lap} Appuyez sur Entrée")
        for num, horse in horses.items():
            update_horse(horse, random.randint(1, 6), lap)

        if is_race_over(horses):
            ranking = get_final_ranking(horses)
            display_ranking(ranking, race_type)
            break

        lap += 1

def main():
    while True:
        nb_horses = get_number_of_horses()
        race_type = get_race_type()
        run_race(nb_horses, race_type)
        if input("\nTapez FIN pour quitter ou Entrée pour une nouvelle course : ").strip().upper() == "FIN":
            break

if __name__ == "__main__":
    main()