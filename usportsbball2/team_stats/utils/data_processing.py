import re
from typing import Any


def split_made_attempted(value: str) -> tuple[int, int]:
    try:
        made, attempted = value.split("-")
        return int(made), int(attempted)
    except ValueError as e:
        raise ValueError(
            f"Error splitting made and attempted values from '{value}': {e}"
        )


def clean_text(text: str) -> str:
    cleaned_text = re.sub(r"[\n\t]+", " ", text)
    cleaned_text = re.sub(r"\s{2,}", " ", cleaned_text)
    return cleaned_text.strip()


def merge_data(
    existing_data: list[dict[str, Any]], new_data: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    data_dict = {
        f"{item['team_name']}_{item['games_played']}": item for item in existing_data
    }

    for new_item in new_data:
        key = f"{new_item['team_name']}_{new_item['games_played']}"
        if key in data_dict:
            data_dict[key].update(new_item)
        else:
            data_dict[key] = new_item

    return list(data_dict.values())
