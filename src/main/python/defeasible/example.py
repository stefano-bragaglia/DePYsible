from defeasible.domain.definitions import Literal, Program

if __name__ == '__main__':
    p = Program.parse("""
            bird(X) <- chicken(X).
            bird(X) <- penguin(X).
            ~flies(X) <- penguin(X).
            chicken(tina).
            penguin(tweety).
            scared(tina).
            flies(X) -< bird(X).
            flies(X) -< chicken(X), scared(X).
            nests_in_trees(X) -< flies(X).
            ~flies(X) -< chicken(X).
        """)
    print(p)
    print('-' * 80)
    print()
    q = p.infer_program()
    print(q)
    print('=' * 80)
    print()

    lit = Literal.parse('flies(tina)')
    print(lit, ':', q.query(lit))

    lit = Literal.parse('~flies(tina)')
    print(lit, ':', q.query(lit))

    lit = Literal.parse('flies(tweety)')
    print(lit, ':', q.query(lit))

    lit = Literal.parse('~flies(tweety)')
    print(lit, ':', q.query(lit))

    lit = Literal.parse('~stack(pile)')
    print(lit, ':', q.query(lit))

    # lit = Literal('chicken(tina)')
    # derivation = p.derives(lit, True)
    # print(lit, '==', ', '.join(repr(d) for d in derivation), '.')
    #
    # lit = Literal('flies(tina)')
    # derivation = p.derives(lit)
    # print(lit, '=', ', '.join(repr(d) for d in derivation), '.')
    #
    # lit = Literal('flies(tina)', True)
    # derivation = p.derives(lit)
    # print(lit, '=', ', '.join(repr(d) for d in derivation), '.')
    #
    # lit = Literal('bird(tweety)')
    # derivation = p.derives(lit, True)
    # print(lit, '==', ', '.join(repr(d) for d in derivation), '.')
    #
    # lit = Literal('flies(tweety)', True)
    # derivation = p.derives(lit, True)
    # print(lit, '==', ', '.join(repr(d) for d in derivation), '.')

    # arguments = []
    # for lit in p.get_literals():
    #     # print(lit)
    #     # print('-' * len(repr(lit)))
    #     for argument in p.get_arguments(lit):
    #         # print('***', argument)
    #         arguments.append(argument)
    #     # print()
    #
    # results = set()
    # for arg1 in arguments:
    #     for arg2 in arguments:
    #         for arg in arguments:
    #             if arg.is_sub_argument_of(arg2):
    #                 if p.disagree(arg.conclusion, arg1.conclusion):
    #                     adverb = 'directly' if arg.conclusion == arg1.conclusion else 'indirectly',
    #                     results.add((repr(arg1), adverb[0], 'attacks', repr(arg2), 'at', arg.conclusion))
    #                     # arg1.attacks[arg2] = arg.conclusion
    # for result in results:
    #     print(*result)
    #     print()

    # roots = {arg for arg in arguments if not arg.attacks}
    #
    # for root in roots:
    #     def stamp(arg, level=0):
    #         for child in arg.attacks:
    #             print(' ' * 4 * level, repr(arg), 'attacks', repr(child), 'at', arg.attacks[child])
    #             stamp(child, level + 1)
    #
    #
    #     stamp(root)

    # print(p.is_contradictory())

    # arg1 = Structure(Literal.parse('~flies(tina)'), p, Rule.parse('~flies(tina) -< chicken(tina).'))
    # arg2 = Structure(Literal.parse('flies(tina)'), p, Rule.parse('flies(tina) -< bird(tina).'))
    # print(arg1)
    # print(arg2)
    # print(arg1.is_strictly_more_specific_than(arg2))
    # print(arg2.is_strictly_more_specific_than(arg1))
    # print(arg1.is_equi_specific_to(arg2))
    # print(arg2.is_equi_specific_to(arg1))
    # print(arg1.is_equi_specific_to(arg1))
    # print(arg2.is_equi_specific_to(arg2))

    print()
    print('Done.')

    # if __name__ == '__main__':
    #     colorama.init()
    #     p = Program.parse("""
    #             bird(X) <- chicken(X).
    #             bird(X) <- penguin(X).
    #             ~flies(X) <- penguin(X).
    #             chicken(tina).
    #             penguin(tweety).
    #             scared(tina).
    #             flies(X) -< bird(X).
    #             flies(X) -< chicken(X), scared(X).
    #             nests_in_trees(X) -< flies(X).
    #             ~flies(X) -< chicken(X).
    #         """)
    #     print(p)
    #
    #     print('-' * 120)
    #
    #     print(p.get_ground_program())
    #
    #     print('-' * 120)
    #
    #     for literal in sorted(p.get_ground_program().as_literals()):
    #         print(literal, '>', ' ' * (25 - len(repr(literal))), p.get_derivation(literal))
    #
    #     print('-' * 120)
    #
    #     for literal in sorted(p.get_ground_program().as_literals()):
    #         arguments = p.get_arguments(literal)
    #         if not arguments:
    #             print(literal, '>', ' ' * (25 - len(repr(literal))), '-')
    #         else:
    #             print(literal, '>', ' ' * (25 - len(repr(literal))),
    #                   '\n                             '.join([repr(a) for a in arguments if a]))
    #
    #     print('-' * 120)
