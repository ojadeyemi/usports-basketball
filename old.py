from playwright.async_api import async_playwright

async def fetch_team_data(stats_url, standings_url, no_of_teams):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            # Navigate to the stats URL with a timeout of 2 minutes
            await page.goto(stats_url, timeout=2 * 60 * 1000)

            # Wait for the page to load completely
            await page.wait_for_timeout(500)

            # Select the dropdown element and choose '100' entries to display
            await page.select_option("#dt-length-0", "100")

            # Get all 'tbody' elements on the page
            tbodies = await page.query_selector_all("tbody")

            # Check if 'tbody' elements are present
            if len(tbodies) == 0:
                print("No tbody elements found")
                return

            # Select the first 'tbody' element
            first_tbody = tbodies[0]

            # Get all rows within the first 'tbody'
            rows = await first_tbody.query_selector_all("tr")

            # Log the number of rows for debugging
            print(f"Number of rows: {len(rows)}")

            data = []  # Array to store the extracted data

            # Iterate over each row in the table
            for row in rows:
                # Get all 'td' elements within each row
                cols = await row.query_selector_all("td")

                # Check if there are more than one column in the row
                if len(cols) > 1:
                    # Push the extracted data into the array
                    data.append({
                        "team_name": await cols[1].inner_text(),
                        "games_played": await cols[2].inner_text(),
                        "field_goals": await cols[3].inner_text(),
                        "field_goal_percentage": await cols[4].inner_text(),
                        "three_pointers": await cols[5].inner_text(),
                        "three_point_percentage": await cols[6].inner_text(),
                        "free_throws": await cols[7].inner_text(),
                        "free_throw_percentage": await cols[8].inner_text(),
                        "points_per_game": await cols[9].inner_text(),
                    })

            print(data)
        except Exception as e:
            print(f"Error fetching team data: {e}")
        finally:
            # Ensure the browser is closed even if an error occurs
            await browser.close()

# Main execution block
async def main():
    # URLs for men’s and women’s teams and standings
    men_urls = [
        "https://universitysport.prestosports.com/sports/mbkb/2023-24/teams?sort=&r=0&pos=off",
        "https://universitysport.prestosports.com/sports/mbkb/2023-24/standings-conf",
    ]
    women_urls = [
        "https://universitysport.prestosports.com/sports/wbkb/2023-24/teams?sort=&r=0&pos=off",
        "https://universitysport.prestosports.com/sports/wbkb/2023-24/standings-conf",
    ]

    # Fetch data for men's teams
    await fetch_team_data(men_urls[0], men_urls[1], 52)

    print("Data has been fetched.")

import asyncio
asyncio.run(main())
