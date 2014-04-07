# -*- coding: utf-8 -*-
"""
    Red lexer
    ~~~~~~~~~~~

    * some fixes to RubyLexer --- class RedRubyLexer
    * lexer for Ruby + Red --- class RedLexer
    * some styles
"""
from pygments.lexers.web import HtmlLexer
from pygments.lexer import bygroups, DelegatingLexer
from pygments.lexers.agile import RubyLexer, RegexLexer
from pygments.lexers.templates import ErbLexer
from pygments.token import Token, Text, Keyword, Name, Comment, String, Error, Number, Operator, Generic, Literal, Punctuation

import sys
import collections


def _idx(t):   return (t[0] if t is not None else None)
def _token(t): return (t[1] if t is not None else None)
def _value(t): return (t[2] if t is not None else None)

"""
--------------------------------------------------------------------------------
  Common lexer class that implements lookahed and lookbehind buffers.
--------------------------------------------------------------------------------
"""
class MyLexerBase(RegexLexer):
    lookahead = 10
    lookbehind = 1
    queue = collections.deque()
    nows_queue = collections.deque()
    processed = collections.deque([], lookbehind)

    def peek_ahead(self, n):
        if len(self.nows_queue) >= n:
            return self.nows_queue[n-1]
        else:
            return (None, None, None)

    def next(self):
        return self.peek_ahead(1)

    def prev(self):
        if len(self.processed) > 0:
            return self.processed[-1]
        else:
            return (None, None, None)

    def process_one(self, curr):
        raise Exception('must override')

    def get_tokens_unprocessed(self, text):
        def __process(res):
            # print >> sys.stderr, "%s '%s'" % (res[1], res[2])
            if res is not None and _token(res) is not Token.Text:
                self.processed.append(res)
            return res

        for index, token, value in RegexLexer.get_tokens_unprocessed(self, text):
            self.queue.append((index, token, value))
            if token is not Token.Text:
                self.nows_queue.append((index, token, value))
            if len(self.nows_queue) < 1 + self.lookahead: continue
            curr = self.queue.popleft()
            if _token(curr) is not Token.Text:
                self.nows_queue.popleft()
            ans = __process(self.process_one(curr))
            if ans is not None:
                yield ans

        while (len(self.queue) > 0):
            curr = self.queue.popleft()
            if _token(curr) is not Token.Text:
                self.nows_queue.popleft()
            ans = __process(self.process_one(curr))
            if ans is not None: yield ans

"""
Alloy Lexer class.
"""
class AlloyLexer(MyLexerBase):
    name = 'Alloy'
    aliases = ['alloy']
    filenames = ['*.als'] # just to have one if you whant to use

    # SIG_KEYWORDS   = ['sig', 'abstract', 'enum']
    # OPS_KEYWORDS   = ['extends', 'set', 'seq', 'one', 'lone', 'no', 'all', 'some', 'sum', 'when', 'else', 'implies', 'not', 'iff', 'and', 'or', 'in', 'disj']
    # FUN_KEYWORDS =   ['fun', 'pred', 'assert', 'fact']
    # OTHER_KEYWORDS = ['none', 'iden', 'univ', 'let', 'open', 'module', 'check', 'run', 'for', 'but', 'exactly', 'Int', 'int']

    # EXTRA_KEYWORDS = SIG_KEYWORDS + OPS_KEYWORDS + FUN_KEYWORDS + OTHER_KEYWORDS

    iden_rex = r'[a-zA-Z_][a-zA-Z0-9_\']*'
    text_tuple = (r'[^\S\n]+', Text)

    tokens = {
        'sig': [
            (r'(extends)\b', Keyword, '#pop'),
            (iden_rex, Name.Class),
            text_tuple,
            (r',', Punctuation),
            (r'\{', Operator, '#pop'),
        ],
        'module': [
            text_tuple,
            (iden_rex, Name.Namespace, '#pop'),
        ],
        'fun': [
            text_tuple,
            (r'\{', Operator, '#pop'),
            (iden_rex, Name.Function, '#pop'),
        ],
        'root': [
            (r'--.*?$', Comment.Single),
            (r'//.*?$', Comment.Single),
            (r'/\*.*?\*/', Comment.Multiline),
            text_tuple,
            (r'"(\\\\|\\"|[^"])*"', String),
            (r'(module)(\s+)', bygroups(Keyword.Namespace, Text), 'module'),
            (r'(sig|enum)(\s+)', bygroups(Keyword.Declaration, Text), 'sig'),
            (r'(iden|univ|none)\b', Keyword.Constant),
            (r'(int|Int)\b', Keyword.Type),
            (r'(this|abstract|extends|set|seq|one|lone|let)\b', Keyword),
            (r'(all|some|no|sum|disj|when|else)\b', Keyword),
            (r'(run|check|for|but|exactly)\b', Keyword),
            (r'(and|or|implies|iff|in)\b', Operator.Word),
            (r'(fun|pred|fact|assert)(\s+)', bygroups(Keyword, Text), 'fun'),
            (r'!|#|&&|\+\+|<<|>>|>=|<=|<=>|\.|->', Operator), 
            (r'[-+/*%=<>&!^|~\{\}\[\]\(\)\.]', Operator),
            (iden_rex, Name),
            (r'[:,]', Punctuation),
            (r'[0-9]+', Number.Integer),
            (r'\n', Text),
        ]
    }

    def process_one(self, curr):
        return curr

############################################################################


from pygments.style import Style
from pygments.styles import get_style_by_name


class AlloyStyle(Style):
    default_style = ""

    styles = {}
    base = get_style_by_name("tango")
    for token in base.styles.keys():
        styles[token] = base.styles[token]

    # const_style = '#000000'

    # styles[Name.Constant] = const_style
    # styles[Name.Class] = 'bold ' + const_style
    # styles[Name.Namespace] = const_style

    styles[Keyword]  = '#1F1FA8 bold'
    styles[Comment]  = '#429E24 italic'
    styles[Operator] = '#000000 bold'
    styles[Literal]  = '#940000'


    styles[Keyword.Constant]    = styles[Keyword]
    styles[Keyword.Declaration] = styles[Keyword]
    styles[Keyword.Namespace]   = styles[Keyword]
    styles[Keyword.Pseudo]      = styles[Keyword]
    styles[Keyword.Reserved]    = styles[Keyword]
    styles[Keyword.Type]        = styles[Keyword]

    styles[Comment.Multiline] = styles[Comment]
    styles[Comment.Preproc]   = styles[Comment]
    styles[Comment.Single]    = styles[Comment]
    styles[Comment.Special]   = styles[Comment]
        
    styles[Literal.Number.Integer] = styles[Literal]
    styles[Literal.String]         = styles[Literal]

    styles[Operator.Word] = styles[Keyword]
