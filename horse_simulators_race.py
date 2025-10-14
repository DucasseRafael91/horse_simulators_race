#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random

from colorama import init, Fore, Style

# Initialise colorama (pour Windows notamment)
init(autoreset=True)

speed_modification_grid = {
    0: {1: 0, 2: 0, 3: +1, 4: +1, 5: +1, 6: +2},
    1: {1: 0, 2: 0, 3: +1, 4: +1, 5: +1, 6: +2},
    2: {1: 0, 2: 0, 3: +1, 4: +1, 5: +1, 6: +2},
    3: {1: -1, 2: 0, 3: 0, 4: +1, 5: +1, 6: +1},
    4: {1: -1, 2: 0, 3: 0, 4: 0, 5: +1, 6: +1},
    5: {1: -2, 2: -1, 3: 0, 4: 0, 5: 0, 6: +1},
    6: {1: -2, 2: -1, 3: 0, 4: 0, 5: 0, 6: 'DQ'},
}

distance_by_speed = {0: 0, 1: 23, 2: 46, 3: 69, 4: 92, 5: 115, 6: 138}
race_length = 2400
lap_time = 10

def get_number_of_horses():
    while True:
        value = input("Entrer le nombre de chevaux (12-20) : ")
        if value.isdigit() and 12 <= int(value) <= 20:
            return int(value)
        print("Valeur non valide.")

def get_race_type():
    types = {"tierce": 3, "quarte": 4, "quinte": 5}
    while True:
        race = input("Type de course (tierce, quarte, quinte) : ").lower()
        if race in types:
            return types[race]
        print("Type invalide.")

def initialize_horses(nb_horses):
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

    mod = speed_modification_grid[horse["speed"]][roll]
    if mod == 'DQ':
        horse["actif"] = False
        return

    horse["speed"] += mod
    horse["distance"] += distance_by_speed[horse["speed"]]

    if horse["distance"] >= race_length and not horse["lap_arrived"]:
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
    print(f"\nTop {race_type} :")
    for i, (num, ch) in enumerate(ranking[:race_type], 1):
        if ch["lap_arrived"]:
            t = ch["lap_arrived"] * lap_time
            print(f"{i}. Cheval {num} - {t//60} min {t%60} s")
        elif not ch["actif"]:
            print(f"{i}. Cheval {num} disqualifié")
        else:
            print(f"{i}. Cheval {num} - {ch['distance']} m")

def print_progress_bar(horses):
    max_bar_length = 40  # Largeur de la barre en caractères

    for num, horse in horses.items():
        progress_ratio = horse["distance"] / race_length
        progress_ratio = min(progress_ratio, 1.0)  # clamp max à 1

        filled_length = int(progress_ratio * max_bar_length)
        bar = '█' * filled_length + '-' * (max_bar_length - filled_length)

        if horse["lap_arrived"]:
            status = f"arrivé (tour {horse['lap_arrived']})"
            color = Fore.GREEN
        elif not horse["actif"]:
            status = "disqualifié"
            color = Fore.RED
        else:
            status = "en course"
            color = Fore.YELLOW

        print(f"Cheval {num:2d} |{color}{bar}{Style.RESET_ALL}| {horse['distance']:4d} m - {status}")

def run_race(nb_horses, race_type):
    horses = initialize_horses(nb_horses)
    lap = 1

    print(f"\nDébut de la course\n")

    while True:
        input(f"\nTour {lap} - Appuyez sur Entrée pour continuer...")
        for num, horse in horses.items():
            update_horse(horse, random.randint(1, 6), lap)

        print_progress_bar(horses)

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