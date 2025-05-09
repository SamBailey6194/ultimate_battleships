# This script holds all functions to do with the
# leaderboard logic.

# Access to correct google sheets
from style import StyledText
from sheets import small_game_lb, medium_game_lb, big_game_lb


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

    leaders = StyledText.bold(f"{title}\n")
    leaders += "-" * 35 + "\n"

    # Giving the columns a dynamic width
    position_width = 4
    username_width = 12
    score_width = 10

    # Leaderboard full width
    # (3 * 2) is for the 2 separators with characters ' | '
    leaderboard_width = (
        position_width + username_width + score_width + (3 * 2)
        )

    # Add column headings
    leaders += (
        StyledText.bold(
            f"{'Pos.':<{position_width}} | {'Username':<{username_width}} |"
            f" {'Game Score':<{score_width}}\n"
        )
    )
    leaders += "-" * leaderboard_width + "\n"

    # Add leaderboard entries
    for position, username in enumerate(sorted_lb, 1):
        leaders += (
            StyledText.bold(f"{position:<{position_width}}") + " |" +
            StyledText.bold(f" {username['Username']:<{username_width}}") +
            " |" + f" {username['Game Score']:<{score_width}}\n"
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
