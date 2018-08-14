from pybuilder.core import use_plugin, init, Author

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.install_dependencies")
use_plugin("python.flake8")
use_plugin("python.coverage")
use_plugin("python.distutils")
use_plugin("python.pycharm")

name = "defeasible"
version = "0.1.0"
author = "Stefano Bragaglia"
with open('LICENSE', 'r') as file:
    license = file.read()
url = "https://github.com/stefano-bragaglia/DefeasiblePython"
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
        # "__init__",
        # "defeasible",
        # "defeasible.dialectical",
        # "defeasible.domain",
        # "defeasible.domain.definitions",
        # "defeasible.domain.interpretation",
        # "defeasible.domain.rendering",
        # "defeasible.domain.rete",
        # "defeasible.domain.theme",
        # "defeasible.example",
        # "defeasible.language",
        # "defeasible.language.grammar",
        # "defeasible.language.visitor",
        # "defeasible.old_definitions",
    ])

    project.set_property("coverage_threshold_warn", 70)  # default is 70
    project.set_property("coverage_branch_threshold_warn", 70)  # default is 0
    project.set_property("coverage_branch_partial_threshold_warn", 70)  # default is 0

    project.set_property("dir_source_unittest_python", "src/test/python")
    project.set_property("unittest_module_glob", "tests_*")

    project.depends_on("assertpy")
    project.depends_on("coloredlogs")
    project.depends_on("verboselogs")
    project.depends_on_requirements("requirements.txt")
