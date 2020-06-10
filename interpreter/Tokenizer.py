import ply.lex as lex

reserved = {
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'exit': 'EXIT',
    'assert': 'ASSERT',
    'return': 'RETURN',
    'if': 'IF',
    'elif': 'ELIF',
    'else': 'ELSE',
    'for': 'FOR',
    'while': 'WHILE',
    'repeat': 'REPEAT',
    'to': 'TO',
    'learn': 'LEARN',
    'and': 'AND',
    'or': 'OR',
    'not': 'NOT'
}

tokens = (
    'ID',
    'BREAK',
    'CONTINUE',
    'NUMBER',
    'BOOLEAN',
    'STRING',
    'REL_OP',
    'LP',
    'RP',
    'FUNCTION',
    'OB',
    'CB',
    'ASSIGN',
    'COMMA',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'NL',
    'EMPTY',
    'COMMENT',
    'LEARN',
    'IF',
    'ELIF',
    'ELSE',
    'WHILE',
    'REPEAT',
    'FOR',
    'TO',
    'OR',
    'AND',
    'NOT',
    'RETURN',

)


def t_FUNCTION(t):
    r"""[a-zA-Z][a-zA-Z0-9]*"""
    if t.value in reserved:
        t.type = reserved[t.value]
    return t


t_ID = r'\$[a-zA-Z0-9]+'


def t_NUMBER(t):
    r"""\d+(\.\d+)?"""
    t.value = int(t.value)
    return t


def t_BOOLEAN(t):
    r"""true|false"""
    if t.value == 'true':
        t.value = True
    else:
        t.value = False

    return t


def t_STRING(t):
    r"""".+\""""
    t.value = t.value[1:-1]
    return t


t_REL_OP = r'==|>=|<=|!=|>|<'
t_LP = r'\('
t_RP = r'\)'
t_OB = r'{'
t_CB = r'}'
t_ASSIGN = r'='
t_COMMA = r','
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_NL = r'[\n]+'


def t_COMMENT(_):
    r"""\#[^\n]+"""

    pass


def t_EMPTY(_):
    r"""[ \t\r]+"""

    pass


# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()
