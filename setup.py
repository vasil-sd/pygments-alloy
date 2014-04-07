#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='pygments-alloy',
    version='0.1',
    description='Pygments lexer for Alloy.',
    keywords='pygments alloy lexer',
    license='MIT',

    author='Aleksandar Milicevic',
    author_email='aleks@csail.mit.edu',

    url='https://github.com/sdg-mit/pygments-alloy',

    packages=find_packages(),
    install_requires=['pygments >= 1.4'],

    entry_points='''[pygments.lexers]
                    alloy=src:AlloyLexer

                    [pygments.styles]
                    github=src:GithubStyle
                    alloy=src:AlloyStyle''',

    classifiers=[
    ],
)
