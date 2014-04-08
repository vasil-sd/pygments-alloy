# Pygments Alloy

Lexer for the Alloy specification language developed by the Software
Design Group at MIT.

# Installation

    git clone http://github.com:sdg-mit/pygments-alloy.git
    cd pygments-alloy
    python setup.py install # might require sudo privileges


# Usage

Just specify *alloy* as the target language when using Pygments, e.g.,

    pygmentize -l alloy -f html -o model.als.html model.als

An Alloy style (color theme), again called *alloy*, is also provided, e.g.,

    pygmentize -S alloy -f html > alloy.css

# About Pygments

To see the supported languages, execute:

    pygmentize -L lexers

To see the supported styles, execute:

    pygmentize -L styles




