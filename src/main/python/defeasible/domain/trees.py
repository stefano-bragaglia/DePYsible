from enum import Enum
from typing import Dict
from typing import List
from typing import Optional
from typing import Set
from typing import Tuple

from defeasible.domain.definitions import Literal
from defeasible.domain.definitions import Program
from defeasible.domain.definitions import Rule
from defeasible.domain.definitions import RuleType


class Structure:
    def __init__(self, argument: Set[Rule], conclusion: Literal, derivation: 'Derivation'):
        self.argument = argument
        self.conclusion = conclusion
        self.derivation = derivation
        self._counter_arguments = None
        self._defeaters = None

    def __repr__(self) -> str:
        if not self.argument:
            return '<∅, %s>' % repr(self.conclusion)

        return '<{%s}, %s>' % (' ; '.join(repr(rule) for rule in self.argument), repr(self.conclusion))

    def counter_argue_at(self, structure: 'Structure', mode: RuleType = RuleType.DEFEASIBLE) \
            -> Optional['Structure']:
        if self.derivation.interpreter != structure.derivation.interpreter:
            return None

        if self.is_strict() or structure.is_strict():
            return None

        for literal in self.derivation.interpreter.get_heads(mode):
            for derivation in self.derivation.interpreter.get_derivations(literal, mode):
                disagreement = derivation.get_structure()
                if disagreement.is_subargument_for(structure) and \
                        disagree(disagreement.conclusion, self.conclusion, self.derivation.interpreter.sigma):
                    return disagreement

        return None

    def get_defeaters(self, mode: RuleType = RuleType.DEFEASIBLE) -> Set['Structure']:
        if self._defeaters is None:
            self._defeaters = set()
            for literal in self.derivation.interpreter.get_heads(mode):
                for derivation in self.derivation.interpreter.get_derivations(literal, mode):
                    defeater = derivation.get_structure()
                    if defeater.is_defeater_for(self):
                        self._defeaters.add(defeater)

        return self._defeaters

    def get_counter_arguments(self, structure: 'Structure', mode: RuleType = RuleType.DEFEASIBLE) -> Set['Structure']:
        if self.is_strict():
            return set()

        if self._counter_arguments is None:
            self._counter_arguments = dict()
            for literal in self.derivation.interpreter.get_heads(mode):
                for derivation in self.derivation.interpreter.get_derivations(literal, mode):
                    current = derivation.get_structure()
                    if current.is_strict():
                        continue

                    disagreement = self.counter_argue_at(current, mode)
                    if disagreement:
                        self._counter_arguments.setdefault(current, set()).add(disagreement)

        return self._counter_arguments.get(structure, set())

    def has_priority_over(self, structure: 'Structure') -> bool:
        preferable = False
        for rule1 in self.argument:
            for rule2 in structure.argument:
                if not (rule1.salience < rule2.salience):
                    return False

                preferable |= rule1.salience > rule2.salience

        return preferable

    def is_blocking_defeater_for(self, structure: 'Structure', mode: RuleType = RuleType.DEFEASIBLE) -> bool:
        for disagreement in self.get_counter_arguments(structure, mode):
            if disagreement.is_subargument_for(structure) and self.is_unrelated_to(disagreement):
                return True

        return False

    def is_defeater_for(self, content) -> bool:
        return self.is_blocking_defeater_for(content) or self.is_proper_defeater_for(content)

    def is_equi_specific_to(self, structure: 'Structure') -> bool:
        if self.derivation.interpreter != structure.derivation.interpreter:
            return False

        if self.argument != structure.argument:
            return False

        index = as_index(*self.derivation.interpreter.sigma, self.conclusion.as_fact())
        if not get_derivations(structure.conclusion, index):
            return False

        index = as_index(*self.derivation.interpreter.sigma, structure.conclusion.as_fact())
        if not get_derivations(self.conclusion, index):
            return False

        return True

    def is_preferable_to(self, structure: 'Structure') -> bool:
        if self.is_equi_specific_to(structure):
            return self.has_priority_over(structure)

        return self.is_strictly_more_specific_than(structure)

    def is_proper_defeater_for(self, structure: 'Structure', mode: RuleType = RuleType.DEFEASIBLE) -> bool:
        for disagreement in self.get_counter_arguments(structure, mode):
            if disagreement.is_subargument_for(structure) and self.is_preferable_to(disagreement):
                return True

        return False

    def is_strict(self) -> bool:
        return not self.argument

    def is_strictly_more_specific_than(self, structure: 'Structure'):
        if self.derivation.interpreter != structure.derivation.interpreter:
            return False

        more_specific = False
        for literal in self.derivation.interpreter.get_derivables():
            sigma_index = as_index(*self.derivation.interpreter.stricts, literal.as_fact())
            delta_index_2 = as_index(*structure.argument, index=sigma_index)
            delta_2 = bool(get_derivations(structure.conclusion, delta_index_2))
            if not delta_2:
                return False

            delta_index_1 = as_index(*self.argument, index=sigma_index)
            delta_1 = bool(get_derivations(self.conclusion, delta_index_1))
            sigma_1 = bool(get_derivations(self.conclusion, sigma_index))
            sigma_2 = bool(get_derivations(structure.conclusion, sigma_index))
            more_specific |= delta_2 and not sigma_2 and not delta_1
            if not delta_1 and sigma_1:
                continue

        return more_specific

    def is_subargument_for(self, structure: 'Structure') -> bool:
        for rule in self.argument:
            if rule not in structure.argument:
                return False

        return True

    def is_unrelated_to(self, structure: 'Structure') -> bool:
        return not self.is_preferable_to(structure) and not structure.is_preferable_to(self)


