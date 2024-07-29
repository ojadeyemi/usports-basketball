import asyncio
import pandas as pd
from typing import Any
from playwright.async_api import async_playwright, Page
from bs4 import BeautifulSoup
from usportsbball2.team_stats.utils import merge_data, parse_team_stats_table
from usportsbball2.team_stats.values import columns_list, stat_group_options


async def fetch_table_html(page: Page, selector: str, option_value: str, index: int):
    await page.select_option("#stats-team-secondary-select", option_value, timeout=5000)
    await page.select_option(selector, "100", timeout=5000)

    tables = await page.query_selector_all("tbody")
    print(f"Number of tables found: {len(tables)}")

    if index < len(tables):
        table_html = await tables[index].inner_html()
        table_html = table_html.replace("\n", "").replace("\t", "")
        return table_html
    else:
        raise IndexError(
            f"Table index {index} is out of bounds. Only {len(tables)} tables found."
        )


async def fetch_team_stats(stats_url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, timeout=10000)
        page = await browser.new_page()
        # Set user-agent and other headers to mimic a real browser
        await page.set_extra_http_headers(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
            }
        )
        try:
            await page.goto(stats_url, timeout=60 * 1000)
            all_data = []

            for index, option in enumerate(stat_group_options):
                selector = f"#dt-length-{index}"
                table_html = await fetch_table_html(page, selector, option, index)

                soup = BeautifulSoup(table_html, "html.parser")
                columns = columns_list[
                    index
                ]  # Get the appropriate columns for the current stat group
                table_data = parse_team_stats_table(soup, index, columns)
                all_data = merge_data(all_data, table_data)

            return all_data
        except Exception as e:
            raise RuntimeError(f"Error fetching team stats: {e}")
        finally:
            await browser.close()


# Main function to run the process
async def main():
    stats_url = "https://universitysport.prestosports.com/sports/wbkb/2023-24/teams?sort=&r=0&pos=off"
    men_urls = [
        "https://universitysport.prestosports.com/sports/mbkb/2023-24/teams?sort=&r=0&pos=off",
        "https://universitysport.prestosports.com/sports/mbkb/2023-24/standings-conf",
    ]
    women_urls = [
        "https://universitysport.prestosports.com/sports/wbkb/2023-24/teams?sort=&r=0&pos=off",
        "https://universitysport.prestosports.com/sports/wbkb/2023-24/standings-conf",
    ]

    # Fetch HTML of team stats for all options
    mens_team_stats = await fetch_team_stats(stats_url)
    print(f"there are this many data {len(mens_team_stats)}")

    df = pd.DataFrame(mens_team_stats)
    print(df.info())
    final_df = df.groupby(["team_name", "games_played"], as_index=False).first()

    final_df.to_html("women.html")


if __name__ == "__main__":
    asyncio.run(main())
