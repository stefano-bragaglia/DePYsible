from enum import Enum
from typing import Dict, Iterable, List, Optional, Set, Tuple

from dataclasses import dataclass, field

from defeasible.domain.definitions import Literal, Program, Rule, RuleType


@dataclass(init=True, repr=False, eq=True, order=True)
class Structure:
    argument: Set[Rule]
    conclusion: Literal
    derivation: 'Derivation'

    def __hash__(self) -> int:
        return hash(repr(self))

    def __repr__(self) -> str:
        if not self.argument:
            return '<∅, %s>' % repr(self.conclusion)

        try:
            result = '<{%s}, %s>' % (' ; '.join(repr(rule) for rule in self.argument), repr(self.conclusion))
        except Exception as e:
            print(e)
        else:
            return result

    def is_counter_argument_of(self, structure: 'Structure', disagreement: 'Structure') -> bool:
        if self.derivation.interpreter != structure.derivation.interpreter \
                or self.derivation.interpreter != disagreement.derivation.interpreter:
            raise Exception('From different interpreters')

        if self.is_strict() or structure.is_strict():
            return False

        return \
            disagreement.is_subargument_of(structure) \
            and disagree(disagreement.conclusion, self.conclusion, self.derivation.interpreter.program.rules)

    def is_equi_specific_to(self, structure: 'Structure') -> bool:
        if self.derivation.interpreter != structure.derivation.interpreter:
            raise Exception('From different interpreters')

        if self.argument != structure.argument:
            return False

        if not self.argument:
            return True

        index = as_index({
            self.conclusion.as_fact(),
            *self.derivation.interpreter.program.rules,
        }, RuleType.STRICT)
        if not get_derivations(structure.conclusion, index):
            return False

        index = as_index({
            structure.conclusion.as_fact(),
            *self.derivation.interpreter.program.rules,
        }, RuleType.STRICT)
        return bool(get_derivations(self.conclusion, index))

    def is_more_salient_than(self, structure: 'Structure') -> bool:
        more_salient = False
        for rule1 in self.argument:
            for rule2 in structure.argument:
                if not (rule1.salience < rule2.salience):
                    return False

                more_salient |= rule1.salience > rule2.salience

        return more_salient

    def is_preferable_to(self, structure: 'Structure') -> bool:
        if self.is_equi_specific_to(structure):
            return self.is_more_salient_than(structure)

        return self.is_strictly_more_specific_than(structure)

    def is_proper_defeater_for(self, structure: 'Structure', disagreement: 'Structure') -> bool:
        if self.derivation.interpreter != structure.derivation.interpreter \
                or self.derivation.interpreter != disagreement.derivation.interpreter:
            raise Exception('From different interpreters')

        return \
            disagreement.is_subargument_of(structure) \
            and self.is_counter_argument_of(structure, disagreement) \
            and self.is_preferable_to(disagreement)

    def is_blocking_defeater_for(self, structure: 'Structure', disagreement: 'Structure') -> bool:
        if self.derivation.interpreter != structure.derivation.interpreter \
                or self.derivation.interpreter != disagreement.derivation.interpreter:
            raise Exception('From different interpreters')

        return \
            disagreement.is_subargument_of(structure) \
            and self.is_counter_argument_of(structure, disagreement) \
            and not self.is_preferable_to(disagreement) \
            and not disagreement.is_preferable_to(self)

    def is_defeater_for(self, structure: 'Structure', disagreement: 'Structure') -> bool:
        if self.derivation.interpreter != structure.derivation.interpreter \
                or self.derivation.interpreter != disagreement.derivation.interpreter:
            raise Exception('From different interpreters')

        return \
            self.is_proper_defeater_for(structure, disagreement) \
            or self.is_blocking_defeater_for(structure, disagreement)

    def is_strict(self) -> bool:
        return not self.argument

    def is_strictly_more_specific_than(self, structure: 'Structure') -> bool:
        if self.derivation.interpreter != structure.derivation.interpreter:
            raise Exception('From different interpreters')

        derivables, rules = set(), set()
        for rule in self.derivation.interpreter.program.rules:
            if self.derivation.interpreter.get_derivations(rule.head, RuleType.DEFEASIBLE):
                derivables.add(rule.head)
            if rule.type == RuleType.STRICT and rule.body:
                rules.add(rule)

        more_specific = False
        for derivable in derivables:
            sigma = as_index({*rules, derivable.as_fact()}, RuleType.STRICT)
            delta1 = as_index({*rules, derivable.as_fact(), *self.argument}, RuleType.DEFEASIBLE)
            delta2 = as_index({*rules, derivable.as_fact(), *structure.argument}, RuleType.DEFEASIBLE)

            def_conclusion = bool(get_derivations(self.conclusion, delta1))
            str_conclusion = bool(get_derivations(self.conclusion, sigma))
            def_structure = bool(get_derivations(structure.conclusion, delta2))
            str_structure = bool(get_derivations(structure.conclusion, sigma))

            more_specific |= def_structure and not str_structure and not def_conclusion
            if not def_conclusion or not (not str_conclusion):
                continue

            if not def_structure:
                return False

        return more_specific

    def is_subargument_of(self, structure: 'Structure') -> bool:
        if self.derivation.interpreter != structure.derivation.interpreter:
            raise Exception('From different interpreters')

        for rule in self.argument:
            if rule not in structure.argument:
                return False

        return True


