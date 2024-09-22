import json
from typing import List
import mastery as m


def determine_owned_champions(riot_puuid: str, mastery_info: List[dict[str, str]]) -> dict[str, str]:
    """
    Determine which champions are owned by a riot player given a list of
    champions from riot compared to the champions present in mastery
    """
    with open('../data/champions.json', 'r') as f:
        all_champs: dict = json.load(f)

    all_champ_keys = all_champs.keys()  # Only a reference to keys in dict
    m.get_all_mastery_by_puuid(riot_puuid)

    owned_champ_keys = set([obj['championId'] for obj in mastery_info])

    # TODO:Construct a dictionary based on remaining items in all_champ_keys

    unowned_champion_keys = all_champ_keys - owned_champ_keys
    unowned_champions = dict()
    for key in unowned_champion_keys:
        unowned_champions[key] = all_champs[key]
    return unowned_champions
