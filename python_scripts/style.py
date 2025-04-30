# Script that holds the function for colorama static methods

# Imported dependencies and modules
import colorama
from colorama import Fore, Back, Style


class StyledText:
    """
    Class that holds the static methods for colorama
    """
    @staticmethod
    def init_styles():
        colorama.init(autoreset=True)

    @staticmethod
    def bold(text):
        return f"{Style.BRIGHT}{text}{Style.RESET_ALL}"

    @staticmethod
    def yellow(text):
        return f"{Fore.YELLOW}{text}{Style.RESET_ALL}"

    @staticmethod
    def green(text):
        return f"{Fore.GREEN}{text}{Style.RESET_ALL}"

    @staticmethod
    def blue(text):
        return f"{Fore.BLUE}{text}{Style.RESET_ALL}"

    @staticmethod
    def magenta(text):
        return f"{Fore.MAGENTA}{text}{Style.RESET_ALL}"

    @staticmethod
    def red(text):
        return f"{Fore.RED}{text}{Style.RESET_ALL}"

    @staticmethod
    def white_bg(grid):
        return f"{Back.WHITE}{grid}{Style.RESET_ALL}"


class Symbols:
    """
    Colouring the symbols for the board
    """
    @staticmethod
    def water():
        return StyledText.blue("~")

    @staticmethod
    def ship():
        return StyledText.magenta("S")

    @staticmethod
    def hit():
        return StyledText.red("H")

    @staticmethod
    def miss():
        return StyledText.green("M")