@dataclass(init=True, repr=False, eq=True, order=True)
class Derivation:
    rules: List[Rule]
    interpreter: 'Interpreter'

    def __hash__(self) -> int:
        return hash(repr(self))

    def __repr__(self) -> str:
        explanation = ', '.join(repr(rule.head) for rule in reversed(self.rules)) if self.rules else '∅'
        symbol = '|~' if any(rule.type == RuleType.DEFEASIBLE for rule in self.rules) else '|-'
        derivable = self.rules[0].head

        return '%s %s %s' % (explanation, symbol, derivable)

    def get_structure(self) -> Structure:
        return Structure({rule for rule in self.rules if rule.type == RuleType.DEFEASIBLE}, self.rules[0].head, self)


class DefeaterType(Enum):
    PROPER = 0
    BLOCKING = 1


Summary = Dict[Structure, Dict[DefeaterType, Dict[Structure, Structure]]]


class Mark(Enum):
    UNDEFEATED = 0
    DEFEATED = 1


@dataclass(init=False, repr=False, eq=True, order=True)
class DialecticalTree:
    content: Structure
    disagreement: Structure = None
    parent: 'DialecticalTree' = None
    children: Set['DialecticalTree'] = field(default_factory=set)

    @staticmethod
    def create(structure: Structure, defeaters: Summary) -> 'DialecticalTree':
        root = DialecticalTree(structure)
        root.build(defeaters)

        return root

    def __init__(
            self,
            defeater: Structure,
            disagreement: Structure = None,
            type: DefeaterType = None,
            parent: 'DialecticalTree' = None,
    ):
        self.content = defeater
        self.disagreement = disagreement
        self.type = type
        self.parent = parent
        self.children = set()
        if not self.parent or not self.parent.parent:
            self._concordance = as_index(self.content.derivation.interpreter.program.rules, RuleType.STRICT)
        else:
            self._concordance = {**self.parent.parent._concordance}
        for rule in self.content.argument:
            self._concordance.setdefault(rule.head, set()).add(rule)

    def __hash__(self) -> int:
        return hash(repr(self))

    def __repr__(self) -> str:
        content = '%s [%s]' % (self.content, self.disagreement or '')
        for child in self.children:
            for line in repr(child).split('\n'):
                content += '\n\t%s' % line

        return content

    def build(self, defeaters: Summary):
        for type in defeaters.get(self.content, {}):
            for defeater, disagreement in defeaters.get(self.content, {}).get(type, {}).items():
                if self.is_acceptable(defeater, disagreement):
                    node = DialecticalTree(defeater, disagreement, type, self)
                    node.build(defeaters)
                    self.children.add(node)

    def is_acceptable(self, defeater: Structure, disagreement: Structure) -> bool:
        if self.content.derivation.interpreter != defeater.derivation.interpreter:
            raise Exception('From different interpreters')

        return \
            not self._is_already_used(defeater) \
            and not self._is_subargument(defeater) \
            and self._is_not_chain_or_defeated(defeater, disagreement)
        # and self._is_concordant(defeater)  # \

    def _is_already_used(self, defeater: Structure) -> bool:
        if defeater == self.content:
            return True

        if not self.parent:
            return False

        return self.parent._is_already_used(defeater)

    def _is_subargument(self, defeater: Structure) -> bool:
        if defeater.is_subargument_of(self.content):
            return True

        if not self.parent:
            return False

        return self.parent._is_subargument(defeater)

    def _is_concordant(self, defeater: Structure) -> bool:
        if not self.parent:
            return True

        rules = {*self.content.derivation.interpreter.program.rules, *defeater.argument}
        current = self.parent
        while current:
            rules.update(current.content.argument)
            if current.parent and current.parent.parent:
                current = current.parent.parent

        index = as_index(rules)
        return is_contradictory(index)

    def _is_not_chain_or_defeated(self, defeater: Structure, disagreement: Structure) -> bool:
        if not self.parent:
            return True

        if not self.content.is_blocking_defeater_for(self.parent.content, self.disagreement):
            return True

        return defeater.is_proper_defeater_for(self.content, disagreement)

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


