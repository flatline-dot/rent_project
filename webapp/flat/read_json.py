import json


def get_metro():
    with open('C:\\Project\\rent_project\\webapp\\flat\\data_metro.json') as f:
        template = json.load(f)
    list_metro = []
    for station in template:
        list_metro.append(station['Station'])

    list_metro.sort()
    list_metro[-1] = 'Улица Дмитриевского'
    unique_name = []
    for name in list_metro:
        if name not in unique_name:
            unique_name.append(name)
    unique_name.sort()
    return unique_name
