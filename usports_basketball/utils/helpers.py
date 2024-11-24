import re
import unicodedata
from typing import Literal

from pandas import DataFrame
from playwright.async_api import Page


async def fetch_table_html(page: Page, index: int):
    """Fetch HTML of a specific table from a page."""
    tables = await page.query_selector_all("tbody")
    if index < len(tables):
        table_html = await tables[index].inner_html()
        table_html = table_html.replace("\n", "").replace("\t", "")

        return table_html

    raise IndexError(f"Table index {index} is out of bounds. Only {len(tables)} tables found.")


def split_made_attempted(value: str) -> tuple[int, int]:
    """Split shots into made and attempted (e.g., '12-20' to 12 and 20)."""
    try:
        made, attempted = value.split("-")
        return int(made), int(attempted)

    except ValueError as e:
        raise ValueError(f"Error splitting made and attempted values from '{value}': {e}") from e


def clean_text(text: str) -> str:
    """Remove non-ASCII characters and extra spaces from text."""
    # Normalize Unicode characters to a standard form
    normalized_text = unicodedata.normalize("NFKC", text)

    # Remove non-printable and non-ASCII characters using regex
    sanitized_text = re.sub(r"[^\x00-\x7F]", "", normalized_text)

    # Remove unwanted whitespace characters
    cleaned_text = re.sub(r"[\n\t]+", " ", sanitized_text)
    cleaned_text = re.sub(r"\s{2,}", " ", cleaned_text)

    return cleaned_text.strip()


def convert_types(df: DataFrame, type_mapping: dict[str, type]) -> DataFrame:
    """Convert DataFrame columns to specified types."""
    for column, dtype in type_mapping.items():
        if dtype in [int, float]:
            df[column] = df[column].replace("-", 0)

        df[column] = df[column].astype(dtype)

    return df


def get_sport_identifier(gender: str) -> str:
    """Get the sport identifier based on gender."""
    if gender == "men":
        return "mbkb"

    if gender == "women":
        return "wbkb"

    raise ValueError("Argument must be 'men' or 'women'")


def normalize_gender_arg(arg: Literal["m", "men", "w", "women"]) -> str:
    """Normalize the 'arg' input to 'men' or 'women'."""
    arg_lower = arg.lower()

    if arg_lower in ["m", "men"]:
        return "men"

    if arg_lower in ["w", "women"]:
        return "women"

    raise ValueError("The argument 'arg' should be either 'men', 'm', 'w', or 'women'")


def validate_season_option(season_option: str, available_options: dict) -> str:
    """Validate the season option and return the corresponding URL fragment."""
    season_option_lower = season_option.lower()
    if season_option_lower not in available_options:
        options = ", ".join(available_options.keys())
        raise ValueError(f"Invalid season_option: {season_option}. Must be one of {options}")

    return available_options[season_option_lower]
