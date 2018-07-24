from colorama import Fore, Style

COMMENT = '%s%s' % (Style.DIM, Fore.LIGHTBLACK_EX)
FUNCTOR = '%s%s' % (Style.NORMAL, Fore.WHITE)
VARIABLE = '%s%s' % (Style.NORMAL, Fore.MAGENTA)
MUTE_VARIABLE = '%s%s' % (Style.DIM, Fore.MAGENTA)
STRING = '%s%s' % (Style.NORMAL, Fore.GREEN)
VALUE = '%s%s' % (Style.NORMAL, Fore.CYAN)
TERM = '%s%s' % (Style.NORMAL, Fore.YELLOW)
PUNCTUATION = '%s%s' % (Style.DIM, Fore.BLUE)
SYMBOLS = '%s%s' % (Style.NORMAL, Fore.RED)

RESET = '%s' % Style.RESET_ALL
