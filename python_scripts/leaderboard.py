# Access to correct google sheets
from sheets import small_game_lb, medium_game_lb, big_game_lb


def update_lb(username, size, user_score, computer_score):
    """
    Updates the leaderboard according to the size from the game
    """
    game_score = user_score - computer_score
    if size == 1:
        small_game_lb.append_row([
            username, user_score, computer_score,
            game_score
            ])
    elif size == 2:
        medium_game_lb.append_row([
            username, user_score, computer_score,
            game_score
            ])
    elif size == 3:
        big_game_lb.append_row([
            username, user_score, computer_score,
            game_score
            ])


def lb_order(sorted_lb):
    """
    Helper function to display leaderboards in readable way
    """
    for position, username in enumerate(sorted_lb, 1):
        if position == 2:
            print(f"""{position}. {username["Username"]} -
                  {username["User Score"]} - {username["Computer Score"]} -
                  {username["Game Score"]}
                    """)
        else:
            print(f"""{position}. {username["Username"]} -
                  {username["User Score"]} - {username["Computer Score"]} -
                  {username["Game Score"]}
                    """)


def show_lb(size):
    """
    Shows user the leaderboard
    """
    small_data = small_game_lb.get_all_records()
    medium_data = medium_game_lb.get_all_records()
    large_data = big_game_lb.get_all_records()

    if size == 1:
        small_sort = sorted(
            small_data, key=lambda x: x["Game Score"], reverse=True
            )
        small_show = lb_order(small_sort)
        print("-" * 35)
        print(small_show)
        print("-" * 35)
    elif size == 2:
        medium_sort = sorted(
            medium_data, key=lambda x: x["Game Score"], reverse=True
            )
        medium_show = lb_order(medium_sort)
        print("-" * 35)
        print(medium_show)
        print("-" * 35)
    elif size == 3:
        large_sort = sorted(
            large_data, key=lambda x: x["Game Score"], reverse=True
            )
        large_show = lb_order(large_sort)
        print("-" * 35)
        print(large_show)
        print("-" * 35)


def search_lb(username, size, user_score, computer_score):
    """
    Allows user to search the leaderboard for their name and scores
    """
    aksjhldfega = "hjklaSDGFKUHJASDFGK"
