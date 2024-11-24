"""
Module for fetching and processing U Sports basketball player statistics.

This module provides a function to retrieve and combine player statistics
from the U Sports basketball league for both men's and women's teams.
It utilizes web scraping techniques to extract data from the U Sports website
and processes it into pandas DataFrames for further analysis.

Function:
- usport_players_stats: Fetch and combine current player statistics.

Author:
    OJ Adeyemi

Date Created:
    August 6, 2024
"""

import asyncio
import random
from typing import Literal

from pandas import DataFrame, concat
from pandas.errors import EmptyDataError

from usports_basketball.constants import BASE_URL, SEASON_URLS
from usports_basketball.utils import get_sport_identifier, normalize_gender_arg, setup_logging, validate_season_option

from .data_processing import get_players_stats_df
from .player_settings import sort_categories

logger = setup_logging()


def __construct_player_urls(gender: str, season_option: str) -> list[str]:
    sport = get_sport_identifier(gender)
    base_url = validate_season_option(season_option, SEASON_URLS)
    player_stats_url_template = f"{BASE_URL}/{sport}/{base_url}/players?pos=sh&r=0&sort={{sort_category}}"

    urls = [player_stats_url_template.format(sort_category=category) for category in sort_categories]

    return urls


async def __fetch_with_delay(url: str) -> DataFrame:
    await asyncio.sleep(random.uniform(0.5, 2.0))
    logger.debug(f"Fetching stats on category: {url[-5:]}")
    players_df = await get_players_stats_df(url)

    return players_df


async def __fetch_and_merge_player_stats(urls: list[str], batch_size: int = 10) -> DataFrame:
    """Fetch and merge player statistics data from a list of URLs."""
    all_dataframes = []
    num_of_urls = len(urls)

    for i in range(0, num_of_urls, batch_size):
        logger.debug(f"GETTING BATCH {i + 1} - {i + batch_size} out of {num_of_urls}")

        # Get the current batch of URLs
        batch_urls = urls[i : i + batch_size]

        # Fetch data for the current batch
        tasks = [__fetch_with_delay(url) for url in batch_urls]
        dataframes = await asyncio.gather(*tasks)

        all_dataframes.extend(dataframes)

    if not all_dataframes:
        raise EmptyDataError("No data received, all DataFrames are empty")

    # Combine all DataFrames, drop duplicates, and reset the index
    merged_df = concat(all_dataframes, ignore_index=True).drop_duplicates().reset_index(drop=True)

    return merged_df


def usport_players_stats(
    arg: Literal["m", "men", "w", "women"], season_option: Literal["regular", "playoffs", "championship"] = "regular"
) -> DataFrame:
    """
    Fetch and process player statistics data from the USports website.

    Args:
        arg (str): Gender of the players. Accepts 'men', 'women', 'm', or 'w' (case insensitive).
        season_option (str): The season option to fetch data for. Options are:
            - 'regular': Regular season statistics (default).
            - 'playoffs': Playoff season statistics.
            - 'championship': Championship season statistics.

    Returns:
        DataFrame: DataFrame containing processed player statistics.
    """
    gender = normalize_gender_arg(arg)
    season_option = season_option.lower()

    logger.info(f"FETCHING {gender.upper()} {season_option.upper()} SEASON PLAYERS STATS")
    urls = __construct_player_urls(gender, season_option)

    df = asyncio.run(__fetch_and_merge_player_stats(urls))

    return df
