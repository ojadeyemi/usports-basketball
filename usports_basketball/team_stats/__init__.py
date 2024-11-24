"""
Module for fetching and processing U Sports basketball team statistics.

This module provides a function to retrieve and merge team statistics and standings data
from the U Sports basketball league for both men's and women's teams.
It utilizes web scraping techniques to extract data from the U Sports website
and processes it into pandas DataFrames for further analysis.

Function:
- usport_team_stats: Fetch and combine current team statistics and standings.

Author:
    OJ Adeyemi

Date Created:
    August 6, 2024
"""

import asyncio
from typing import Literal

import pandas as pd
from pandas import DataFrame

from ..constants import BASE_URL, SEASON, SEASON_URLS
from ..utils import get_sport_identifier, normalize_gender_arg, setup_logging, validate_season_option
from .data_processing import get_standings_df, get_team_stats_df
from .team_settings import team_conference

logger = setup_logging()


def __construct_urls(gender: str, season_option: str) -> tuple[str, str]:
    """Construct URLs for fetching team stats and standings data based on gender and season option."""
    sport = get_sport_identifier(gender)
    base_url = validate_season_option(season_option, SEASON_URLS)

    team_stats_url = f"{BASE_URL}/{sport}/{base_url}/teams"
    standings_url = f"{BASE_URL}/{sport}/{SEASON}/standings"
    
    return team_stats_url, standings_url


async def __combine_data(gender: str, season_option: str) -> DataFrame:
    """Combine team stats and standings data into a single DataFrame."""
    if season_option not in SEASON_URLS:
        raise ValueError(f"Invalid season_option: {season_option}. Must be one of {', '.join(SEASON_URLS.keys())}")

    team_stats_url, standings_url = __construct_urls(gender, season_option)

    logger.debug(f"FETCHING {gender.upper()} {season_option.upper()} SEASON STANDINGS")
    standings_df = await get_standings_df(standings_url)

    logger.debug(f"FETCHING {gender.upper()} {season_option.upper()} SEASON STATISTICS\n")
    team_stats_df = await get_team_stats_df(team_stats_url)

    # Update column names if necessary
    if season_option in ["playoffs", "championship"]:
        standings_df.columns = [f"reg_{col}" if col != "team_name" else col for col in standings_df.columns]

    # Merge data based on season_option
    merge_columns = ["team_name", "games_played"] if season_option == "regular" else ["team_name"]
    combined_df = pd.merge(standings_df, team_stats_df, on=merge_columns, how="inner")
    combined_df["conference"] = combined_df["team_name"].map(team_conference).astype(str)

    return combined_df


def usport_team_stats(
    arg: Literal["m", "men", "w", "women"], season_option: Literal["regular", "playoffs", "championship"] = "regular"
) -> DataFrame:
    """
    Retrieve and combine current U Sports Basketball team stats based on gender and season.

    Args:
        arg (str): Gender of the teams. Accepts 'men', 'women', 'm', or 'w' (case insensitive).
        season_option (str): The season type to fetch data for. Options are:
            - 'regular': Regular season statistics (default).
            - 'playoffs': Playoff season statistics.
            - 'championship': Championship season statistics.

    Returns:
        DataFrame: DataFrame containing the combined team stats.
    """
    gender = normalize_gender_arg(arg)
    season_option = season_option.lower()

    logger.info(f"FETCHING CURRENT {gender.upper()} {season_option.upper()} SEASON TEAM STATS\n")

    return asyncio.run(__combine_data(gender, season_option))