class Derivation:
    def __init__(self, rules: List[Rule], interpreter: 'Interpreter'):
        self.rules = rules
        self.interpreter = interpreter
        self._defeasible = None
        self._structure = None

    def __hash__(self) -> int:
        return hash(repr(self))

    def __repr__(self) -> str:
        explanation = ', '.join(repr(rule.head) for rule in reversed(self.rules)) if self.rules else '∅'
        symbol = '|~' if any(rule.type == RuleType.DEFEASIBLE for rule in self.rules) else '|-'
        derivable = self.rules[0].head

        return '%s %s %s' % (explanation, symbol, derivable)

    def get_structure(self) -> Structure:
        if self._structure is None:
            self._structure = Structure(self._get_defeasible(), self.rules[0].head, self)

        return self._structure

    def is_strict(self) -> bool:
        return not self._get_defeasible()

    def _get_defeasible(self) -> Set[Rule]:
        if self._defeasible is None:
            self._defeasible = {rule for rule in self.rules if rule.type == RuleType.DEFEASIBLE}

        return self._defeasible

    def union(self, derivation: 'Derivation') -> Optional['Derivation']:
        if type(derivation) is not Derivation or self.interpreter != derivation.interpreter:
            return None

        rules = [*self.rules]
        for rule in derivation.rules:
            if rule not in rules:
                rules.append(rule)

        return Derivation(rules, self.interpreter)


class Mark(Enum):
    UNDEFEATED = 0
    DEFEATED = 1


