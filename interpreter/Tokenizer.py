import ply.lex as lex

reserved = {
    'fw',
    'tl',
    'tr',
    'while',
    'if',
    'repeat'
}

tokens = (
    'KEYWORD',
    'ID',
    'NUMBER',
    'BOOLEAN',
    'STRING',
    'REL_OP',
    'LOGIC_OP',
    'LP',
    'RP',
    'LEARN',
    'FUNCTION',
    'OB',
    'CB',
    'ATTRIBUTION',
    'COMMA',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'NL',
    'EMPTY'
)


def t_KEYWORD(t):
    r'[a-z]+'
    if t in reserved:
        return t
    return None


t_ID = r'\$[a-zA-Z0-9]+'


def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = int(t.value)
    return t


def t_BOOLEAN(t):
    r'true|false'
    if t.value == 'true':
        t.value = True
    else:
        t.value = False

    return t


t_STRING = r'".+"'
t_REL_OP = r'==|>=|<=|!=|>|<'
t_LOGIC_OP = r'not|and|or'
t_LP = r'\('
t_RP = r'\)'
t_LEARN = r'learn'
t_FUNCTION = r'[a-zA-Z][a-zA-Z0-9]*'
t_OB = r'{'
t_CB = r'}'
t_ATTRIBUTION = r'='
t_COMMA = r','
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_NL = r'[\n]+'


def t_EMPTY(t):
    r'[ \t]+'

    pass


# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()
