# mobs/orc_grunt.py
ORC_GRUNT_DATA = {
    "level": 7,
    "is_grouped": True,
    "adena_min": 35,
    "adena_max": 63,
    "groups": [
        {
            "group_chance": 0.096207,
            "items": [
                {"name": "coal", "chance_in_group": 0.298792, "min": 1, "max": 1},
                {"name": "varnish", "chance_in_group": 0.298792, "min": 1, "max": 1},
                {"name": "rec_leather_stockings", "chance_in_group": 0.402416, "min": 1, "max": 1}
            ]
        },
        {
            "group_chance": 0.700000,
            "items": [
                {"name": "adena", "chance_in_group": 1.000000, "min": 35, "max": 63} # Диапазон адены со скрина
            ]
        },
        {
            "group_chance": 0.030646,
            "items": [
                {"name": "leather_cap", "chance_in_group": 0.411865, "min": 1, "max": 1},
                {"name": "small_shield", "chance_in_group": 0.588315, "min": 1, "max": 1}
            ]
        }
    ]
}
