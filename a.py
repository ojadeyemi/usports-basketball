import asyncio
import re
import pandas as pd
from typing import Any
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

NO_OF_TEAMS = 48


# Function to split values like "444-1000" into made and attempted
def split_made_attempted(value: str) -> tuple[int, int]:
    try:
        made, attempted = value.split("-")
        return int(made), int(attempted)
    except ValueError as e:
        raise ValueError(
            f"Error splitting made and attempted values from '{value}': {e}"
        )


def clean_text(text: str) -> str:
    # Remove newlines and tabs
    cleaned_text = re.sub(r"[\n\t]+", " ", text)
    # Replace multiple spaces with a single space
    cleaned_text = re.sub(r"\s{2,}", " ", cleaned_text)
    return cleaned_text.strip()


# Function to parse table data using BeautifulSoup
def parse_table_data(soup: BeautifulSoup, table_index: int, columns: list[str]):
    table_data: list[dict[str, Any]] = []
    tables = soup.find_all("tbody")

    table = tables[table_index]
    rows = table.find_all("tr")
    print(f"table len = {len(tables)} and rows len = {len(rows)}\n")
    team_count = 0

    for row in rows:
        if team_count >= NO_OF_TEAMS:
            print(f"Reached the maximum of {NO_OF_TEAMS} teams. Stopping.")
            break

        cols = row.find_all("td")
        if len(cols) > 1:
            row_data = {}
            team_name = clean_text(cols[1].get_text())
            games_played = clean_text(cols[2].get_text())
            row_data["team_name"] = team_name
            row_data["games_played"] = games_played
            for j, col in enumerate(columns):
                if j < len(cols) - 1:
                    value = cols[j + 3].get_text().strip()
                    if col in [
                        "field_goal_made",
                        "three_pointers_made",
                        "free_throws_made",
                        "field_goal_made_against",
                        "three_pointers_made_against",
                    ]:
                        made, attempted = split_made_attempted(value)
                        row_data[col] = made
                        row_data[col.replace("made", "attempted")] = attempted
                    else:
                        row_data[col] = value
            table_data.append(row_data)
            team_count += 1

    return table_data


# Function to fetch team stats from multiple tables
async def fetch_team_stats(stats_url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        try:
            await page.goto(stats_url, timeout=60 * 1000)

            await page.select_option("#dt-length-0", "100")

            # Get the page content
            html_content = await page.content()

            # Save the HTML content to a file
            with open("test.html", "w", encoding="utf-8") as file:
                file.write(html_content)
            print("HTML content saved to html file")

            # Parse the HTML content with BeautifulSoup
            soup = BeautifulSoup(html_content, "html.parser")

            columns_list = [
                [
                    "field_goal_made",
                    "field_goal_percentage",
                    "three_pointers_made",
                    "three_point_percentage",
                    "free_throws_made",
                    "free_throw_percentage",
                    "points_per_game",
                ],
                [
                    "offensive_rebounds_per_game",
                    "defensive_rebounds_per_game",
                    "total_rebounds_per_game",
                    "rebound_margin",
                ],
                [
                    "turnovers_per_game",
                    "steals_per_game",
                    "blocks_per_game",
                    "assists_per_game",
                ],
                ["team_fouls_per_game", "offensive_efficiency", "net_efficiency"],
                [
                    "field_goal_made_against",
                    "field_goal_percentage_against",
                    "three_pointers_made_against",
                    "three_point_percentage_against",
                    "points_per_game_against",
                ],
                [
                    "offensive_rebounds_per_game_against",
                    "defensive_rebounds_per_game_against",
                    "total_rebounds_per_game_against",
                    "rebound_margin_against",
                ],
                [
                    "turnovers_per_game_against",
                    "steals_per_game_against",
                    "blocks_per_game_against",
                    "assists_per_game_against",
                ],
                [
                    "team_fouls_per_game_against",
                    "defensive_efficiency",
                    "net_efficiency_against",
                ],
            ]

            all_data = []
            for i, columns in enumerate(columns_list):
                table_data = parse_table_data(soup, i, columns)
                all_data.extend(table_data)

            # Merge all data based on team_name and games_played
            merged_data = {}
            for entry in all_data:
                key = (entry["team_name"], entry["games_played"])
                if key not in merged_data:
                    merged_data[key] = entry
                else:
                    merged_data[key].update(entry)

            return list(merged_data.values())
        except Exception as e:
            print(f"Error fetching team stats: {e}")
        finally:
            await browser.close()


# Main function to run the process
async def main():
    stats_url = "https://universitysport.prestosports.com/sports/mbkb/2023-24/teams?sort=&r=0&pos=off"

    # Fetch team stats
    stats = await fetch_team_stats(stats_url)

    # Convert the stats to a DataFrame
    df = pd.DataFrame(stats)

    df.to_html("newteams.html")


if __name__ == "__main__":
    asyncio.run(main())
