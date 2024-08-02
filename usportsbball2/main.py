from player_stats import construct_player_urls
from team_stats import get_men_team_stats, get_women_team_stats  # noqa: F401


def main():
    urls = construct_player_urls(gender="men")
    # women_team_stats = get_women_team_stats()
    # print(women_team_stats.info())


if __name__ == "__main__":
    main()
