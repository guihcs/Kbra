from interpreter.Tokenizer import tokens
import ply.yacc as yacc

code = []

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)


def p_start(p):
    """start : NL start
             | statement start
             | learn start
             | empty

    """
    if (not p[1] is None) and (not p[1] == '\n'):
        code.append(p[1])
    p[0] = code

def p_empty(p):
    'empty : '
    pass


def p_learn(p):
    """learn : LEARN"""
    pass


def p_statement(p):
    """statement : KEYWORD expression OB statement CB NL
                 | ID ATTRIBUTION expression NL
    """

    if len(p) < 6:
        p[0] = (p[2], p[1], p[3])
    else:

        pass



def p_args(p):
    """args : expression
            | args COMMA expression
    """


def p_expression(p):
    """expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | LP expression RP
                  | constant
    """
    if len(p) < 3:
        p[0] = p[1]
    else:
        p[0] = (p[1], p[3], p[2])


def p_constant(p):
    """constant : ID
                | NUMBER
    """
    p[0] = p[1]


def p_error(t):
    print("Syntax error at '%s'" % t.value)


parser = yacc.yacc()