class DialecticalTree:
    @staticmethod
    def create(content: Structure) -> 'DialecticalTree':
        root = DialecticalTree(content)
        root.build()

        return root

    def __init__(self, content: Structure, parent: 'DialecticalTree' = None):
        self.content = content
        self.parent = parent
        self.children = set()
        if not self.parent or not self.parent.parent:
            self._concordance = dict()
            for rule in self.content.derivation.interpreter.sigma:
                self._concordance.setdefault(rule.head, set()).add(rule)
        else:
            self._concordance = {**self.parent.parent._concordance}
        for rule in self.content.argument:
            self._concordance.setdefault(rule.head, set()).add(rule)

    def __repr__(self) -> str:
        return self._describe()

    def _describe(self, indent: int = 0) -> str:
        content = '%s%s' % ('\t' * indent, self.content)
        for child in self.children:
            content += '\n' + child._describe(indent + 1)

        return content

    def build(self, mode: RuleType = RuleType.DEFEASIBLE):
        defeaters = self.content.get_defeaters(mode)
        for defeater in defeaters:
            if self.is_acceptable(defeater, mode):
                node = DialecticalTree(defeater, self)
                node.build(mode)
                self.children.add(node)

    def is_acceptable(self, defeater: Structure, mode: RuleType = RuleType.DEFEASIBLE) -> bool:
        if self.content.derivation.interpreter != defeater.derivation.interpreter:
            return False

        if not self._is_concordant(defeater):
            return False

        if self._is_subargument(defeater):
            return False

        return self._is_not_chain_or_defeated(defeater, mode)

    def _is_concordant(self, defeater: Structure) -> bool:
        return not self.parent or is_contradictory(self._concordance, defeater.argument)

    def _is_subargument(self, defeater: Structure) -> bool:
        if defeater.is_subargument_for(self.content):
            return True

        if not self.parent:
            return False

        return self.parent._is_subargument(defeater)

    def _is_not_chain_or_defeated(self, defeater: Structure, mode: RuleType = RuleType.DEFEASIBLE) -> bool:
        if not self.parent:
            return True

        if not self.content.is_blocking_defeater_for(self.parent.content, mode):
            return True

        return defeater.is_proper_defeater_for(self.content, mode)

    def mark(self) -> Mark:
        if not self.children:
            return Mark.UNDEFEATED

        for child in self.children:
            mark = child.mark()
            if mark == Mark.UNDEFEATED:
                return Mark.DEFEATED

        return Mark.UNDEFEATED


Warrant = Set[Rule]


class Answer(Enum):
    UNKNOWN = -1
    NO = 0
    YES = 1
    UNDECIDED = 2


class Interpreter:
    def __init__(self, program: Program):
        self.program = program
        self._cache = dict()
        self._index = dict()
        self._rules = dict()
        for rule in program.get_ground_program().rules:
            self._index.setdefault(RuleType.DEFEASIBLE, {}).setdefault(rule.head, set()).add(rule)
            if rule.type == RuleType.STRICT:
                self._index.setdefault(RuleType.STRICT, {}).setdefault(rule.head, set()).add(rule)
            self._rules.setdefault(rule.type, {}).setdefault(not rule.body, set()).add(rule)
        self._derivations = dict()
        self._strict = None

        self._sigma = None
        self._delta = None

    def get_heads(self, mode: RuleType = RuleType.DEFEASIBLE) -> Set[Literal]:
        return set(self._index.get(mode, {}).keys())

    @property
    def facts(self) -> Set[Rule]:
        return self._rules.get(RuleType.STRICT, {}).get(True, set())

    @property
    def stricts(self) -> Set[Rule]:
        return self._rules.get(RuleType.STRICT, {}).get(False, set())

    @property
    def presumptions(self) -> Set[Rule]:
        return self._rules.get(RuleType.DEFEASIBLE, {}).get(True, set())

    @property
    def defeasibles(self) -> Set[Rule]:
        return self._rules.get(RuleType.DEFEASIBLE, {}).get(False, set())

    @property
    def sigma(self) -> Set[Rule]:
        if self._sigma is None:
            self._sigma = {*self.stricts, *self.facts}

        return self._sigma

    @property
    def delta(self) -> Set[Rule]:
        if self._delta is None:
            self._delta = {*self.defeasibles, *self.presumptions}

        return self._delta

    def get_derivables(self, mode: RuleType = RuleType.DEFEASIBLE) -> Set[Literal]:
        for literal in self.get_heads(mode):
            self.get_derivations(literal, mode)

        return {literal for literal, derivations in self._derivations.get(mode, {}).items() if derivations}

    def _get_warrant(self, literal: Literal, mode: RuleType = RuleType.DEFEASIBLE) -> Optional[Warrant]:
        derivations = self.get_derivations(literal, mode)
        if not derivations:
            return None

        for derivation in derivations:
            structure = derivation.get_structure()
            tree = DialecticalTree.create(structure)
            print(tree)
            print()
            mark = tree.mark()
            if mark == Mark.UNDEFEATED:
                return structure.argument

        return None

    def get_derivations(self, literal: Literal, mode: RuleType = RuleType.DEFEASIBLE) -> Set[Derivation]:
        if not self._rules.get(RuleType.STRICT, {}).get(True, set()):  # no facts
            return set()

        if literal not in self._index.get(mode, {}):  # no expansions
            return set()

        if literal not in self._derivations.get(mode, {}):
            derivations = get_derivations(literal, self._index.get(mode, {}))
            if derivations:
                group = self._derivations.setdefault(mode, {}).setdefault(literal, set())
                for rules in derivations:
                    derivation = Derivation(rules, self)
                    group.add(derivation)

        return self._derivations.get(mode, {}).get(literal, set())

    def query(self, literal: Literal, mode: RuleType = RuleType.DEFEASIBLE) -> Tuple[Answer, Optional[Warrant]]:
        if literal in self._cache:
            return self._cache[literal]

        if literal not in self._index.get(mode, {}):
            self._cache[literal] = (Answer.UNKNOWN, None)
            return self._cache[literal]

        warrant = self._get_warrant(literal, mode)
        if warrant is not None:
            self._cache[literal] = (Answer.YES, warrant)
            return self._cache[literal]

        complement = literal.get_complement()
        warrant = self._get_warrant(complement, mode)
        if warrant is not None:
            self._cache[literal] = (Answer.NO, warrant)
            return self._cache[literal]

        self._cache[literal] = (Answer.UNDECIDED, None)
        return self._cache[literal]


