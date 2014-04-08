# Pygments Alloy

Lexer for the [Alloy](http://alloy.mit.edu) modeling language developed by the [Software Design Group](http://sdg.csail.mit.edu) at [MIT](http://mit.edu).

# Installation

```bash
git clone http://github.com:sdg-mit/pygments-alloy.git
cd pygments-alloy
python setup.py install # might require sudo privileges
```

# Usage

Just specify *alloy* as the target language when using Pygments, e.g.,

```bash
pygmentize -l alloy -f html -o model.als.html model.als
```

An Alloy style (color theme), again called *alloy*, is also provided, e.g.,

```bash
pygmentize -S alloy -f html > alloy.css
```

# About Pygments

To see the supported languages, execute:

```bash
pygmentize -L lexers
```

To see the supported styles, execute:

```bash
pygmentize -L styles
```



