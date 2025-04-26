# This script holds all functions to do with the
# leaderboard logic.

# Imported modules and dependencies
import colorama
from colorama import Style
# Access to correct google sheets
from sheets import small_game_lb, medium_game_lb, big_game_lb

# Initialise colorama
colorama.init(autoreset=True)


def update_lb(username, size, user_score, computer_score):
    """
    Updates the leaderboard according to the size from the game
    """
    game_score = user_score - computer_score
    if size == 5:
        small_game_lb.append_row([
            username, user_score, computer_score,
            game_score
            ])
    elif size == 10:
        medium_game_lb.append_row([
            username, user_score, computer_score,
            game_score
            ])
    elif size == 15:
        big_game_lb.append_row([
            username, user_score, computer_score,
            game_score
            ])


def lb_order(sorted_lb, size):
    """
    Helper function to display leaderboards in readable way
    """
    if size == 5:
        title = "Leaderboard for Small Game (5x5)"
    elif size == 10:
        title = "Leaderboard for Medium Game (10x10)"
    else:
        title = "Leaderboard for Large Game (15x15)"

    leaders = f"{Style.BRIGHT}{title}{Style.RESET_ALL}\n"
    leaders += "-" * 35 + "\n"

    # Add column headings
    leaders += (
        f"{Style.BRIGHT}Position | Username | User Score | Computer Score |"
        f" Game Score\n{Style.RESET_ALL}"
        )
    leaders += "-" * 35 + "\n"

    # Add leaderboard entries
    for position, username in enumerate(sorted_lb, 1):
        leaders += (
            f"{Style.BRIGHT}{position:<4}{Style.RESET_ALL} |"
            f" {Style.BRIGHT}{username['Username']:<8}{Style.RESET_ALL} |"
            f" {username['User Score']:<4} | {username['Computer Score']:<4}"
            f" {username['Game Score']}\n"
        )

    return leaders


def show_lb(size):
    """
    Shows user the leaderboard
    """
    small_data = small_game_lb.get_all_records()
    medium_data = medium_game_lb.get_all_records()
    large_data = big_game_lb.get_all_records()

    if size == 5:
        small_sort = sorted(
            small_data, key=lambda x: x["Game Score"], reverse=True
            )
        small_show = lb_order(small_sort, size)
        print("-" * 35)
        print(small_show)
        print("-" * 35)
    elif size == 10:
        medium_sort = sorted(
            medium_data, key=lambda x: x["Game Score"], reverse=True
            )
        medium_show = lb_order(medium_sort, size)
        print("-" * 35)
        print(medium_show)
        print("-" * 35)
    elif size == 15:
        large_sort = sorted(
            large_data, key=lambda x: x["Game Score"], reverse=True
            )
        large_show = lb_order(large_sort, size)
        print("-" * 35)
        print(large_show)
        print("-" * 35)


def search_lb(username, size, user_score=None, computer_score=None):
    """
    Allows user to search the leaderboard for their name and scores
    """
    if size == 5:
        data = small_game_lb.get_all_records()
    elif size == 10:
        data = medium_game_lb.get_all_records()
    elif size == 15:
        data = big_game_lb.get_all_records()
    else:
        print("Game size not recognised.")
        return

    search = [
        user_input for user_input in data
        if user_input["Username"].strip().lower() == username.strip()
    ]

    if search:
        sorted_search = sorted(
            search, key=lambda x: x["Game Score"], reverse=True
            )
        print(lb_order(sorted_search, size))
    else:
        print(f"No entries found for {username} on {size}x{size} leaderbaord.")
