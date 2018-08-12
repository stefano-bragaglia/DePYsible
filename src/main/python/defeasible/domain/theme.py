from colorama import Fore
from colorama import Style

COMMENT = '%s%s' % (Style.DIM, Fore.LIGHTBLACK_EX)
NEGATION = '%s%s' % (Style.BRIGHT, Fore.MAGENTA)
FUNCTOR = '%s%s' % (Style.NORMAL, Fore.LIGHTBLUE_EX)
VARIABLE = '%s%s' % (Style.NORMAL, Fore.RED)
MUTE_VARIABLE = '%s%s' % (Style.DIM, Fore.RED)
STRING = '%s%s' % (Style.NORMAL, Fore.GREEN)
VALUE = '%s%s' % (Style.NORMAL, Fore.CYAN)
TERM = '%s%s' % (Style.NORMAL, Fore.GREEN)
PUNCTUATION = '%s%s' % (Style.DIM, Fore.LIGHTWHITE_EX)

ARGUMENTATION = '%s%s' % (Style.NORMAL, Fore.MAGENTA)
UNCOVERED = '%s%s' % (Style.NORMAL, Fore.LIGHTRED_EX)

STRICT = '%s%s' % (Style.NORMAL, Fore.GREEN)
DEFEASIBLE = '%s%s' % (Style.NORMAL, Fore.YELLOW)

ANSWER = '%s%s' % (Style.NORMAL, Fore.BLUE)

RESET = '%s%s' % (Style.RESET_ALL, Fore.RESET)
