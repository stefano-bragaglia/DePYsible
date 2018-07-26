import os

from colorama import Fore, Style


def get_license():
    with open(os.path.join(os.path.dirname(__file__), 'resources', 'LICENSE'), 'r') as file:
        for i, row in enumerate(file):
            print('%s%s%s%s', (Style.DIM, Fore.WHITE, row, Style.RESET_ALL))
            if i % 23 == 0:
                command = input('%s%sPress %sReturn%s to continue, or %sQ%s (and %sReturn%s) to quit:%s ' % (
                    Style.DIM, Fore.WHITE, Fore.LIGHTWHITE_EX, Fore.WHITE, Fore.LIGHTWHITE_EX, Fore.WHITE,
                    Fore.LIGHTWHITE_EX, Fore.WHITE, Style.RESET_ALL))
                if command.strip().upper() == 'Q':
                    break
