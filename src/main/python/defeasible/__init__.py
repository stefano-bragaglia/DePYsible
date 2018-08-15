import os
import re
import subprocess

from colorama import Fore, Style

from defeasible.domain.definitions import Literal
from defeasible.domain.definitions import Program
from defeasible.domain.interpretation import Interpreter
from defeasible.domain.rendering import Renderer


def main(blind: bool = False):
    filename = None
    program = Program([])
    interpreter = Interpreter(program)

    show_intro()
    while True:
        command = input(prompt(blind)).strip()

        if command == 'halt':
            break

        elif command == 'credits':
            show_credits(blind)

        elif command == 'copyright':
            show_copyright(blind)

        elif command == 'edit':
            if not filename:
                filename = get_filename()
            subprocess.call(['nano', filename])

        # elif command == 'ground.':
        #     program = program.get_ground_program()

        elif command == 'help':
            show_help(blind)

        elif command == 'license':
            show_license(blind)

        elif command == 'listing':
            print(Renderer.render(program, blind=blind))

        # elif command == 'parent.':
        #     program = program.get_variable_program()

        elif command == 'reset':
            filename = None
            program = Program([])
            interpreter = Interpreter(program)

        elif re.match(r'\[(.*)\]', command):
            tmp_filename = command[1:-1]
            try:
                with open(tmp_filename, 'r') as file:
                    program = Program.parse(file.read())
                    interpreter = Interpreter(program)
            except Exception as e:
                show_error(str(e), blind)
            else:
                filename = tmp_filename

        else:
            try:
                literal = Literal.parse(command)
            except Exception:
                rules = set(program.rules)
                try:
                    rules.update(Program.parse(command).rules)
                except Exception as e:
                    show_error(str(e), blind)
                else:
                    program = Program(list(rules))
                    interpreter = Interpreter(program)
            else:
                answer, warrant = interpreter.query(literal)
                print(Renderer.render(answer, blind=blind))
                if warrant:
                    for rule in sorted(warrant):
                        print('\t', Renderer.render(rule, blind=blind))


def get_filename() -> str:
    i = 0
    while True:
        filename = os.path.join(os.getcwd(), 'defeasible_%d.pl' % i)
        if not os.path.exists(filename):
            return filename
        i += 1


def show_intro(blind: bool = False):
    import platform

    if blind:
        print('Welcome to Defeasible 0.0.1 (%s)' % platform.platform())
        print('Defeasible comes with ABSOLUTELY NO WARRANTY. This is free software.')
        print('Type "help", "copyright", "credits" or "license" for more information.')
        return

    print('%sWelcome to %sDefeasible 0.0.1%s %s(%s)%s%s' % (
        Fore.WHITE, Fore.BLUE, Fore.WHITE, Style.DIM, platform.platform(), Style.RESET_ALL, Fore.RESET))
    print('%sDefeasible%s comes with ABSOLUTELY NO WARRANTY. This is free software.%s' % (
        Fore.BLUE, Fore.WHITE, Fore.RESET))
    print('%sType %s"help"%s, %s"copyright"%s, %s"credits"%s or %s"license"%s for more information.%s' %
          (Fore.WHITE, Fore.YELLOW, Fore.WHITE, Fore.YELLOW, Fore.WHITE,
           Fore.YELLOW, Fore.WHITE, Fore.YELLOW, Fore.WHITE, Fore.RESET))


def prompt(blind: bool = False):
    if blind:
        return '\n?- '

    return '\n%s%s?- %s%s' % (Style.DIM, Fore.LIGHTWHITE_EX, Fore.RESET, Style.RESET_ALL)


def show_error(message: str, blind: bool = False):
    if blind:
        print('ERROR: %s' % message)

    print('%sERROR: %s%s' % (Fore.RED, message, Fore.RESET))


def show_credits(blind: bool = False):
    if blind:
        print('  This work was inspired by A. García and G. Simari. "Defeasible Logic Programming:')
        print('  An Argumentative Approach," in Theory and Practice of Logic Programming, ')
        print('  4(1):95–138, 2004. https://arxiv.org/abs/cs/0302029')

    print('  %s%sThis work was inspired by %sA. García and G. Simari. %s"Defeasible Logic Programming:%s%s' %
          (Style.DIM, Fore.WHITE, Style.RESET_ALL, Fore.BLUE, Fore.RESET, Style.RESET_ALL))
    print('  %s%sAn Argumentative Approach,"%s%s in %s%sTheory and Practice of Logic Programming%s%s,%s%s' %
          (Style.NORMAL, Fore.BLUE, Style.DIM, Fore.WHITE, Style.NORMAL, Fore.GREEN,
           Style.DIM, Fore.WHITE, Fore.RESET, Style.RESET_ALL))
    print('  %s%s4(1):95–138%s%s, %s%s2004%s%s. %s%shttps://arxiv.org/abs/cs/0302029%s%s' %
          (Style.NORMAL, Fore.CYAN, Style.DIM, Fore.WHITE, Style.NORMAL, Fore.YELLOW,
           Style.DIM, Fore.WHITE, Style.NORMAL, Fore.RED, Style.RESET_ALL, Fore.RESET))


