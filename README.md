# usports-basketball [![PyPI Latest Release](https://img.shields.io/pypi/v/usports-basketball?color=orange)](https://pypi.org/project/usports-basketball/) [![License](https://img.shields.io/pypi/l/usports-basketball.svg)](https://github.com/ojadeyemi/usports-basketball/blob/main/LICENSE) [![Downloads](https://static.pepy.tech/badge/usports-basketball)](https://pepy.tech/project/usports-basketball) [![Package Status](https://img.shields.io/pypi/status/usports-basketball.svg)](https://pypi.org/project/usports-basketball/)

**usports-basketball** is a Python package that fetches and analyzes current basketball stats from the [U Sports website](https://usports.ca/en). With two simple functions—one for fetching team stats and the other for player stats—users can easily retrieve detailed data for either the men's or women's league. Each function returns a DataFrame with the relevant statistics statistics, allowing users to gather data for analysis and insights.

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

## Functions

### `usports_team_stats`

This function fetches and processes team statistics data, including standings, win-loss totals, shooting percentages, and other relevant team metrics for the current U Sports basketball season.

#### Parameters

- `arg` (str): The league for which you want to retrieve team statistics. Valid values are `'men'` and `'women'`.

#### Returns

- `DataFrame`: A pandas DataFrame containing the team statistics data.

### `usports_player_stats`

This function fetches and processes player statistics data, including total games played, points scored, shooting percentages, rebounds, assists, turnovers, steals, blocks, and other individual player metrics for the current U Sports basketball season.

#### Parameters

- `arg` (str): The league for which you want to retrieve player statistics. Valid values are `'men'` and `'women'`.

#### Returns

- `DataFrame`: A pandas DataFrame containing the player statistics data.

## Examples

- ### Fetching current stats from the league

```python
from usports_basketball import usports_team_stats, usports_player_stats

# Fetching and processing men's team statistics
men_team_stats_df = usports_team_stats('men')

# Fetching and processing men's player statistics
men_player_stats_df = usports_player_stats('men')

# Fetching and processing women's team statistics
women_team_stats_df = usports_team_stats('women')

# Fetching and processing women's player statistics
women_player_stats_df = usports_player_stats('women')
```

- ### Viewing Column Names

```python
# Use these code snippets to see all column names in each DataFrame
# For the team statistics DataFrame
print("Column names in men's player statistics DataFrame:")
print(men_player_stats_df.columns.tolist())

# For the player statistics DataFrame
print("\nColumn names in men's player statistics DataFrame:")
print(men_player_stats_df.columns.tolist())
```

- ### Getting top 10 scorers in OUA Conference (Men's League)

```python
# Initialize a DataFrame to store OUA teams
oua_teams_df = women_team_stats_df[women_team_stats_df['conference'].isin(['OUA East', 'OUA West', 'OUA Central'])][['team_name']].copy()
# Filter the DataFrame to include only players from the OUA conference
oua_players_df = men_player_stats_df[men_player_stats_df['school'].isin(oua_teams_df['team_name'])]

# Calculate points per game (PPG) for each player. Rounded to 2 decimal places
oua_players_df['points_per_game'] = round(oua_players_df['total_points'] / oua_players_df['games_played'], 2)

# Sort the DataFrame by points per game in descending order
oua_players_df = oua_players_df.sort_values(by='points_per_game', ascending=False)

# Retrieve the top 10 players leading in points per game
top_10_players = oua_players_df.head(10)

# Print the top 10 players
print(top_10_players[['lastname_initials', 'first_name', 'school', 'points_per_game']].to_string(index=False))
```

- ### Getting teams who have at least 5 games in a row (Women's League)

```python
# Filter the DataFrame to include only teams with a streak of 5+ wins
teams_with_win_streak = women_team_stats_df[women_team_stats_df['streak'].str.startswith('W', na=False)].copy()

# Convert 'streak' column to numeric for comparison
teams_with_win_streak['streak'] = teams_with_win_streak['streak'].str.extract('(\d+)').astype(float)

# Filter teams with streak of 5+ wins
teams_with_5plus_wins = teams_with_win_streak[teams_with_win_streak['streak'] >= 5]

# Print teams with streak of 5+ wins
print("Teams with streak of 5+ wins:")
print(teams_with_5plus_wins[['team_name', 'games_played', 'conference', 'win_percentage']])
```

- ### Exporting DataFrame to different files

```python
# Export the  to a CSV file using the `to_csv()` method
men_team_stats_df.to_csv('men_team_stats.csv', index=False)  # Export without row index

#Export to a HTML table representation using to_html method
men_team_stats_df.to_html('table.html')

#Export to a JSON file using the to_json() method
men_team_stats_df.to_json('men_team_stats.json', orient='records') # Export in 'records' format

#Export to a SQL database using the to_sql() method (requires SQLAlchemy)
from sqlalchemy import create_engine

engine = create_engine('sqlite:///usports_stats.db') #Export to SQLite database
women_team_stats_df.to_sql('team_stats', con=engine, index=False) # Export without row index
women_player_stats_df.to_sql('player_stats', con=engine, index=False) # Export without row index
```

## Explore [Pandas DataFrame](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html) documentation for instructions on manipulating data and performing data analysis.

## Author

This package was developed by OJ Adeyemi.

## Contributing

Contributions, bug reports, and feature requests are welcome! Please feel free to open an issue or submit a pull request on [GitHub](https://github.com/ojadeyemi/usports-basketball).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
for details.
