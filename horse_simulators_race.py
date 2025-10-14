#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random

# --- Grilles de vitesse et distance ---
SPEED_MODIFICATION_GRID = {
    0: {1: 0, 2: 0, 3: +1, 4: +1, 5: +1, 6: +2},
    1: {1: 0, 2: 0, 3: +1, 4: +1, 5: +1, 6: +2},
    2: {1: 0, 2: 0, 3: +1, 4: +1, 5: +1, 6: +2},
    3: {1: -1, 2: 0, 3: 0, 4: +1, 5: +1, 6: +1},
    4: {1: -1, 2: 0, 3: 0, 4: 0, 5: +1, 6: +1},
    5: {1: -2, 2: -1, 3: 0, 4: 0, 5: 0, 6: +1},
    6: {1: -2, 2: -1, 3: 0, 4: 0, 5: 0, 6: 'DQ'},
}

DISTANCE_BY_SPEED = {
    0: 0,
    1: 23,
    2: 46,
    3: 69,
    4: 92,
    5: 115,
    6: 138
}

RACE_LENGTH = 2400
LAP_TIME = 10

# --- Fonctions ---

def get_number_of_horses():
    while True:
        value = input("Entrer le nombre de chevaux (entre 12 et 20) : ")
        if value.isdigit():
            number = int(value)
            if 12 <= number <= 20:
                return number
        print("Valeur non valide.")

def get_race_type():
    while True:
        race = input("Entrer le type de course (tierce, quarte, quinte) : ").lower()
        if race in {"tierce", "quarte", "quinte"}:
            return {"tierce": 3, "quarte": 4, "quinte": 5}[race]
        print("Type de course invalide.")

def initialize_horses(nb_horses):
    horses = {}
    for numero in range(1, nb_horses + 1):
        horses[numero] = {
            "speed": 0,
            "distance": 0,
            "actif": True,
            "lap_arrived": None
        }
    return horses

def roll_dice():
    return random.randint(1, 6)

def update_horse(horse, roll, speed_mod_grid, dist_by_speed, lap, race_length):
    if not horse["actif"] or horse["lap_arrived"] is not None:
        return

    speed = horse["speed"]
    mod = speed_mod_grid[speed][roll]

    if mod == 'DQ':
        horse["actif"] = False
        print(f"❌ Disqualifié (jet de {roll})")
        return

    new_speed = max(0, min(speed + mod, 6))
    horse["speed"] = new_speed
    horse["distance"] += dist_by_speed[new_speed]

    if horse["distance"] >= race_length and horse["lap_arrived"] is None:
        horse["lap_arrived"] = lap

    print(f"Jet={roll}, mod={mod:+}, speed={new_speed}, distance={horse['distance']} m")

def is_race_over(horses, race_length):
    return all(
        not h["actif"] or h["lap_arrived"] is not None
        for h in horses.values()
    )

def get_final_ranking(horses):
    return sorted(
        horses.items(),
        key=lambda x: (
            x[1]["lap_arrived"] if x[1]["lap_arrived"] is not None else float('inf'),
            -x[1]["distance"]
        )
    )

def display_ranking(ranking, race_type, lap_time):
    print("\nClassement final :\n")
    for place, (num, ch) in enumerate(ranking, start=1):
        if ch["lap_arrived"] is not None:
            temps = ch["lap_arrived"] * lap_time
            print(f"{place}. Cheval {num} est arrivé en {temps} s")
        elif not ch["actif"]:
            print(f"{place}. Cheval {num} est disqualifié")
        else:
            print(f"{place}. Cheval {num} - {ch['distance']} m (en course)")

    print(f"\nTop {race_type} :")
    for i, (num, ch) in enumerate(ranking[:race_type], start=1):
        if ch["lap_arrived"] is not None:
            temps = ch["lap_arrived"] * lap_time
            print(f"{i}. Cheval {num}  en {temps} s")
        elif not ch["actif"]:
            print(f"{i}. Cheval {num} est disqualifié")
        else:
            print(f"{i}. Cheval {num} - {ch['distance']} m")

def run_race(nb_horses, race_type, speed_mod_grid, dist_by_speed, race_length, lap_time):
    horses = initialize_horses(nb_horses)
    lap = 1

    print(f"\nDébut de la course avec {nb_horses} chevaux\n")

    while True:
        input(f"\n--- Tour {lap} (t = {lap * lap_time} s) --- (Entrée pour continuer)")

        for numero, horse in horses.items():
            if not horse["actif"] or horse["lap_arrived"] is not None:
                continue

            print(f"Cheval {numero}: ", end="")
            roll = roll_dice()
            update_horse(horse, roll, speed_mod_grid, dist_by_speed, lap, race_length)

        if is_race_over(horses, race_length):
            ranking = get_final_ranking(horses)
            display_ranking(ranking, race_type, lap_time)
            break

        lap += 1

# --- Programme principal ---

def main():
    while True:
        nb_horses = get_number_of_horses()
        race_type = get_race_type()

        run_race(
            nb_horses,
            race_type,
            SPEED_MODIFICATION_GRID,
            DISTANCE_BY_SPEED,
            RACE_LENGTH,
            LAP_TIME
        )

        fin = input("\nTapez FIN pour quitter ou Entrée pour une nouvelle course : ")
        if fin.strip().upper() == "FIN":
            break

if __name__ == "__main__":
    main()
