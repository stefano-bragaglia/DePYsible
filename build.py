import os

from pybuilder.core import init, use_plugin

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.install_dependencies")
use_plugin("python.flake8")
use_plugin("python.coverage")
use_plugin("python.distutils")
use_plugin("python.pycharm")

name = "DePYsible"
version = "0.1.0"
summary = "depysible Logic and Argumentation Theory on First Order Logic in pure Python"
description = """
___DePYsible___ is a Python implementation of [depysible Logic](https://en.wikipedia.org/wiki/depysible_logic) for [argumentation](https://en.wikipedia.org/wiki/Argumentation_theory).
In particular, _depysible Logic_ is a non-monotonic logic proposed to formalize depysible reasoning and argumentation.

In a nutshell, _depysible Logic_ supports three types of propositions:

* __strict rules__: to specify known facts or information that is always a consequence of other sure facts,
* __depysible rules__: to specify information that is typically or possibly a consequence of other information,
* __undercutting defeaters__: to specify exceptions to depysible rules.

Some approaches like the one used in [this implementation](http://cs.uns.edu.ar/~ajg/papers/2004TPLPGarciaSimari.pdf), the _undercutting defeaters_ are derived by identifying the defeating __arguments__ among conflicting ones.
(An _argument_ relates to a fact called __conclusion__ and includes the list of depysible rules that have to be true to make the _conclusion_ to hold.)

A priority ordering over the _depysible rules_ and the _defeaters_ can be given or inferred by the __generalised specificity__ of the arguments. 
Intuitively, this comparison criterion favours two aspects: it prefers arguments (1) with greater information content or (2) with less use of rules (more direct).
In other words, given two conflicting arguments, the defeater is the more precise or more concise among them. 
Arguments that have the same generalised specificity can be ordered by means of user-specified priorities on the rules. 

During the process of deduction, the strict rules are always applied, while a depysible rule can be applied only if no defeater of a higher priority specifies that it should not.
This process decides if each depysible fact is _true_, _false_ or _undecided_ and provides the clues supporting these decisions.

    % Strict rules
    bird(X) <- chicken(X).
    bird(X) <- penguin(X).
    ~flies(X) <- penguin(X).
    
    % Facts
    chicken(tina).
    penguin(tweety).
    scared(tina).
    
    % depysible knowledge
    flies(X) -< bird(X).
    flies(X) -< chicken(X), scared(X).
    ~flies(X) -< chicken(X).
    nests_in_trees(X) -< flies(X).

    ?- derive ~flies(tweety)
        penguin(tweety), ~flies(tweety)  |-  ~flies(tweety)
    
    ?- argue ~flies(tina)
        <{~flies(tina) -< chicken(tina).}, ~flies(tina)>
        
    ?- ~flies(tweety)
    YES
    
    ? ~flies(tina)
    NO
        flies(tina) -< chicken(tina), scared(tina).
    
    ?- nests_in_trees(tweety)
    UNDECIDED
    
    ?- ~nests_in_trees(tina)
    UNKNOWN

See [github.com/stefano-bragaglia/DePYsible.git](https://github.com/stefano-bragaglia/DePYsiblePython.git) for more details.
"""
author = "Stefano Bragaglia"
with open(os.path.join(os.path.dirname(__file__), 'LICENSE'), 'r') as file:
    license = file.read()
url = "https://github.com/stefano-bragaglia/depysiblePython"
default_task = ["clean", "analyze", "publish"]


@init
def set_properties(project):
    project.set_property("flake8_break_build", True)  # default is False
    project.set_property("flake8_verbose_output", True)  # default is False
    project.set_property("flake8_radon_max", 10)  # default is None
    project.set_property_if_unset("flake8_max_complexity", 10)  # default is None
    # Complexity: <= 10 is easy, <= 20 is complex, <= 50 great difficulty, > 50 unmaintainable

    project.set_property("coverage_break_build", True)  # default is False
    project.set_property("coverage_verbose_output", True)  # default is False
    project.set_property("coverage_allow_non_imported_modules", False)  # default is True
    project.set_property("coverage_exceptions", [
        "__init__",
        "depysible",
        # "depysible.domain",
        "depysible.domain.definitions",
        # "depysible.domain.interpretation",
        "depysible.domain.rendering",
        # "depysible.domain.rete",
        "depysible.domain.theme",
        # "depysible.language",
        # "depysible.language.grammar",
        # "depysible.language.visitor",
    ])

    project.set_property("coverage_threshold_warn", 35)  # default is 70
    project.set_property("coverage_branch_threshold_warn", 35)  # default is 0
    project.set_property("coverage_branch_partial_threshold_warn", 35)  # default is 0

    project.set_property("dir_source_unittest_python", "src/test/python")
    project.set_property("unittest_module_glob", "tests_*")

    project.depends_on("assertpy")
    project.depends_on("coloredlogs")
    project.depends_on("verboselogs")
    project.depends_on_requirements("requirements.txt")
