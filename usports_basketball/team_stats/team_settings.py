"""Contains mappings and configurations for team statistics, conferences, and standings."""

team_stats_columns_type_mapping: list[dict[str, type]] = [
    {
        "field_goal_made": int,
        "field_goal_percentage": float,
        "three_pointers_made": int,
        "three_point_percentage": float,
        "free_throws_made": int,
        "free_throw_percentage": float,
        "points_per_game": float,
    },
    {
        "offensive_rebounds_per_game": float,
        "defensive_rebounds_per_game": float,
        "total_rebounds_per_game": float,
        "rebound_margin": float,
    },
    {
        "turnovers_per_game": float,
        "steals_per_game": float,
        "blocks_per_game": float,
        "assists_per_game": float,
    },
    {
        "team_fouls_per_game": float,
        "offensive_efficiency": float,
        "net_efficiency": float,
    },
    {
        "field_goal_made_against": int,
        "field_goal_percentage_against": float,
        "three_pointers_made_against": int,
        "three_point_percentage_against": float,
        "points_per_game_against": float,
    },
    {
        "offensive_rebounds_per_game_against": float,
        "defensive_rebounds_per_game_against": float,
        "total_rebounds_per_game_against": float,
        "rebound_margin_against": float,
    },
    {
        "turnovers_per_game_against": float,
        "steals_per_game_against": float,
        "blocks_per_game_against": float,
        "assists_per_game_against": float,
    },
    {
        "team_fouls_per_game_against": float,
        "defensive_efficiency": float,
        "net_efficiency_against": float,
    },
]


team_conference = {
    "Acadia": "AUS",
    "Alberta": "CW",
    "Algoma": "OUA West",
    "Bishop's": "RSEQ",
    "Brandon": "CW",
    "Brock": "OUA Central",
    "Calgary": "CW",
    "Cape Breton": "AUS",
    "Carleton": "OUA East",
    "Concordia": "RSEQ",
    "Dalhousie": "AUS",
    "Guelph": "OUA West",
    "Lakehead": "OUA Central",
    "Laurentian": "OUA East",
    "Laurier": "OUA West",
    "Laval": "RSEQ",
    "Lethbridge": "CW",
    "MacEwan": "CW",
    "Manitoba": "CW",
    "McGill": "RSEQ",
    "McMaster": "OUA Central",
    "Memorial": "AUS",
    "Mount Royal": "CW",
    "Nipissing": "OUA East",
    "Ontario Tech": "OUA East",
    "Ottawa": "OUA East",
    "Queen's": "OUA East",
    "Regina": "CW",
    "Saint Mary's": "AUS",
    "Saskatchewan": "CW",
    "StFX": "AUS",
    "Thompson Rivers": "CW",
    "Toronto": "OUA Central",
    "Toronto Metropolitan": "OUA Central",
    "Trinity Western": "CW",
    "UBC": "CW",
    "UBC Okanagan": "CW",
    "UFV": "CW",
    "UNB": "AUS",
    "UNBC": "CW",
    "UPEI": "AUS",
    "UQAM": "RSEQ",
    "Victoria": "CW",
    "Waterloo": "OUA West",
    "Western": "OUA West",
    "Windsor": "OUA West",
    "Winnipeg": "CW",
    "York": "OUA Central",
}

standings_type_mapping: dict[str, type] = {
    "team_name": str,
    "games_played": int,
    "total_wins": int,
    "total_losses": int,
    "ties": int,
    "win_percentage": float,
    "total_points": int,
    "total_points_against": int,
}

stat_group_options = {
    "Offense Shooting": "#sh-0",
    "Off Rebounding": "#rb-0",
    "Off Ball Control": "#bc-0",
    "Off Efficiency": "#eff-0",
    "Defense Shooting": "#dsh-0",
    "Def Rebounding": "#drb-0",
    "Defense Ball Control": "#dbc-0",
    "Def Efficiency": "#deff-0",
}