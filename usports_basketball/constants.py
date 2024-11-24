"""Constants used across the U Sports basketball data fetching and processing modules."""

# Season identifier, update this when the season changes
SEASON = "2024-25"

# Mapping of season options to their corresponding URL fragments
SEASON_URLS = {"regular": SEASON, "playoffs": f"{SEASON}p", "championship": f"{SEASON}c"}

# Base URL for the U Sports website
BASE_URL = "https://universitysport.prestosports.com/sports"

# Timeout value (in milliseconds) for all Playwright operations
TIMEOUT = 50000  # 50 seconds
