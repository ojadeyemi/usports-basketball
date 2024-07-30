import asyncio
import pandas as pd
from .data_processing import get_standings_df
from .data_processing import get_team_stats_df
from .config.values import team_conference


def get_men_team_stats():
    return asyncio.run(combine_data("men"))


def get_women_team_stats():
    return asyncio.run(combine_data("women"))


async def combine_data(gender: str) -> pd.DataFrame:
    if gender == "men":
        urls = [
            "https://universitysport.prestosports.com/sports/mbkb/2023-24/teams?sort=&r=0&pos=off",
            "https://universitysport.prestosports.com/sports/mbkb/2023-24/standings-conf",
        ]
    elif gender == "women":
        urls = [
            "https://universitysport.prestosports.com/sports/wbkb/2023-24/teams?sort=&r=0&pos=off",
            "https://universitysport.prestosports.com/sports/wbkb/2023-24/standings-conf",
        ]
    else:
        raise ValueError("Gender must be 'men' or 'women'")

    team_stats_url, standings_url = urls
    standings_df = await get_standings_df(standings_url)
    team_stats_df = await get_team_stats_df(team_stats_url)
    combined_df = pd.merge(
        standings_df, team_stats_df, on=["team_name", "games_played"], how="inner"
    )
    combined_df["conference"] = (
        combined_df["team_name"].map(team_conference).astype(str)
    )
    return combined_df
