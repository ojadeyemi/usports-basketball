# USports Basketball Statistics Package

## Introduction

The USports Basketball Statistics Package is a Python package designed to retrieve and analyze basketball statistics data from the USports website. This package provides functions for web scraping and processing both team and player statistics, allowing users to gather data for analysis and insights.

## Installation

You can install the package via pip:

```bash
pip install usports-basketball
```

## Dependencies

This package relies on the following dependencies:
- requests
- BeautifulSoup (bs4)
- pandas

Make sure you have these dependencies installed before using the package.

## Functions

### `usports_team_stats`

This function fetches and processes team statistics data, including standings, win-loss totals, shooting percentages, and other relevant team metrics for the current USports basketball season.

#### Parameters

- `arg` (str): The conference for which you want to retrieve team statistics. Valid values are `'men'` and `'women'`.

#### Returns

- `DataFrame`: A pandas DataFrame containing the team statistics data.

### `usports_player_stats`

This function fetches and processes player statistics data, including total games played, points scored, shooting percentages, rebounds, assists, turnovers, steals, blocks, and other individual player metrics for the current USports basketball season.

#### Parameters

- `arg` (str): The conference for which you want to retrieve player statistics. Valid values are `'men'` and `'women'`.

#### Returns

- `DataFrame`: A pandas DataFrame containing the player statistics data.

## Example Usage

```python
from usports_basketball import usports_team_stats, usports_player_stats

# Fetching and processing men's team statistics
men_team_stats_df = usports_team_stats('men')

# Fetching and processing men's player statistics
men_player_stats_df = usports_player_stats('men')
```

You can use the `.dtype` function to retrieve the data types of all columns in the DataFrame. This can be useful for understanding the structure of the data you've fetched. Here's how you can use it:

```python
# Assuming `usports_player_stats` returns a DataFrame named `men_player_stats_df`
# Fetching and processing men's player statistics
men_player_stats_df = usports_player_stats('men')

# Get the data types of all columns with their column names
column_dtypes = men_player_stats_df.dtypes

# Print the column names and their corresponding data types
print(column_dtypes)
```

## Note

- This package is based on the current USports basketball season only. To access statistics from previous seasons, manual adjustments to the web scraping code may be required.

## Author

This package was developed by OJ Adeyemi.

## Contributing

Contributions, bug reports, and feature requests are welcome! Please feel free to open an issue or submit a pull request on [GitHub](https://github.com/ojadeyemi/usports-basketball).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
for details.
