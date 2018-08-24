# DefeasiblePython
[![GitHub tag](https://img.shields.io/github/tag/stefano-bragaglia/DefeasiblePython.svg)](https://github.com/stefano-bragaglia/DefeasiblePython/tags)

[![Contributors](https://img.shields.io/github/contributors/stefano-bragaglia/DefeasiblePython.svg)](https://github.com/stefano-bragaglia/DefeasiblePython/graphs/contributors)
[![GitHub last commit (branch)](https://img.shields.io/github/last-commit/stefano-bragaglia/DefeasiblePython/master.svg)](https://github.com/stefano-bragaglia/DefeasiblePython)
[![license](https://img.shields.io/github/license/stefano-bragaglia/DefeasiblePython.svg)](https://github.com/stefano-bragaglia/DefeasiblePython/blob/master/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/stefano-bragaglia/DefeasiblePython.svg)](https://github.com/stefano-bragaglia/DefeasiblePython/issues)
[![GitHub closed issues](https://img.shields.io/github/issues-closed/stefano-bragaglia/DefeasiblePython.svg)](https://github.com/stefano-bragaglia/DefeasiblePython/issues?q=is%3Aissue+is%3Aclosed)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/stefano-bragaglia/DefeasiblePython.svg)](https://github.com/stefano-bragaglia/DefeasiblePython/pulls)
[![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed/stefano-bragaglia/DefeasiblePython.svg)](https://github.com/stefano-bragaglia/DefeasiblePython/pulls?q=is%3Apr+is%3Aclosed)

An implementation of Defeasible Logic in Python

[//]: # "## Contributing"

[//]: # "Bug reports and pull requests are welcome on GitHub at [twitterz.api](https://github.com/stefano-bragaglia/DefeasiblePython) repository."
[//]: # "This project is intended to be a safe, welcoming space for collaboration, and contributors are expected to adhere to the" 
[//]: # "[Contributor Covenant](http://contributor-covenant.org) code of conduct."

### Grammar

    program      ::= rule* 'EOF'
    rule         ::= defeasible | strict 
    defeasible   ::= literal '-<' literals? salience? '.'
    strict       ::= literal ( '<-' literals? )? salience? '.'
    literals     ::= literal ( ',' literal )*
    literal      ::= negation? atom
    negation     ::= '~'+
    atom         ::= functor ( '(' terms? ')' )?
    functor      ::= DOUBLE_QUOTE | SINGLE_QUOTE | IDENTIFIER
    terms        ::= term ( ',' term )*
    term         ::= boolean | number | string | IDENTIFIER | VARIABLE
    boolean      ::= TRUE | FALSE
    number       ::= REAL | INTEGER
    string       ::= DOUBLE_QUOTE | SINGLE_QUOTE
    salience     ::= '@' INTEGER

    TRUE         ::= [Tt] [Rr] [Uu] [Ee]
    FALSE        ::= [Ff] [Aa] [Ll] [Ss] [Ee]
    REAL         ::= '-'? [0-9]* '.' [0-9]+ ('E' '-'? [0-9]+)?
    INTEGER      ::= '-'? [0-9]+
    DOUBLE_QUOTE ::= '"' [^"]* '"'
    SINGLE_QUOTE ::= "'" [^']* "'"
    IDENTIFIER   ::= [a-z][a-z_A-Z0-9]*
    VARIABLE     ::= [_A-Z][a-z_A-Z0-9]*
    COMMENT      ::= '%' .* 'EOL'


#### program
![program](src/resources/images/program.png)

    program  ::= rule* 'EOF'

no references

#### rule
![rule](src/resources/images/rule.png)

    rule     ::= defeasible
               | strict

referenced by:
* [program](#program)

#### defeasible
![defeasible](src/resources/images/defeasible.png)

    defeasible
             ::= literal '-<' literals? salience? '.'

referenced by:
* [rule](#rule)

#### strict
![strict](src/resources/images/strict.png)

    strict   ::= literal ( '<-' literals? )? salience? '.'

referenced by:
* [rule](#rule)

#### literals
![literals](src/resources/images/literals.png)

    literals ::= literal ( ',' literal )*

referenced by:
* [defeasible](#defeasible)
* [strict](#strict)

#### literal
![literal](src/resources/images/literal.png)

    literal  ::= negation? atom

referenced by:
* [defeasible](#defeasible)
* [literals](#literals)
* [strict](#strict)

#### negation
![negation](src/resources/images/negation.png)

    negation ::= '~'+

referenced by:
* [literal](#literal)

#### atom
![atom](src/resources/images/atom.png)

    atom     ::= functor ( '(' terms? ')' )?

referenced by:
* [literal](#literal)

#### functor
![functor](src/resources/images/functor.png)

    functor  ::= DOUBLE_QUOTE
               | SINGLE_QUOTE
               | IDENTIFIER

referenced by:
* [atom](#atom)

#### terms
![terms](src/resources/images/terms.png)

    terms    ::= term ( ',' term )*

referenced by:
* [atom](#atom)

#### term
![term](src/resources/images/term.png)

    term     ::= boolean
               | number
               | string
               | IDENTIFIER
               | VARIABLE

referenced by:
* [terms](#terms)

#### boolean
![boolean](src/resources/images/boolean.png)

    boolean  ::= TRUE
               | FALSE

referenced by:
* [term](#term)

#### number
![number](src/resources/images/number.png)

    number   ::= REAL
               | INTEGER

referenced by:
* [term](#term)

#### string
![string](src/resources/images/string.png)

    string   ::= DOUBLE_QUOTE
               | SINGLE_QUOTE

referenced by:
* [term](#term)



### Future Works

Include _presumptions_, _negation_as_failure_ (standard negation) and _concordance_ check.

### License

The project is covered by the [Simplified BSD license](https://opensource.org/licenses/BSD-2-Clause). 