def show_copyright(blind: bool = False):
    if blind:
        print("Copyright (c) 2018, Stefano Bragaglia")
        print("All rights reserved. https://github.com/stefano-bragaglia/DefeasiblePython")

    print("%s%sCopyright (c) 2018, %sStefano Bragaglia%s" % (Fore.WHITE, Style.DIM, Style.RESET_ALL, Fore.RESET))
    print("%s%sAll rights reserved. %s%shttps://github.com/stefano-bragaglia/DefeasiblePython%s%s" %
          (Style.DIM, Fore.WHITE, Style.NORMAL, Fore.RED, Fore.RESET, Style.RESET_ALL))


def show_help(blind: bool = False):
    if blind:
        print(' copyright   Shows copyright information')
        print(' credits     Shows credits information')
        print(' edit        Edit current program in external editor')
        print(' halt        Stops this interpreter\'s session')
        print(' license     Shows license')
        print(' listing     Lists the content of current program')
        print(' reset       Drop current program')

    print(' %scopyright   %sShows copyright information%s' % (Fore.YELLOW, Fore.WHITE, Fore.RESET))
    print(' %scredits     %sShows credits information%s' % (Fore.YELLOW, Fore.WHITE, Fore.RESET))
    print(' %sedit        %sEdit current program in external editor%s' % (Fore.YELLOW, Fore.WHITE, Fore.RESET))
    print(' %shalt        %sStops this session%s' % (Fore.YELLOW, Fore.WHITE, Fore.RESET))
    print(' %slicense     %sShows license%s' % (Fore.YELLOW, Fore.WHITE, Fore.RESET))
    print(' %slisting     %sLists the content of current program%s' % (Fore.YELLOW, Fore.WHITE, Fore.RESET))
    print(' %sreset       %sDrop current program%s' % (Fore.YELLOW, Fore.WHITE, Fore.RESET))


def show_license(blind: bool = False):
    if blind:
        print('Defeasible is covered by the Simplified BSD license:')
        print()
        print("Redistribution and use in source and binary forms, with or without")
        print("modification, are permitted provided that the following conditions are met:")
        print()
        print("* Redistributions of source code must retain the above copyright notice, this")
        print("  list of conditions and the following disclaimer.")
        print()
        print("* Redistributions in binary form must reproduce the above copyright notice,")
        print("  this list of conditions and the following disclaimer in the documentation")
        print("  and/or other materials provided with the distribution.")
        print()
        print("THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS \"AS IS\"")
        print("AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE")
        print("IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE")
        print("DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE")
        print("FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL")
        print("DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR")
        print("SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER")
        print("CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,")
        print("OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE")
        print("OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.")

    print('%sDefeasible%s is covered by the %sSimplified BSD license%s:%s' %
          (Fore.BLUE, Fore.WHITE, Fore.YELLOW, Fore.WHITE, Fore.RESET))
    print()
    for row in [
        "%s%sRedistribution and use in source and binary forms, with or without%s",
        "%s%smodification, are permitted provided that the following conditions are met%s:",
        "%s%s%s",
        "%s* %sRedistributions of source code must retain the above copyright notice, this%s",
        "%s  %slist of conditions and the following disclaimer.%s",
        "%s%s%s",
        "%s* %sRedistributions in binary form must reproduce the above copyright notice,%s",
        "%s  %sthis list of conditions and the following disclaimer in the documentation%s",
        "%s  %sand/or other materials provided with the distribution.%s"
    ]:
        print(row % (Fore.RED, Fore.WHITE, Fore.RESET))
    print()
    for row in [
        "%sTHIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS \"AS IS\"%s",
        "%sAND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE%s",
        "%sIMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE%s",
        "%sDISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE%s",
        "%sFOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL%s",
        "%sDAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR%s",
        "%sSERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER%s",
        "%sCAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,%s",
        "%sOR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE%s",
        "%sOF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.%s",
    ]:
        print(row % (Fore.CYAN, Fore.RESET))
