
specialist_db: dict[dict[str, str | int | bool]] = {
    'speciality_1':{
        'specialist_1':
        {'experience':11,},
        'specialist_2':
        {'experience':10,},
        'specialist_3':
        {'experience':13,}

    },
     'speciality_2':{
        'specialist_4':
        {'experience':11,},
        'specialist_5':
        {'experience':10},
        'specialist_6':
        {'experience':13,}}

    }
def get_specialists():
    dict_specialist = {}
    for value in list(specialist_db.values()):
        dict_specialist |= value
    return dict_specialist

print(get_specialists())