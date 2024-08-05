import asyncio

from bs4 import BeautifulSoup
from playwright.async_api import Page, async_playwright

from ...utils import fetch_table_html, get_random_header, merge_player_data, parse_player_stats_table
from ..player_settings import player_stats_columns_type_mapping


async def fetch_table_data(page: Page, index: int, columns: dict[str, type]):
    """Fetch and parse a specific table from the page."""
    table_html = await fetch_table_html(page, index)
    soup = BeautifulSoup(table_html, "html.parser")
    column_names = list(columns.keys())
    return parse_player_stats_table(soup, column_names)


async def fetching_player_stats(url: str):
    """Function for handling fetching data from players stat url"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, timeout=10000)
        page = await browser.new_page()
        headers = get_random_header()
        await page.set_extra_http_headers(headers)

        # Block unnecessary resources to speed up page load
        await page.route("**/*.{png,jpg,jpeg,gif,webp,css,woff2,woff,js}", lambda route: route.abort())

        try:
            await page.goto(url, timeout=50000)
            tasks = [fetch_table_data(page, index + 3, player_stats_columns_type_mapping[index]) for index in range(3)]

            results = await asyncio.gather(*tasks)

            all_data = []
            for result in results:
                all_data = merge_player_data(all_data, result)

            return all_data

        except Exception as e:
            raise RuntimeError(f"Error fetching team stats: {e}") from e
        finally:
            await browser.close()
