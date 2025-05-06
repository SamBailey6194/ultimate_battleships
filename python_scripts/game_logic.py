# This script holds all the game logic classes

# Imported dependencies and modules
from random import choice
import time
# Imported other python scripts
from sheets import saved_games
from style import StyledText, Symbols
from save_load import Save, LoadGames
from board_creation import BoardSetup


class BoardAfterShots:
    def __init__(self, game):
        self.game = game

    def hit_counter(self, grid):
        """
        Counts the hits for each shot a player takes
        """
        return sum(
            row.count(Symbols.ship()) for row in grid
            )

    def valid_shot(self, row, col, board):
        """
        Refactord code to hold the validate the coordinates shot at
        """
        if not (
            0 <= row < len(board.grid) and 0 <= col < len(board.grid[0])
        ):
            print(f"Invalid coordinates: ({row}, {col})")
            return False
        return True

    def already_shot(self, board, general, row, col):
        """
        Refactored code to hold the explanation a shot has
        already been made there
        """
        if board.grid[row][col] in (Symbols.miss(), Symbols.hit()):
            time.sleep(1)
            print(
                f"{general} you have already shot here, please pick a"
                " new spot."
                )
            return False

    def hit(self, board, general, row, col):
        """
        Refactored code to hold the processing of when
        a shot hits a ship
        """
        hit_ship = StyledText.red("Hit")
        if board.grid[row][col] == Symbols.ship():
            board.grid[row][col] = Symbols.hit()

            if general == self.game.player:
                self.game.user_hits += 1
            else:
                self.game.computer_hits += 1

            ships_left = (
                self.game.total_ships - self.game.user_hits
                if general == self.game.player
                else self.game.total_ships - self.game.computer_hits
                )
            remaining_ships = StyledText.red(ships_left)
            time.sleep(1)
            print(
                f"{general} {hit_ship}!\n"
                f"Just {remaining_ships} left to destroy.", flush=True
                )
            return True

    def miss(self, board, general, row, col):
        """
        Refactored code to hold the processing of when
        a shot misses
        """
        miss_ship = StyledText.green("Miss")

        if board.grid[row][col] == Symbols.water():
            ships_left = (
                self.game.total_ships - self.game.user_hits
                if general == self.game.player
                else self.game.total_ships - self.game.computer_hits
                )
            remaining_ships = StyledText.red(ships_left)
            time.sleep(1)
            print(
                f"{general} {miss_ship}!\n"
                f"Just {remaining_ships} left to destroy.", flush=True
                )
            board.grid[row][col] = Symbols.miss()
            return True

    def update_board(self, general, board, row, col):
        """
        Function to update board that has been attacked
        """
        if not self.valid_shot(row, col, board):
            return False

        if self.already_shot(board, general, row, col):
            return False

        if self.hit(board, general, row, col):
            return True

        if self.miss(board, general, row, col):
            return True

        time.sleep(1)
        print(
            "Remember: The top left corner is row: 0, col: 0.\n"
            "Please bear that in mind when entering rows and columns."
            )
        return False

    def key(self):
        """
        Refactored code to hold the board key
        """
        water_ = StyledText.blue("Water")
        ship_ = StyledText.magenta("Ship")
        hit_ = StyledText.red("Hit")
        miss_ = StyledText.green("Miss")

        water_space = Symbols.water()
        ship_space = Symbols.ship()
        hit_space = Symbols.hit()
        miss_space = Symbols.miss()

        print("-" * 35)
        print(
            "Key:\n"
            f"{water_space} = {water_} \n"
            f"{ship_space} = {ship_}\n"
            f"{hit_space} = {hit_}\n"
            f"{miss_space} = {miss_}\n"
            )
        print("-" * 35)

    def boards_shown(self):
        """
        Refactored code to show the updated boards
        """
        print(f"{self.game.player}'s board:")
        self.game.player_board.display_board(show_ships=True)
        print("-" * 35)
        print("Computer's board:")
        self.game.pc_board.display_board(show_ships=False)
        print("-" * 35)

    def stats(self):
        """
        Refactored code to display the game stats
        """
        print("-" * 35)

        user_hits = StyledText.red(str(self.game.user_hits))
        computer_hits = StyledText.red(str(self.game.computer_hits))
        total_ships = StyledText.magenta(
            str(self.game.player_board.total_ships)
            )

        print(f"{self.game.player} hits: {user_hits}/{total_ships}")
        print(f"Computer hits: {computer_hits}/{total_ships}")
        print("-" * 35)

    def update_game_status(self):
        """
        Updates the game board after shots are taken
        """
        time.sleep(1.5)
        self.key()
        self.boards_shown()
        self.stats()
        time.sleep(1.5)


