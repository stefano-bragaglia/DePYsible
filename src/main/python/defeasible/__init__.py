import os
import re

from colorama import Fore, Style

from defeasible.domain.definitions import Program
from defeasible.domain.rendering import Renderer


def main():
    print('Welcome to Defeasible (version 0.0.1)')
    print('Type "help", "copyright", "credits" or "license" for more information.')

    program = Program([])
    while True:
        command = input('\n?- ').strip()

        if command == 'halt.':
            break

        elif command == 'listing.':
            print(Renderer.render(program))

        elif command == 'ground.':
            program = program.get_ground_program()

        elif command == 'parent.':
            program = program.get_variable_program()

        elif re.match(r'\[(.*)\]\.', command):
            filename = command[1:-2]
            try:
                with open(filename, 'r') as file:
                    program = Program.parse(file.read())
            except Exception as e:
                print('ERROR: %s' % str(e))

        else:
            rules = set(program.rules)
            try:
                rules.update(Program.parse(command).rules)
            except Exception as e:
                print('ERROR: %s' % str(e))
            else:
                program = Program(list(rules))


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
