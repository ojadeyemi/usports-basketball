from typing import Any

from bs4 import BeautifulSoup
from pandas import DataFrame
from playwright.async_api import Page, async_playwright

from ...utils import get_random_header, merge_team_data, parse_standings_table
from ..team_settings import standings_type_mapping


async def fetching_standings_data(standings_url: str) -> list[dict[str, Any]]:
    """function for handling fetch standings data from standings url"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, timeout=10000)
        page = await browser.new_page()

        headers = get_random_header()
        await page.set_extra_http_headers(headers)
        # Block unnecessary resources
        await page.route(
            "**/*.{png,jpg,jpeg,gif,webp,css,woff2,woff,js}",
            lambda route: route.abort(),
        )

        await page.goto(standings_url, timeout=10000, wait_until="networkidle")

        await page.wait_for_selector("tbody", timeout=10000)
        tables = await page.query_selector_all("tbody")

        tables_length = len(tables)

        all_standings = []
        for i in range(0, tables_length):
            table = await tables[i].inner_html()

            standings_html = table.replace("\n", "").replace("\t", "")

            soup = BeautifulSoup(standings_html, "html.parser")

            column_names = list(standings_type_mapping.keys())[1:]
            standings_data = parse_standings_table(soup, column_names)
            all_standings = merge_team_data(all_standings, standings_data)

        await browser.close()

        return all_standings


async def _fetch_team_record(page: Page, team_url: str, team_name: str) -> DataFrame:
    """Click the team's link, extract the team stats, and return them as a DataFrame with a team_name column."""
    await page.goto(team_url)

    # Extract the <ul> tag with the class name 'team-stats'
    ul_content = await page.locator("ul.team-stats").inner_html()

    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(ul_content, "html.parser")
    stats = {"team_name": team_name}

    # Mapping categories to DataFrame columns
    category_mapping = {"Overall": "overall", "PCT": "pct", "Conf": "conf", "C.PCT": "c.pct", "Streak": "streak", "Home": "home", "Away": "away", "Neutral": "neutral"}

    # Loop through each <li> tag and extract the relevant data
    for li in soup.find_all("li"):
        category = li.find("div", class_="small text-uppercase text-muted").get_text(strip=True)
        value = li.find("div", class_="fs-4 lh-1 text-nowrap fw-bold").get_text(strip=True)
        if category in category_mapping:
            stats[category_mapping[category]] = value

    # Convert the dictionary into a DataFrame with one row
    df = DataFrame([stats])
    print(df)
    return df


async def parse_team_links_and_fetch_data(page, team_name_tag: Any) -> DataFrame:
    """Fetch the data for a specific team based on the provided team_name_tag."""
    # Extract the team URL and name from the <a> tag
    href = team_name_tag.get("href")
    team_name = team_name_tag.get_text(strip=True)
    team_url = f"https://universitysport.prestosports.com{href}"

    print(f"Fetching data for team: {team_name}")

    # Fetch the team's data
    df = await _fetch_team_record(page, team_url, team_name)

    return df


async def fetch_all_teams_data(team_name_tags: list[Any]) -> list[DataFrame]:
    """Fetch data for all teams based on the provided list of <a> tags."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # Block unnecessary resources to speed up page load
        await page.route("**/*.{png,jpg,jpeg,gif,webp,css,woff2,woff,js}", lambda route: route.abort())

        all_team_data = []
        for team_name_tag in team_name_tags:
            df = await parse_team_links_and_fetch_data(page, team_name_tag)
            all_team_data.append(df)

        await browser.close()

    return all_team_data
