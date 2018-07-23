# import re
# from enum import Enum
# from typing import Dict, List, Optional, Set, Tuple, Iterable
# from typing import Union
#
# from arpeggio import ParserPython, visit_parse_tree
#
# Value = Union[bool, int, float, str]
# Variable = str
# Term = Union[Value, Variable]
# Substitutions = Dict[Variable, Term]
#
# _variable_pattern = re.compile(r'[_A-Z][a-z_0-9]*')
#
#
# class RuleType(Enum):
#     STRICT = 0
#     DEFEASIBLE = 1
#
#
# def is_variable(term: Term) -> bool:
#     return type(term) is str and _variable_pattern.match(term)
#
#
# def divide(clauses: Set['Rule']) -> Tuple[Set['Literal'], Set['Rule']]:
#     facts = set()
#     rules = set()
#     for rule in clauses:
#         if rule.is_fact() and rule.rule_type == RuleType.STRICT:
#             facts.add(rule.head)
#         else:
#             rules.add(rule)
#
#     return facts, rules
#
#
# def get_derivation(literal: 'Literal', rules: Set['Rule']) -> Optional[List['Literal']]:
#     def get_orderables(lit: 'Literal') -> Optional[Set[Tuple[int, 'Literal']]]:
#         if lit in facts:
#             return {(0, lit)}
#         else:
#             children = set()
#             for rule in rules:
#                 if rule.head == lit:
#                     pos = 0
#                     current = set()
#                     complete = True
#                     for future in rule.body:
#                         follows = get_orderables(future)
#                         if not follows:
#                             complete = False
#                             break
#
#                         for follow in follows:
#                             current.add(follow)
#                             pos = max(pos, follow[0])
#                     if complete:
#                         current.add((pos + 1, lit))
#                         children.update(current)
#                         return children
#
#             return None
#
#     facts, rules = divide(rules)
#     orderables = get_orderables(literal)
#     if not orderables:
#         return None
#
#     derivation = []
#     for _, current in sorted(orderables, key=lambda x: x[0]):
#         if current != literal and current not in orderables:
#             derivation.append(current)
#     derivation += [literal]
#
#     return derivation
#
#
# def is_contradictory(rules: Set['Rule']) -> bool:
#     positives = set()
#     negatives = set()
#     for rule in rules:
#         for literal in rule.get_literals():
#             first = negatives if literal.negated else positives
#             other = positives if literal.negated else negatives
#             if literal not in first:
#                 first.add(literal)
#                 complement = literal.get_complement()
#                 if complement in other and get_derivation(literal, rules) and get_derivation(complement, rules):
#                     return True
#
#     return False
#
#
# def get_combos(items):
#     combos = []
#     n = len(items)
#     for i in range(2 ** n):
#         combo = []
#         for j in range(n):
#             if (i >> j) % 2 == 1:
#                 combo.append(items[j])
#         combos.append(combo)
#
#     return sorted(combos, key=lambda x: len(x))
#
#
# def get_arguments(literal: 'Literal', rules: Set['Rule']) -> List['Structure']:
#     results = set()
#     stricts = {rule for rule in rules if rule.rule_type == RuleType.STRICT}
#     defeasibles = rules.difference(stricts)
#     for combo in get_combos(defeasibles):
#         rules = stricts.union(combo)
#         if not is_contradictory(rules):
#             if get_derivation(literal, rules):
#                 if not any(r in combo for r in results):
#                     results.add(combo)
#
#             # self.arguments = {}
#             # strict = list(self.get_strict())
#             # defeasible = list(self.get_defeasible())
#             # for lit in self.get_literals():
#             #     for combo in get_combos(defeasible):
#             #         rules = strict + combo
#             #         p = Program(*rules)
#             #         if not p.is_contradictory():
#             #             d = p.derives(lit)
#             #             if d:
#             #                 argument = Argument(lit, self, *combo)
#             #                 if lit not in self.arguments or \
#             #                         not any(a.is_sub_argument_of(argument) for a in self.arguments[lit]):
#             #                     self.arguments.setdefault(lit, set()).add(argument)
#
#         return {*self.arguments.values()}
#
#
# class Atom:
#     def __init__(self, functor: str, terms: List[Term]):
#         if functor is None or not functor.strip():
#             raise ValueError("'functor' is none or empty")
#         if terms is None:
#             raise ValueError("'terms' is none")
#
#         self.functor = functor
#         self.terms = terms
#
#     def __repr__(self):
#         if not self.terms:
#             return self.functor
#
#         return '%s(%s)' % (self.functor, ', '.join(str(term) for term in self.terms))
#
#     def __eq__(self, other):
#         if not isinstance(other, Atom):
#             return False
#         elif self is other:
#             return True
#         else:
#             return self.functor == other.functor \
#                    and self.terms == other.terms
#
#     def __hash__(self):
#         return hash(repr(self))
#
#     def __lt__(self, value):
#         if not isinstance(value, Atom):
#             return False
#
#         return repr(self) < repr(value)
#
#     def arity(self) -> int:
#         return len(self.terms)
#
#     def is_ground(self) -> bool:
#         for term in self.terms:
#             if is_variable(term):
#                 return False
#
#         return True
#
#     def unifies(self, ground: 'Atom') -> Optional[Substitutions]:
#         if not isinstance(ground, Atom):
#             return None
#
#         if self.functor != ground.functor:
#             return None
#
#         if self.arity() != ground.arity():
#             return None
#
#         substitutions = {}
#         for i, term in enumerate(self.terms):
#             if is_variable(term):
#                 if not term in substitutions:
#                     substitutions[term] = ground.terms[i]
#                 elif substitutions[term] != ground.terms[i]:
#                     return None
#
#             elif term != ground.terms[i]:
#                 return None
#
#         return substitutions
#
#     def substitutes(self, subs: Substitutions) -> 'Atom':
#         return Atom(self.functor, [subs.get(term, '_') if is_variable(term) else term for term in self.terms])
#
#
# class Literal:
#     @staticmethod
#     def parse(content: str) -> 'Literal':
#         from defeasible.grammar import literal, comment
#         from defeasible.visitor import DefeasibleVisitor
#
#         parser = ParserPython(literal, comment_def=comment)
#         parse_tree = parser.parse(content)
#
#         return visit_parse_tree(parse_tree, DefeasibleVisitor())
#
#     def __init__(self, negated: bool, atom: Atom):
#         if negated is None:
#             raise ValueError("'negated' is none")
#         if atom is None:
#             raise ValueError("'atom' is none")
#
#         self.negated = negated
#         self.atom = atom
#
#     def __repr__(self):
#         return ('~' if self.negated else '') + repr(self.atom)
#
#     def __eq__(self, other):
#         if not isinstance(other, Literal):
#             return False
#         elif self is other:
#             return True
#         else:
#             return self.negated == other.negated \
#                    and self.atom == other.atom
#
#     def __hash__(self):
#         return hash(repr(self))
#
#     def __lt__(self, value):
#         if not isinstance(value, Literal):
#             return False
#
#         if repr(self.atom) == repr(value.atom):
#             return self.negated < value.negated
#
#         return repr(self.atom) < repr(value.atom)
#
#     def unifies(self, ground: 'Literal') -> Optional[Substitutions]:
#         if not isinstance(ground, Literal):
#             return None
#
#         if self.negated != ground.negated:
#             return None
#
#         return self.atom.unifies(ground.atom)
#
#     def substitutes(self, subs: Substitutions) -> 'Literal':
#         return Literal(self.negated, self.atom.substitutes(subs))
#
#     @property
#     def functor(self) -> str:
#         return self.atom.functor
#
#     @property
#     def terms(self) -> List[Term]:
#         return self.atom.terms
#
#     def arity(self) -> int:
#         return self.atom.arity()
#
#     def is_ground(self) -> bool:
#         return self.atom.is_ground()
#
#     def get_complement(self):
#         return Literal(not self.negated, self.atom)
#
#     def get_derivation(self, program: 'Program', type_: 'RuleType' = RuleType.DEFEASIBLE) -> Optional[List['Literal']]:
#         if not program.is_ground():
#             program = program.infer_program()
#
#         return get_derivation(self, program.rules)
#
#     def get_arguments(self, program: 'Program') -> Optional[Iterable['Structure']]:
#         if not program.is_ground():
#             program = program.infer_program()
#
#         strict = program.get_strict()
#         defeasible = program.get_defeasible()
#
#         for combo in get_combos(defeasible):
#
#             pass
#
#         pass
#
#     def get_arguments(self):
#         if not self.is_ground():
#             return self.infer_program().get_arguments()
#
#         if not self.arguments:
#             self.arguments = {}
#             strict = list(self.get_strict())
#             defeasible = list(self.get_defeasible())
#             for lit in self.get_literals():
#                 for combo in get_combos(defeasible):
#                     rules = strict + combo
#                     p = Program(*rules)
#                     if not p.is_contradictory():
#                         d = p.derives(lit)
#                         if d:
#                             argument = Argument(lit, self, *combo)
#                             if lit not in self.arguments or \
#                                     not any(a.is_sub_argument_of(argument) for a in self.arguments[lit]):
#                                 self.arguments.setdefault(lit, set()).add(argument)
#
#         return {*self.arguments.values()}
#
#
# class Rule:
#     @staticmethod
#     def parse(content: str) -> 'Rule':
#         from defeasible.grammar import rule, comment
#         from defeasible.visitor import DefeasibleVisitor
#
#         parser = ParserPython(rule, comment_def=comment)
#         parse_tree = parser.parse(content)
#
#         return visit_parse_tree(parse_tree, DefeasibleVisitor())
#
#     def __eq__(self, other):
#         if not isinstance(other, Rule):
#             return False
#         elif self is other:
#             return True
#         else:
#             return self.head == other.head \
#                    and self.body == other.body \
#                    and self.rule_type == other.rule_type
#
#     def __hash__(self):
#         return hash(repr(self))
#
#     def __init__(self, head: Literal, rule_type: RuleType, *body: Literal):
#         self.head = head
#         self.body = sorted(l for l in set(body))
#         self.rule_type = rule_type
#
#     def __lt__(self, value):
#         if self.rule_type == value.rule_type:
#             if self.is_fact() == value.is_fact():
#                 if self.is_fact():
#                     return self.head < value.head
#
#                 if self.head == value.head:
#                     return self.body < value.body
#
#                 return self.head < value.head
#
#             return self.is_fact() < value.is_fact()
#
#         return self.rule_type.value < value.rule_type.value
#
#     def __repr__(self):
#         content = repr(self.head)
#         if self.body or self.rule_type == RuleType.DEFEASIBLE:
#             content += ' <- ' if self.rule_type == RuleType.STRICT else ' -< '
#         if self.body:
#             content += ', '.join(repr(l) for l in self.body)
#         content += '.'
#         return content
#
#     def is_fact(self) -> bool:
#         return not self.body
#
#     def is_ground(self) -> bool:
#         if not self.head.is_ground():
#             return False
#
#         for literal in self.body:
#             if not literal.is_ground():
#                 return False
#
#         return True
#
#     def get_literals(self) -> List[Literal]:
#         return [self.head] + self.body
#
#
# class Argument:
#     def __init__(self, conclusion: Literal, program: 'Program', *defeasibles: Rule):
#         self.conclusion = conclusion
#         self.program = program
#         self.defeasibles = []
#         for defeasible in defeasibles:
#             if defeasible.rule_type != RuleType.DEFEASIBLE:
#                 raise ValueError('Only defeasible rules are allowed')
#             if defeasible not in self.defeasibles:
#                 self.defeasibles.append(defeasible)
#
#     def __repr__(self):
#         return '<[%s], %s>' % (', '.join(repr(d) for d in self.defeasibles), repr(self.conclusion))
#
#     def attacks_at(self, other: 'Structure', lit: Literal) -> bool:
#         if self.program != other.program:
#             return False
#
#         for arg in self.program.get_arguments(lit):
#             if arg.is_sub_argument_of(other) and self.program.disagree(lit, self.conclusion):
#                 return True
#
#         return False
#
#     def is_sub_argument_of(self, other: 'Structure') -> bool:
#         if self.program != other.program:
#             return False
#
#         return all(rule in other.defeasibles for rule in self.defeasibles)
#
#     def is_strictly_more_specific_than(self, other: 'Structure') -> bool:
#         if self.program != other.program:
#             return False
#
#         found = False
#         pie_g = self.program.get_strict_rules()
#         f = [Rule(head, RuleType.STRICT) for head in self.program.get_derivable_literals()]
#         for h in get_combos(f):
#             strict = pie_g.union(h)
#             p = Program(*strict)
#             pa_1 = Program(*strict.union(self.defeasibles))
#             pa_2 = Program(*strict.union(other.defeasibles))
#             if p.derives(self.conclusion) and not pa_1.derives(self.conclusion, True):
#                 if not pa_2.derives(other.conclusion):
#                     return False
#             if not found and pa_2.derives(other.conclusion) \
#                     and not p.derives(other.conclusion, True) \
#                     and not pa_1.derives(self.conclusion):
#                 found = True
#
#         return found
#
#     def is_equi_specific_to(self, other: 'Structure') -> bool:
#         if self.program != other.program:
#             return False
#
#         if self.defeasibles != other.defeasibles:
#             return False
#
#         rules = self.program.get_strict()
#         h1 = Rule(self.conclusion, RuleType.STRICT)
#         if not Program(*rules.union({h1})).derives(other.conclusion, True):
#             return False
#
#         h2 = Rule(other.conclusion, RuleType.STRICT)
#         if not Program(*rules.union({h2})).derives(self.conclusion, True):
#             return False
#
#         return True
#
#     def is_proper_defeater_for_at(self, other: 'Structure', lit: Literal) -> bool:
#         if self.program != other.program:
#             return False
#
#         for arg in self.program.get_arguments(lit):
#             if arg.is_sub_argument_of(other) \
#                     and self.attacks_at(other, lit) \
#                     and self.is_strictly_more_specific_than(arg):
#                 return True
#
#         return False
#
#     def is_blocking_defeater_for_at(self, other: 'Structure', lit: Literal) -> bool:
#         if self.program != other.program:
#             return False
#
#         for arg in self.program.get_arguments(lit):
#             if arg.is_sub_argument_of(other) \
#                     and self.attacks_at(other, lit) \
#                     and self.is_strictly_more_specific_than(arg) \
#                     and arg.is_strictly_more_specific_than(self):
#                 return True
#
#         return False
#
#     def is_defeater_for(self, other: 'Structure'):
#         if self.program != other.program:
#             return False
#
#         for lit in self.program.get_literals():
#             if self.is_proper_defeater_for_at(other, lit):
#                 return True
#
#             if self.is_blocking_defeater_for_at(other, lit):
#                 return True
#
#         return False
#
#
# class Answer(Enum):
#     YES = 0
#     NO = 1
#     UNDECIDED = 2
#     UNKNOWN = 3
#
#
# class Program:
#     @staticmethod
#     def parse(content: str) -> 'Program':
#         from defeasible.grammar import program, comment
#         from defeasible.visitor import DefeasibleVisitor
#
#         parser = ParserPython(program, comment_def=comment)
#         parse_tree = parser.parse(content)
#
#         program = visit_parse_tree(parse_tree, DefeasibleVisitor())
#         if not program.is_valid():
#             raise ValueError('This program is invalid')
#
#         return program
#
#     def __eq__(self, other):
#         if not isinstance(other, Program):
#             return False
#         elif self is other:
#             return True
#         else:
#             return self.rules == other.rules
#
#     def __hash__(self):
#         return hash(self.rules)
#
#     def __init__(self, *rules: Rule):
#         self.rules = sorted(rule for rule in rules)
#         self.ground = None
#         self.arguments = None
#
#     def __repr__(self):
#         return '\n'.join(repr(rule) for rule in self.rules)
#
#     def get_facts(self) -> Set[Rule]:
#         return {rule for rule in self.rules if rule.rule_type == RuleType.STRICT and not rule.body}
#
#     def get_presumptions(self) -> Set[Rule]:
#         return {rule for rule in self.rules if rule.rule_type == RuleType.DEFEASIBLE and not rule.body}
#
#     def get_strict_rules(self) -> Set[Rule]:
#         return {rule for rule in self.rules if rule.rule_type == RuleType.STRICT and rule.body}
#
#     def get_defeasible_rules(self) -> Set[Rule]:
#         return {rule for rule in self.rules if rule.rule_type == RuleType.DEFEASIBLE and rule.body}
#
#     def get_strict(self) -> Set[Rule]:
#         return {rule for rule in self.rules if rule.rule_type == RuleType.STRICT}
#
#     def get_defeasible(self) -> Set[Rule]:
#         return {rule for rule in self.rules if rule.rule_type == RuleType.DEFEASIBLE}
#
#     def get_literals(self) -> Set[Literal]:
#         literals = set()
#         for rule in self.rules:
#             literals.add(rule.head)
#             for lit in rule.body:
#                 literals.add(lit)
#
#         return literals
#
#     def get_arguments(self):
#         if not self.is_ground():
#             return self.infer_program().get_arguments()
#
#         if not self.arguments:
#             self.arguments = {}
#             strict = list(self.get_strict())
#             defeasible = list(self.get_defeasible())
#             for lit in self.get_literals():
#                 for combo in get_combos(defeasible):
#                     rules = strict + combo
#                     p = Program(*rules)
#                     if not p.is_contradictory():
#                         d = p.derives(lit)
#                         if d:
#                             argument = Argument(lit, self, *combo)
#                             if lit not in self.arguments or \
#                                     not any(a.is_sub_argument_of(argument) for a in self.arguments[lit]):
#                                 self.arguments.setdefault(lit, set()).add(argument)
#
#         return {*self.arguments.values()}
#
#     # def get_arguments(self, lit: 'Literal'):
#     #     arguments = []
#     #     strict = list(self.get_strict())
#     #     defeasible = list(self.get_defeasible())
#     #     for combo in get_combos(defeasible):
#     #         rules = strict + combo
#     #         p = Program(*rules)
#     #         if not p.is_contradictory():
#     #             d = p.derives(lit)
#     #             if d:
#     #                 argument = Structure(lit, self, *combo)
#     #                 if not any(a.is_sub_argument_of(argument) for a in arguments):
#     #                     arguments.append(argument)
#     #
#     #     return arguments
#
#     def is_ground(self):
#         for rule in self.rules:
#             if not rule.is_ground():
#                 return False
#
#         return True
#
#     def is_contradictory(self) -> bool:
#         if not self.is_ground():
#             return self.infer_program().is_contradictory()
#
#         positives = set()
#         negatives = set()
#         for rule in self.rules:
#             for literal in rule.get_literals():
#                 first = negatives if literal.negated else positives
#                 other = positives if literal.negated else negatives
#                 if literal not in first:
#                     first.add(literal)
#                     complement = literal.get_complement()
#                     if complement in other and literal.get_derivation(self) and complement.get_derivation(self):
#                         return True
#
#         return False
#
#     def is_valid(self) -> bool:
#         return not Program(*self.infer_program().get_strict()).is_contradictory()
#
#     def infer_program(self) -> 'Program':
#         if self.is_ground():
#             return self
#
#         if not self.ground:
#             self.ground = fire_rules(self)
#
#         return self.ground
#
#     def derives(self, lit: Literal, strict: bool = False) -> List[Literal]:
#         for rule_type in RuleType:
#             if rule_type == RuleType.STRICT or not strict:
#                 for rule in self.rules:
#                     if rule.head == lit and rule.rule_type == rule_type and not rule.body:
#                         return [rule.head]
#
#                 for rule in self.rules:
#                     if rule.head == lit and rule.rule_type == rule_type and rule.body:
#                         result = []
#                         activated = True
#                         for b in rule.body:
#                             derivation = self.derives(b)
#                             if not derivation:
#                                 activated = False
#                                 break
#                             for l in derivation:
#                                 if l not in result:
#                                     result.append(l)
#                         if activated:
#                             if rule.head not in result:
#                                 result.append(rule.head)
#                             return result
#
#         return []
#
#     def get_derivable_literals(self, strict: bool = False) -> Set[Literal]:
#         literals = set()
#         for literal in self.get_literals():
#             if self.derives(literal, strict):
#                 literals.add(literal)
#
#         return literals
#
#     def disagree(self, lit1: 'Literal', lit2: 'Literal') -> bool:
#         rules = list(self.get_strict()) + [Rule(lit1, RuleType.STRICT), Rule(lit2, RuleType.STRICT)]
#         program = Program(*rules)
#
#         return program.is_contradictory()
#
#     # def query(self, literal: Literal) -> Answer:
#     #     def expand(node: Node):
#     #         for lit in self.get_literals():
#     #             for arg in self.get_arguments(lit):
#     #                 if arg.is_defeater_for(node.argument):
#     #                     node.defeaters.add(expand(Node(arg)))
#     #
#     #         return node
#     #
#     #     if literal not in self.get_literals():
#     #         return Answer.UNKNOWN
#     #
#     #     current = Answer.UNDECIDED
#     #     for argument in self.get_arguments(literal):
#     #         root = expand(Node(argument))
#     #         if not root.defeaters:
#     #             continue
#     #
#     #         status = root.mark()
#     #         if status == Status.UNDEFEATED:
#     #             return Answer.YES
#     #         current = Answer.NO
#     #
#     #     return current
#
#
# Payload = Tuple[List[Literal], Substitutions]
#
#
# class Root:
#     def __init__(self):
#         self.children = set()
#
#     def notify(self, ground: Literal):
#         for child in self.children:
#             child.notify(ground, {}, self)
#
#
# class Alfa:
#     def __init__(self, pattern: Literal, parent: Root):
#         self.parent = parent
#         self.pattern = pattern
#         self.name = repr(pattern)
#         self.memory = []
#         self.children = set()
#         parent.children.add(self)
#
#     def notify(self, ground: Literal, subs: Substitutions, parent: Root):
#         subs = self.pattern.unifies(ground)
#         if subs is not None:
#             payload = ([ground], subs)
#             if payload not in self.memory:
#                 self.memory.append(payload)
#                 for child in self.children:
#                     child.notify([ground], subs, self)
#
#
# class Beta:
#     def __init__(self, parent_1: Union[Alfa, 'Beta'], parent_2: Alfa):
#         self.parent_1 = parent_1
#         self.parent_2 = parent_2
#         self.name = '%s, %s' % (parent_1.name, parent_2.name)
#         self.memory = []
#         self.children = set()
#         parent_1.children.add(self)
#         parent_2.children.add(self)
#
#     def notify(self, ground: List[Literal], subs: Substitutions, parent: Union[Alfa, 'Beta']):
#         if parent is self.parent_1:
#             for ground_2, subs_2 in self.parent_2.memory:
#                 self._notify(ground, subs, ground_2, subs_2)
#         elif parent is self.parent_2:
#             for ground_1, subs_1 in self.parent_1.memory:
#                 self._notify(ground_1, subs_1, ground, subs)
#
#     @staticmethod
#     def _unifies(subs_1: Substitutions, subs_2: Substitutions) -> Optional[Substitutions]:
#         for var in set(subs_1).intersection(subs_2):
#             if subs_1[var] != subs_2[var]:
#                 return None
#
#         return {**subs_1, **subs_2}
#
#     def _notify(self, ground_1: List[Literal], subs_1: Substitutions, ground_2: List[Literal], subs_2: Substitutions):
#         subs = self._unifies(subs_1, subs_2)
#         if subs is not None:
#             ground = [*ground_1, *ground_2]
#             payload = (ground, subs)
#             if payload not in self.memory:
#                 self.memory.append(payload)
#                 for child in self.children:
#                     child.notify(ground, subs, self)
#
#
# class Leaf:
#     def __init__(self, rule: Rule, parent: Union[Alfa, Beta], root: Root, agenda: List):
#         self.parent = parent
#         self.rule = rule
#         self.name = repr(rule)
#         self.memory = []
#
#         self.root = root
#         self.agenda = agenda
#         parent.children.add(self)
#
#     def notify(self, ground: List[Literal], subs: Substitutions, parent: Union[Alfa, 'Beta']):
#         payload = (ground, subs)
#         if payload not in self.memory:
#             self.memory.append(payload)
#
#             lit = self.rule.head.substitutes(subs)
#             if self.rule.rule_type is RuleType.STRICT:
#                 fact = Rule(lit, self.rule.rule_type)
#                 if fact not in self.agenda:
#                     self.agenda.append(fact)
#
#             rule = Rule(lit, self.rule.rule_type, *ground)
#             if rule not in self.agenda:
#                 self.agenda.append(rule)
#
#             self.root.notify(lit)
#
#
# def fire_rules(program: Program) -> Program:
#     if program.is_ground():
#         return program
#
#     rules = []
#     table = {}
#     root = Root()
#     for rule in program.rules:
#         if rule.is_fact():
#             rules.append(rule)
#         else:
#             beta = None
#             for lit in rule.body:
#                 name = repr(lit)
#                 alfa = table.setdefault(name, Alfa(lit, root))
#                 if beta is None:
#                     beta = alfa
#                 else:
#                     name = '%s, %s' % (beta.name, alfa.name)
#                     beta = table.setdefault(name, Beta(beta, alfa))
#             Leaf(rule, beta, root, rules)
#
#     for fact in program.get_facts():
#         root.notify(fact.head)
#
#     return Program(*rules)
