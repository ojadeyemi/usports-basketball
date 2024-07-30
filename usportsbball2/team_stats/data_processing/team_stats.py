import pandas as pd
from ..data_fetching import fetch_team_stats
from ..utils import convert_types
from ..config.values import team_stats_columns_type_mapping


async def get_team_stats_df(stats_url: str) -> pd.DataFrame:
    team_stats = await fetch_team_stats(stats_url)

    df = pd.DataFrame(team_stats)

    invalid_rows_count = df[df["games_played"] == "-"].shape[0]
    if invalid_rows_count > 0:
        print(
            f"\nDropping {invalid_rows_count} rows with invalid 'games_played' values\n"
        )
        df = df[df["games_played"] != "-"]

    combined_type_mapping = {
        "team_name": str,
        "games_played": int,
    }

    for mapping in team_stats_columns_type_mapping:
        combined_type_mapping.update(mapping)

    df = convert_types(df, combined_type_mapping)
    return df
