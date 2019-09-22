import requests
import json
import browser_cookie3 # todo: check this lib and look for alternatives


def get_character_data(character_name):
    """
    Get character data from server.
    You can access ONLY your character.
    And also you need to be logged in 'www.pathofexile.com'

    :param character_name: Character name which data you want to receive
    :return: Data in json format
    """
    character_data_url = f'https://www.pathofexile.com/character-window/get-items?character={character_name}'

    # Get cookies from all browsers
    cj = browser_cookie3.load()

    return requests.get(character_data_url, cookies=cj).json()


def get_equipped_gems_requirements(data):
    """
    Parse character data and return info about equipped gems and their requirements

    :param data: Character data in json
    :return: Dict with key = item type and value = list of lists

    return example:
    {
        'BodyArmour':
            [
                ('Melee Physical Damage Support', [('Str', '108')]),
                ('Fortify Support', [('Str', '108')]),
                ('Vaal Cyclone', [('Str', '68'), ('Dex', '98')]),
                ('Increased Area of Effect Support', [('Int', '109')]),
                ('Elemental Damage with Attacks Support', [('Str', '68'), ('Int', '47')]),
                ('Pulverise Support', [('Str', '105')])
            ]
    }
    """
    gems = {}

    for item in data['items']:
        try:
            item['socketedItems']
        except KeyError:
            continue

        for gem in item['socketedItems']:
            requirements = []
            for req in gem['requirements']:
                if req['name'] in ('Dex', 'Int', 'Str'):
                    requirements.append((req['name'], req['values'][0][0]))

            gems.setdefault(item['inventoryId'], [])
            gems[item['inventoryId']].append((gem['typeLine'], requirements))

    return gems
