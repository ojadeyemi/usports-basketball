"""
utils package

This package provides utility functions for processing data related to team standings and team stats.

Modules:
- parsing: Functions for parsing HTML tables.
  - parse_standings_table: Extracts standings data from an HTML table.
  - parse_team_stats_table: Extracts team stats data from an HTML table.

- type_conversion: Functions for converting data types.
  - convert_types: Converts DataFrame columns to specified types.

- data_processing: Functions for data manipulation and processing.
  - split_made_attempted: Splits a string into made and attempted values.
  - merge_data: Merges existing and new data, updating records.
  - clean_text: Cleans text by removing extra spaces and newlines.
"""

from .parsing import parse_standings_table, parse_team_stats_table
from .type_conversion import convert_types
from .data_processing import split_made_attempted, merge_data, clean_text

__all__ = [
    "parse_standings_table",
    "parse_team_stats_table",
    "convert_types",
    "split_made_attempted",
    "merge_data",
    "clean_text",
]
