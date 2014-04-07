# Pygments Alloy

Lexer for the Alloy specification language developed by the Software
Design Group at MIT.

# Installation

## Using PyPI and pip 

(might need sudo privileges)

    pip install pygments-alloy


## Manual

(might need sudo privileges to run the last command)

    git clone http://github.com:sdg-mit/pygments-alloy.git
    cd pygments-alloy
    python setup.py install


# Usage

Just specify *alloy* as the target language when using Pygments, e.g.,

    pygmentize -l alloy -f html -o model.als.html model.als

To generate the style file for Alloy, type:

    pygmentize -S alloy -f html > alloy.css

# About Pygments

To see the supported languages, execute:

    pygmentize -L lexers

To see the supported styles, execute:

    pygmentize -L styles   


    

