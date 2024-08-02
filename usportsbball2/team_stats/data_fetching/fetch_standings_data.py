from typing import Any, List

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from utils import merge_data, parse_standings_table

from ..settings.team_settings import standings_type_mapping


async def fetch_standings_data(standings_url: str) -> List[dict[str, Any]]:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, timeout=10000)
        page = await browser.new_page()

        await page.set_extra_http_headers(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
            }
        )
        # Block unnecessary resources
        await page.route(
            "**/*.{png,jpg,jpeg,gif,webp,css,woff2,woff,js}",
            lambda route: route.abort(),
        )

        print("Navigating to standings page")
        await page.goto(standings_url, timeout=30 * 1000, wait_until="networkidle")  # wait 30 sec
        print("standings clicked\n")

        await page.wait_for_selector("tbody", timeout=30 * 1000)  # Wait for table body to be present
        tables = await page.query_selector_all("tbody")

        tables_length = len(tables)
        print("Fetching standings")
        all_standings = []
        for i in range(0, tables_length):
            table = await tables[i].inner_html()

            standings_html = table.replace("\n", "").replace("\t", "")

            soup = BeautifulSoup(standings_html, "html.parser")

            column_names = list(standings_type_mapping.keys())[1:]
            standings_data = parse_standings_table(soup, column_names)
            all_standings = merge_data(all_standings, standings_data)

        await browser.close()
        print("done standings")
        return all_standings