@dataclass(init=False, repr=False, eq=True, order=True)
class Interpreter:
    program: Program

    def __init__(self, program: Program):
        self.program = program.get_ground_program()
        self._defeaters = None
        self._literals = None
        self._structures = None
        self._answers = None

    def __repr__(self) -> str:
        return repr(self.program)

    def get_defeaters(self) -> Summary:
        if self._defeaters is None:
            arguments = self.get_structures(RuleType.DEFEASIBLE)

            subarguments = {}
            for argument in arguments:
                for subargument in arguments:
                    if subargument.is_subargument_of(argument):
                        subarguments.setdefault(argument, set()).add(subargument)

            counter_arguments = {}
            for counter_argument in arguments:
                for argument in arguments:
                    if counter_argument != argument:
                        for subargument in subarguments.get(argument, set()):
                            if counter_argument.is_counter_argument_of(argument, subargument):
                                counter_arguments.setdefault(argument, {})[counter_argument] = subargument

            self._defeaters = {}
            for argument in counter_arguments:
                for counter_argument, disagreement in counter_arguments[argument].items():
                    if counter_argument.is_preferable_to(disagreement):
                        self._defeaters \
                            .setdefault(argument, {}) \
                            .setdefault(DefeaterType.PROPER, {}) \
                            .setdefault(counter_argument, disagreement)
                    elif not disagreement.is_preferable_to(counter_argument):
                        self._defeaters \
                            .setdefault(argument, {}) \
                            .setdefault(DefeaterType.BLOCKING, {}) \
                            .setdefault(counter_argument, disagreement)

        return self._defeaters

    def get_derivations(self, literal: Literal, mode: RuleType = RuleType.DEFEASIBLE) -> Set[Derivation]:
        if not self.program.get_facts():
            return set()

        index = as_index(self.program.rules, mode)
        if literal not in index:
            return set()

        return {Derivation(rules, self) for rules in get_derivations(literal, index)}

    def get_literals(self, mode: RuleType = RuleType.DEFEASIBLE) -> Set[Literal]:
        if self._literals is None:
            self._literals = {rule.head for rule in self.program.rules if rule.type.value <= mode.value}

        return self._literals

    def get_structures(self, mode: RuleType = RuleType.DEFEASIBLE) -> Set[Structure]:
        if self._structures is None:
            self._structures = {}

        if mode not in self._structures:
            structures = self._structures.setdefault(mode, set())
            literals = self.get_literals(mode)
            for literal in literals:
                derivations = self.get_derivations(literal, mode)
                for derivation in derivations:
                    structure = derivation.get_structure()
                    structures.add(structure)

        return self._structures.get(mode, set())

    def is_contradictory(self, mode: RuleType = RuleType.DEFEASIBLE) -> bool:
        index = as_index(self.program.rules, mode)

        return is_contradictory(index)

    def query(self, literal: Literal, mode: RuleType = RuleType.DEFEASIBLE) -> Tuple[Answer, Optional[Warrant]]:
        if self._answers is None:
            self._answers = {}

        answers = self._answers.setdefault(mode, {})
        if literal not in answers:
            if literal not in self.get_literals(mode):
                answers.setdefault(literal, (Answer.UNKNOWN, None))
            else:
                warrant = self._get_warrant(literal, mode)
                if warrant is not None:
                    answers.setdefault(literal, (Answer.YES, warrant))
                else:
                    complement = literal.get_complement()
                    warrant = self._get_warrant(complement, mode)
                    if warrant is not None:
                        answers.setdefault(literal, (Answer.NO, warrant))
                    else:
                        answers.setdefault(literal, (Answer.UNDECIDED, None))

        return self._answers.get(mode, {}).get(literal, (Answer.UNKNOWN, None))

    def _get_warrant(self, literal: Literal, mode: RuleType = RuleType.DEFEASIBLE) -> Optional[Warrant]:
        derivations = self.get_derivations(literal, mode)
        if not derivations:
            return None

        defeaters = self.get_defeaters()
        for derivation in derivations:
            structure = derivation.get_structure()
            tree = DialecticalTree.create(structure, defeaters)
            mark = tree.mark()
            if mark == Mark.UNDEFEATED:
                return structure.argument

        return None


Index = Dict[Literal, Set[Rule]]


def disagree(literal1: Literal, literal2: Literal, rules: Iterable[Rule]) -> bool:
    if literal1.get_complement() == literal2:
        return True

    index = as_index(rules, RuleType.STRICT)
    index.setdefault(literal1, set()).add(literal1.as_fact())
    index.setdefault(literal2, set()).add(literal2.as_fact())

    return is_contradictory(index)


def as_index(rules: Iterable[Rule], mode: RuleType = RuleType.DEFEASIBLE) -> Index:
    index = {}
    for rule in rules:
        if rule.type.value <= mode.value:
            index.setdefault(rule.head, set()).add(rule)

    return index


def is_contradictory(index: Index) -> bool:
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


# Summary = Dict[Structure, Dict[DefeaterType, Dict[Structure, Structure]]]


def recurse(argument: Structure, summary: Summary):
    print(argument)
    _recurse(argument, summary, 0)


def _recurse(argument: Structure, summary: Summary, indent: int = 0):
    for type in DefeaterType:
        for defeater, disagreement in summary.get(argument, {}).get(type, {}).items():
            print('\t' * indent, defeater, '[', disagreement, ']')
            _recurse(defeater, summary, indent + 1)
