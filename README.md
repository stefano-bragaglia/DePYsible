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

    program      = rule* eof
    rule         = defeasible | strict ;
    defeasible   = literal '-<' literals? salience? '.'
    strict       = literal ( '<-' literals? )? salience? '.'
    literals     = literal ( ',' literal )*
    literal      = negation? atom
    negation     = '~'+
    atom         = functor ( '(' terms? ')' )?
    functor      = double_quote | single_quote | identifier
    terms        = term ( ',' term )*
    term         = boolean | number | string | identifier | variable
    boolean      = 'TRUE' | 'FALSE'
    number       = real | integer
    string       = double_quote | single_quote
    
    comment      = ?RegEx(%.*)?
    real         = ?RegEx(-?\d*\.\d+(E-?\d+)?)?
    integer      = ?RegEx(-?\d+)?
    double_quote = ?RegEx("[^"]*")? 
    single_quote = ?RegEx('[^']*')?
    identifier   = ?RegEx([a-z][a-zA-Z_0-9]*)?
    variable     = ?RegEx([_A-Z][a-zA-Z_0-9]*)?

### License

The project is covered by the [Simplified BSD license](https://opensource.org/licenses/BSD-2-Clause). 
