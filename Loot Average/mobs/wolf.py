# mobs/wolf.py
WOLF_DATA = {
    "level": 4,
    "is_grouped": True,
    "adena_min": 22,
    "adena_max": 40,
    "groups": [
        {
            "group_chance": 0.060094,
            "items": [
                {"name": "coal", "chance_in_group": 0.249084, "min": 1, "max": 1},
                {"name": "varnish", "chance_in_group": 0.249084, "min": 1, "max": 1},
                {"name": "rec_broad_sword", "chance_in_group": 0.132841, "min": 1, "max": 1},
                {"name": "lesser_hp_potion", "chance_in_group": 0.368991, "min": 1, "max": 2} # Волк может дропнуть до 2 банок!
            ]
        },
        {
            "group_chance": 0.700000,
            "items": [
                {"name": "adena", "chance_in_group": 1.000000, "min": 22, "max": 40}
            ]
        },
        {
            "group_chance": 0.020788,
            "items": [
                {"name": "short_bow", "chance_in_group": 1.000000, "min": 1, "max": 1}
            ]
        }
    ]
}