class ShotTracker:
    def __init__(self, game):
        self.game = game
        self.available_coordinates = []

    def random_coordinate(self, coordinates):
        """
        Helper method to generate random coordinates
        """
        return choice(coordinates)

    def reset_coordinates(self, size):
        """
        Resets the coordinates the computer can choose from when starting
        a new game or loading in a saved game
        """
        self.available_coordinates = [
            (row, col) for row in range(size) for col in range(size)
            if self.game.player_board.grid[row][col] in (
                Symbols.water(), Symbols.ship()
                )
        ]

    def shots_fired(self, player_name, target_board, is_user):
        """
        This asks for user to fire their shots and takes a random
        shot for the computer
        """
        board = BoardSetup(
            self.game.player,
            self.game.player_board.total_ships,
            self.game.player_board,
            self.game.pc_board
            )
        size = target_board.size

        if not self.available_coordinates:
            self.reset_coordinates(target_board.size)

        while True:
            if is_user:
                print("-" * 35)
                row = board.validate_coordinates(
                    "Enter row to shoot at: \n", size
                    )
                print("-" * 35)
                col = board.validate_coordinates(
                    "Enter col to shoot at: \n", size
                    )
                print("-" * 35)
            else:
                shot = self.random_coordinate(self.available_coordinates)
                row, col = shot
                self.available_coordinates.remove(shot)

            if self.game.board_management.update_board(
                player_name,
                target_board,
                row,
                col
            ):
                break


class TurnTracker:
    def __init__(self, game):
        self.game = game

    def player_turn(self):
        """
        Player turn taken
        """
        time.sleep(1.5)
        print("-" * 35)
        print("Time to take your shot! Fire!!!!!!")
        self.game.shot.shots_fired(
            self.game.player,
            self.game.pc_board,
            is_user=True,
            )
        time.sleep(1.5)

    def computer_turn(self):
        """
        Computer turn taken
        """
        print("-" * 35)
        print("Computer's turn, let's hope they miss!!!")
        print("-" * 35)
        time.sleep(1.5)
        self.game.shot.shots_fired(
            "Computer",
            self.game.player_board,
            is_user=False,
            )


class Gameplay:
    def __init__(self, game):
        self.game = game

    def delete_game(self):
        """
        Function that deletes a game from the database if it has been
        loaded in and completed
        """
        games = LoadGames(
            game_id=None,
            username=self.game.player,
            player_board=None,
            computer_board=None,
            games=None,
            player_colour=None,
            computer_colour=None
            )

        player_games, _ = games.load_saved_games()
        saves = saved_games.get_all_records()

        delete_row = []
        for id, row in enumerate(saves, start=2):
            if (
                row.get("Game ID") == self.game.game_id
            ):
                delete_row.append(id)

        for row_id in reversed(delete_row):
            saved_games.delete_rows(row_id)

    def game_over_check(self):
        """
        Checks after shots taken if the game is over and congratulates
        winner
        """
        if (
            self.game.user_hits == self.game.total_ships and
            self.game.computer_hits == self.game.total_ships
        ):
            print("Both players took out each other. Game is a tie")
            return True
        elif self.game.user_hits == self.game.total_ships:
            print(
                f"{self.game.player}, you win!!!! You beat the computer."
                )
            return True
        elif self.game.computer_hits == self.game.total_ships:
            print(
                f"Computer wins!!! Unlucky {self.game.player},"
                " maybe next time."
                )
            return True
        else:
            return False

    def save_game(self):
        """
        Saves the game by calling the Save class
        """
        save_state = Save(
            self.game.game_id,
            self.game.player,
            self.game.player_board.size,
            self.game.player_board.total_ships,
            self.game.player_board,
            self.game.pc_board,
            self.game.user_hits,
            self.game.computer_hits,
            self.game.shot.available_coordinates
        )

        return save_state.save_game_state()

    def play_game(self):
        """
        Starts or resumes the game and checks when the game finishes
        """
        updated_game_state = BoardAfterShots(self.game)

        while True:
            self.game.turn.player_turn()
            self.game.turn.computer_turn()
            self.game.board_management.update_game_status()

            if self.game_over_check():
                self.delete_game()
                return "game over"

            continue_save_exit = self.save_game()
            if continue_save_exit == "continue":
                updated_game_state.boards_shown()
                continue
            elif continue_save_exit == "save":
                return "saved"
            elif continue_save_exit == "exit":
                return "exit"
