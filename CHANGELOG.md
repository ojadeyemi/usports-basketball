# Changelog

All notable changes to this project will be documented in this file.

## v2.0.3

### Removed

- **Team record data**: url doesn't work so I can't get `streak`, `home` and `away` team data

### Changed

- Increased rate limiting time

## v2.0.2

### Changed

- Updated data for the **2024-25** Season
- minor bug fixes

## v2.0.1

### Added

- Added **streak**, **home**, and **away** stats to `team_stats`.

### Changed

- Updated logger to format messages based on log level. DEBUG level includes state and name; other levels include only the message.

## v2.0.0

### Added

- This CHANGELOG file to start keeping track of the changes that happens in this library.
- Modularized package into sub_packages `team_stats`, `player_stats` and `utils`.
- testing scripts
- Implemented pytest in Github Actions workflow

### Changed

- Improved data fetching mechanism using Playwright.
- Updated implementation of `usport_players_stats` and `usport_team_stats` functions to handle season_options
