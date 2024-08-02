import asyncio

import pandas as pd

from .settings.player_settings import sort_categories

REGULAR_SEASON = "regular"
SEASON_URLS = {"regular": "2023-24", "playoffs": "2023-24p", "championship": "2023-24c"}
BASE_URL = "https://universitysport.prestosports.com/sports"


def get_sport_identifier(gender: str) -> str:
    if gender == "men":
        return "mbkb"
    elif gender == "women":
        return "wbkb"
    else:
        raise ValueError("Gender must be 'men' or 'women'")


def construct_urls(gender: str, season_option: str) -> str:
    sport = get_sport_identifier(gender)
    base_url = SEASON_URLS[season_option]

    player_stats_url = f"{BASE_URL}/{sport}/{base_url}/players?pos=sh&r=0&sort={{sort_category}}"
    return player_stats_url


def construct_player_urls(gender: str, season_option: str = REGULAR_SEASON) -> list[str]:
    player_stats_url_template = construct_urls(gender, season_option)

    urls = []
    for sort_category in sort_categories:
        url = player_stats_url_template.format(sort_category=sort_category)
        urls.append(url)

    return urls
