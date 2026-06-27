# mobs/werewolf.py
WEREWOLF_DATA = {
    "level": 9,
    "is_grouped": True,
    "adena_min": 46,
    "adena_max": 83,
    "groups": [
        {
            "group_chance": 0.136007,
            "items": [
                {"name": "animal_bone", "chance_in_group": 0.323267, "min": 1, "max": 3}, # Кости пачками
                {"name": "animal_skin", "chance_in_group": 0.323265, "min": 1, "max": 2},
                {"name": "rec_leather_stockings", "chance_in_group": 0.326529, "min": 1, "max": 1},
                {"name": "haste_potion", "chance_in_group": 0.026939, "min": 1, "max": 1}
            ]
        },
        {
            "group_chance": 0.002814,
            "items": [
                {"name": "iron_gloves", "chance_in_group": 1.000000, "min": 1, "max": 1}
            ]
        },
        {
            "group_chance": 0.700000,
            "items": [
                {"name": "adena", "chance_in_group": 1.000000, "min": 46, "max": 83}
            ]
        }
    ]
}
