# Script that holds the function for colorama static methods

# Imported dependencies and modules
import colorama
from colorama import Fore, Style


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
        return f"{Fore.LIGHTYELLOW_EX}{text}{Style.RESET_ALL}"

    @staticmethod
    def green(text):
        return f"{Fore.LIGHTGREEN_EX}{text}{Style.RESET_ALL}"

    @staticmethod
    def blue(text):
        return f"{Fore.LIGHTBLUE_EX}{text}{Style.RESET_ALL}"

    @staticmethod
    def magenta(text):
        return f"{Fore.LIGHTMAGENTA_EX}{text}{Style.RESET_ALL}"

    @staticmethod
    def red(text):
        return f"{Fore.LIGHTRED_EX}{text}{Style.RESET_ALL}"


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
