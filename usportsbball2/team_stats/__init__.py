import asyncio

import pandas as pd

from .data_processing import get_standings_df, get_team_stats_df
from .settings.team_settings import team_conference

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


def construct_urls(gender: str, season_option: str) -> tuple[str, str]:
    """Construct URLs for fetching team stats and standings data based on gender and season option."""
    sport = get_sport_identifier(gender)
    base_url = SEASON_URLS[season_option]
    team_stats_url = f"{BASE_URL}/{sport}/{base_url}/teams"
    standings_url = f"{BASE_URL}/{sport}/2023-24/standings-conf"
    return team_stats_url, standings_url


async def combine_data(gender: str, season_option: str) -> pd.DataFrame:
    """Combine team stats and standings data into a single DataFrame."""
    if season_option not in SEASON_URLS:
        raise ValueError(f"Invalid season_option: {season_option}. Must be one of {', '.join(SEASON_URLS.keys())}")

    team_stats_url, standings_url = construct_urls(gender, season_option)

    standings_df = await get_standings_df(standings_url)
    team_stats_df = await get_team_stats_df(team_stats_url)

    # Update column names if necessary
    if season_option in ["playoffs", "championship"]:
        standings_df.columns = [f"reg_{col}" if col != "team_name" else col for col in standings_df.columns]

    # Merge data based on season_option
    merge_columns = ["team_name", "games_played"] if season_option == "regular" else ["team_name"]
    combined_df = pd.merge(standings_df, team_stats_df, on=merge_columns, how="inner")
    combined_df["conference"] = combined_df["team_name"].map(team_conference).astype(str)

    return combined_df


def get_men_team_stats(season_option: str = REGULAR_SEASON) -> pd.DataFrame:
    """
    Retrieve and combine current men’s team stats based on the specified season option.

    Args:
        season_option (str): The season option, e.g., 'regular', 'playoffs', or 'championship'.

    Returns:
        pd.DataFrame: The combined DataFrame for men’s team stats.
    """
    return asyncio.run(combine_data("men", season_option))


def get_women_team_stats(season_option: str = REGULAR_SEASON) -> pd.DataFrame:
    """
    Retrieve and combine current women’s team stats based on the specified season option.

    Args:
        season_option (str): The season option, e.g., 'regular', 'playoffs', or 'championship'.

    Returns:
        pd.DataFrame: The combined DataFrame for women’s team stats.
    """
    return asyncio.run(combine_data("women", season_option))
