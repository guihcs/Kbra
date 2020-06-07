from interpreter.Tokenizer import tokens
import ply.yacc as yacc

scope_stack = [[]]
current_index = [0]
def p_start(p):
    """start : statements"""
    p[0] = scope_stack[0]
    pass


def p_statements(p):
    """statements : NL statements
                  | ID ASSIGN expression statements
                  | KEYWORD expression scope OB statements CB post_scope statements
                  | expression statements
                  | empty
    """
    if len(p) < 3 or '\n' in p[1]:
        return

    # function call
    if len(p) < 5:
        scope_stack[current_index[0]].insert(0, (p[1]))
        pass
    # assign
    elif len(p) < 8:
        scope_stack[current_index[0]].insert(0, ('ASSIGN', ('ID', p[1]), p[3]))
        pass
    # branching
    else:
        scope_stack[current_index[0]].insert(0, ('BRANCH', p[1], p[2], p[7]))
        pass

    pass


def p_scope(p):
    'scope : '
    current_index[0] += 1
    scope_stack.append([])
    pass


def p_post_scope(p):
    'post_scope : '
    current_index[0] -= 1
    p[0] = scope_stack[current_index[0] + 1]
    scope_stack.pop()
    pass


def p_expression(p):
    """expression : expression REL_OP expression
                  | expression PLUS expression
                  | constant
                  | id
                  | function
    """

    if len(p) < 3:
        p[0] = p[1]
    else:
        p[0] = (p[1], p[3], ('OPERATOR', p[2]))
    pass


def p_constant(p):
    """constant : NUMBER
    """

    p[0] = ('CONSTANT', p[1])


def p_id(p):
    'id : ID'
    p[0] = ('ID', p[1])


def p_function(p):
    'function : FUNCTION LP args RP'
    p[0] = ('FUNCTION', p[1], p[3])


def p_args(p):
    """args : args COMMA expression
            | expression
    """

    if len(p) < 3:
        p[0] = (p[1], )
    else:
        p[0] = (p[1], p[3])
        pass
    pass


def p_empty(p):
    'empty : '

    pass


def p_error(t):
    print("Syntax error at '%s'" % t.value)


parser = yacc.yacc()