Index = Dict[Literal, Set[Rule]]


def as_index(*rules: Rule, index: Index = None) -> Dict[Literal, Set[Rule]]:
    index = {**index} if index else dict()
    for rule in rules:
        index.setdefault(rule.head, set()).add(rule)

    return index


def disagree(literal1: Literal, literal2: Literal, rules: Set[Rule] = None) -> bool:
    index = as_index(*rules) if rules else dict()
    index = as_index(literal1.as_fact(), literal2.as_fact(), index=index)

    return is_contradictory(index)


def is_contradictory(index: Index, rules: Set[Rule] = None) -> bool:
    if rules:
        index = as_index(*rules, index=index)

    for literal in index:
        if get_derivations(literal, index):
            complement = literal.get_complement()
            if get_derivations(complement, index):
                return True

    return False


def get_derivations(literal: Literal, index: Index) -> List[List[Rule]]:
    if literal not in index:
        return []

    derivations = []
    for rule in index[literal]:
        partials = [[rule]]
        for body_literal in rule.body:
            completions = get_derivations(body_literal, index)
            if not completions:
                partials = None
                break

            temporary = []
            for partial in partials:
                for completion in completions:
                    derivation = [*partial]
                    for step in completion:
                        if step not in derivation:
                            derivation.append(step)
                    if derivation not in temporary:
                        temporary.append(derivation)
            partials = temporary
        if partials:
            for partial in partials:
                if partial not in derivations:
                    derivations.append(partial)

    return derivations


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
    print(p.get_ground_program())
    print('-' * 120)
    i = Interpreter(p)


    def query(literal: Literal):
        print('?- %s.' % literal)
        result, warrant = i.query(literal)
        print('%s.' % result.name)
        if warrant:
            for rule in warrant:
                print('\t%s' % rule)
        print()


    query(Literal.parse('penguin(tina)'))

    query(Literal.parse('bird(tina)'))

    query(Literal.parse('~bird(tina)'))

    query(Literal.parse('flies(tina)'))

    query(Literal.parse('~flies(tina)'))

    query(Literal.parse('flies(tweety)'))

    query(Literal.parse('~flies(tweety)'))

    query(Literal.parse('nests_in_trees(tina)'))

    query(Literal.parse('~nests_in_trees(tina)'))
