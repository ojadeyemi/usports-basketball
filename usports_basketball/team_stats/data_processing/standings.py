import pandas as pd

from usports_basketball.team_stats.data_fetching import fetching_standings_data
from usports_basketball.team_stats.team_settings import standings_type_mapping
from usports_basketball.utils import convert_types


async def get_standings_df(standings_url: str) -> pd.DataFrame:
    """function to handle stadnings data into a pandas DataFrame"""
    standings_data = await fetching_standings_data(standings_url)

    standings_df = pd.DataFrame(standings_data)

    standings_df = convert_types(standings_df, standings_type_mapping)
    standings_df = standings_df.drop(columns=["ties"])

    return standings_df
