from colorama import Fore
from colorama import Style

COMMENT = '%s%s' % (Style.DIM, Fore.LIGHTBLACK_EX)
NEGATION = '%s%s' % (Style.NORMAL, Fore.CYAN)
FUNCTOR = '%s%s' % (Style.NORMAL, Fore.BLUE)
VARIABLE = '%s%s' % (Style.NORMAL, Fore.RED)
MUTE_VARIABLE = '%s%s' % (Style.DIM, Fore.RED)
STRING = '%s%s' % (Style.NORMAL, Fore.GREEN)
VALUE = '%s%s' % (Style.NORMAL, Fore.CYAN)
TERM = '%s%s' % (Style.NORMAL, Fore.GREEN)
PUNCTUATION = '%s%s' % (Style.DIM, Fore.WHITE)

STRICT = '%s%s' % (Style.NORMAL, Fore.MAGENTA)
DEFEASIBLE = '%s%s' % (Style.NORMAL, Fore.YELLOW)

ARGUMENTATION = '%s%s' % (Style.NORMAL, Fore.CYAN)

ANSWER = '%s%s' % (Style.NORMAL, Fore.BLUE)

RESET = '%s%s' % (Style.RESET_ALL, Fore.RESET)
