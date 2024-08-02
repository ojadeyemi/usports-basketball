from bs4 import BeautifulSoup
from playwright.async_api import Page, async_playwright
from utils import merge_data, parse_team_stats_table

from ..settings.team_settings import stat_group_options, team_stats_columns_type_mapping


async def fetch_table_html(page: Page, selector: str, option_value: str, index: int):
    # await page.select_option("#stats-team-secondary-select", option_value, timeout=5000)
    # await page.select_option(selector, "100", timeout=5000)

    tables = await page.query_selector_all("tbody")

    if index < len(tables):
        table_html = await tables[index].inner_html()
        table_html = table_html.replace("\n", "").replace("\t", "")
        return table_html
    else:
        raise IndexError(f"Table index {index} is out of bounds. Only {len(tables)} tables found.")


async def fetch_team_stats(stats_url: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, timeout=10000)
        page = await browser.new_page()
        print("clicking on stats page")
        await page.set_extra_http_headers(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
            }
        )

        # Block unnecessary resources to speed up page load
        await page.route("**/*.{png,jpg,jpeg,gif,webp,css,woff2,woff,js}", lambda route: route.abort())

        try:
            await page.goto(stats_url, timeout=60 * 1000)
            all_data = []
            print("\nInital team_stats page clicked")
            for index, option in enumerate(stat_group_options):
                selector = f"#dt-length-{index}"
                print(f"Clicking on {selector}")
                table_html = await fetch_table_html(page, selector, option, index)

                soup = BeautifulSoup(table_html, "html.parser")
                columns = team_stats_columns_type_mapping[index]
                column_names = list(columns.keys())
                table_data = parse_team_stats_table(soup, index, column_names)
                all_data = merge_data(all_data, table_data)

            return all_data
        except Exception as e:
            raise RuntimeError(f"Error fetching team stats: {e}")
        finally:
            await browser.close()
