from colorama import Fore, Style

COMMENT = '%s%s' % (Style.DIM, Fore.LIGHTBLACK_EX)
FUNCTOR = '%s' % Fore.LIGHTWHITE_EX
VARIABLE = '%s' % Fore.MAGENTA
MUTE_VARIABLE = '%s%s' % (Style.DIM, Fore.MAGENTA)
STRING = '%s' % Fore.GREEN
VALUE = '%s' % Fore.CYAN
TERM = '%s' % Fore.WHITE
PUNCTUATION = '%s' % Fore.BLUE
SYMBOLS = '%s' % Fore.RED

RESET = '%s' % Style.RESET_ALL
