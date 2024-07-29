import asyncio
import pandas as pd
from typing import Any, List
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from utils import parse_standings_table, merge_data
from values import standings_column_list


async def fetch_standings_data(standings_url: str) -> List[dict[str, Any]]:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, timeout=10000)
        page = await browser.new_page()
        await page.goto(standings_url, timeout=60 * 1000)
        tables = await page.query_selector_all("tbody")
        print(f"Number of tables found: {len(tables)}")
        tables_length = len(tables)
        all_standings = []
        for i in range(0, tables_length):
            table = await tables[i].inner_html()

            standings_html = table.replace("\n", "").replace("\t", "")

            soup = BeautifulSoup(standings_html, "html.parser")

            standings_data = parse_standings_table(soup, standings_column_list)
            all_standings = merge_data(all_standings, standings_data)

        await browser.close()
        return all_standings


async def main():
    standings_url = (
        "https://universitysport.prestosports.com/sports/wbkb/2023-24/standings-conf"
    )

    # Fetch standings data
    standings_data = await fetch_standings_data(standings_url)
    print(f"There are this many standings data: {len(standings_data)}")

    df = pd.DataFrame(standings_data)
    print(df.info())
    print(df.head())


if __name__ == "__main__":
    asyncio.run(main())
