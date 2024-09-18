import json
import mastery as m


def determine_owned_champions(mastery_info: dict[str, str]) -> dict[str, str]:
    """
    Determine which champions are owned by a riot player given a list of
    champions from riot compared to the champions present in mastery
    """
    with open('../data/champions.json', 'r') as f:
        all_champs: dict = json.load(f) 

    keys = all_champs.keys()
    return {}

