""" BASIC TESTS"""
import pandas as pd

from usports_basketball import usports_team_stats, usports_player_stats

def test_usports_team_stats_returns_dataframe():
    """Test if usports_team_stats function returns a pandas DataFrame."""
    team_stats_df = usports_team_stats('men')
    assert isinstance(team_stats_df, pd.DataFrame)

def test_usports_player_stats_returns_dataframe():
    """Test if usports_player_stats function returns a pandas DataFrame."""
    player_stats_df = usports_player_stats('women')
    assert isinstance(player_stats_df, pd.DataFrame)

def test_usports_team_stats_non_empty():
    """Test if usports_team_stats function returns a non-empty DataFrame."""
    team_stats_df = usports_team_stats('women')
    assert not team_stats_df.empty, "Team statistics DataFrame is empty"

def test_usports_player_stats_non_empty():
    """Test if usports_player_stats function returns a non-empty DataFrame."""
    player_stats_df = usports_player_stats('men')
    assert not player_stats_df.empty, "Player statistics DataFrame is empty"

def test_usports_team_stats_columns():
    """Test if usports_team_stats function returns the expected columns."""
    team_stats_df = usports_team_stats('men')
    expected_columns = [
    'lastname_initials', 'first_name', 'team_name', 'games_played', 'points_per_game', 
    'field_goal_percentage', 'three_point_percentage', 'free_throw_percentage', 
    'offensive_rebounds_per_game', 'defensive_rebounds_per_game', 'total_rebounds_per_game', 
    'assists_per_game', 'turnovers_per_game', 'steals_per_game', 'blocks_per_game', 
    'team_fouls_per_game', 'offensive_efficiency', 'defensive_efficiency', 'Net_efficiency', 
    'field_goals_percentage_against', 'three_points_percentage_against', 
    'offensive_rebounds_per_game_against', 'defensive_rebounds_per_game_against', 
    'total_rebounds_per_game_against', 'assists_per_game_against', 'turnovers_per_game_against', 
    'steals_per_game_against', 'blocks_per_game_against', 'team_fouls_per_game_against', 
    'points_per_game_against', 'conference', 'field_goal_made', 'field_goal_attempted', 
    'three_pointers_made', 'three_pointers_attempted', 'free_throws_made', 'free_throws_attempted', 
    'field_goal_made_against', 'field_goal_attempted_against', 'three_pointers_made_against', 
    'three_pointers_attempted_against', 'total_wins', 'total_losses', 'win_percentage', 
    'last_ten_games', 'streak', 'total_points', 'total_points_against'
    ]

    actual_columns = team_stats_df.columns.tolist()
    for column in expected_columns:
        assert column in actual_columns, f"Expected column '{column}' not found in team_stats_df"

def test_usports_player_stats_columns():
    """Test if usports_player_stats function returns the expected columns."""
    player_stats_df = usports_player_stats('men')
    expected_columns = [
    'lastname_initials',
    'first_name',
    'school',
    'games_played',
    'games_started',
    'minutes_played',
    'offensive_rebounds',
    'defensive_rebounds',
    'total_rebounds',
    'personal_fouls',
    'disqualifications',
    'assists',
    'turnovers',
    'assist_per_turnover',
    'steals',
    'blocks',
    'field_goal_made',
    'field_goal_attempted',
    'field_goal_percentage',
    'three_pointers_made',
    'three_pointers_attempted',
    'three_pointers_percentage',
    'free_throws_made',
    'free_throws_attempted',
    'free_throws_percentage',
    'total_points'
]
    actual_columns = player_stats_df.columns.tolist()
    for column in expected_columns:
        assert column in actual_columns, f"Expected column '{column}' not found in player_stats_df"
