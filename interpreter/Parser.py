import ply.yacc as yacc

# noinspection PyUnresolvedReferences
from interpreter.Tokenizer import tokens

stack_functions = {
    '+': 'ADD',
    '*': 'MULT',
    '-': 'SUB',
    '/': 'DIV',
    '>': 'GT',
    '<': 'LT',
    '<=': 'LE',
    '>=': 'GE',
    '==': 'EQ',
    '!=': 'NEQ'
}

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'REL_OP'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

scope_stack = [[]]


def append_code(code):
    scope_stack[-1].append(code)


def pushScope():
    scope_stack.append([])
    pass


def popScope():
    scope = scope_stack.pop()
    return scope
    pass


def p_start(p):
    """start : declarations"""
    global scope_stack
    p[0] = scope_stack[0]
    scope_stack = [[]]
    pass


def p_declarations(_):
    """declarations : NL declarations
                    | learn declarations
                    | statements declarations
                    | empty
    """

    pass


def p_statements(_):
    """statements : NL statements
                  | assignment declarations
                  | branching declarations
                  | loop declarations
                  | function declarations
                  | return declarations
    """


def p_learn(p):
    """learn : LEARN FUNCTION params scope OB statements CB post_scope"""
    append_code(('LEARN', p[2], p[3], p[8]))
    pass


def p_params(p):
    """params : params COMMA ID
              | ID
    """
    if len(p) < 3:
        p[0] = p[1]
    else:
        p[0] = (p[1], p[3])
    pass


def p_assignment(p):
    """assignment : assign"""
    append_code(p[1])
    pass


def p_assign(p):
    """assign : id ASSIGN logic"""
    p[0] = ('ASSIGN', p[1], p[3])


def p_branching(p):
    """branching : IF logic scope OB statements CB post_scope chain"""

    append_code(('IF', p[2], p[7], p[8]))


def p_scope(_):
    """scope : """
    pushScope()
    pass


def p_post_scope(p):
    """post_scope : """
    p[0] = popScope()
    pass


def p_chain(p):
    """chain : NL chain
             | elif chain
             | else
             | empty
    """
    if p[1] == '\n':
        p[0] = p[2]
    elif len(p) < 3:
        p[0] = p[1]
    else:
        p[0] = (p[1], p[2])
    pass


def p_elif(p):
    """elif : ELIF logic scope OB statements CB post_scope"""
    p[0] = ('ELIF', p[2], p[7])
    pass


def p_else(p):
    """else : ELSE scope OB statements CB post_scope"""
    p[0] = ('ELSE', p[6])
    pass


def p_loop(_):
    """loop : while
            | repeat
            | for
    """

    pass


def p_while(p):
    """while : WHILE expression scope OB statements CB post_scope"""
    append_code(('WHILE', p[2], p[7]))


def p_repeat(p):
    """repeat : REPEAT expression scope OB statements CB post_scope"""
    append_code(('REPEAT', p[2], p[7]))


def p_for(p):
    """for : FOR assign TO expression scope OB statements CB post_scope"""
    append_code(('FOR', p[2], p[4], p[9]))


def p_logic(p):
    """logic : logic OR logic
             | logic AND logic
             | expression
    """
    if len(p) < 3:
        p[0] = (p[1],)
    else:
        p[0] = (p[1], p[3], ('OP', p[2]))
    pass


def p_expression(p):
    """expression : expression REL_OP expression
                  | expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | paren
                  | constant
                  | id
                  | function
    """
    if len(p) < 3:
        p[0] = p[1]
    else:
        p[0] = (p[1], p[3], ('OP', stack_functions[p[2]]))
        pass
    pass


def p_paren(p):
    """paren : LP logic RP"""
    p[0] = p[2]
    pass


def p_constant(p):
    """constant : NUMBER
                | BOOLEAN
                | STRING
    """

    p[0] = ('CONSTANT', p[1])


def p_id(p):
    """id : ID"""
    p[0] = ('ID', p[1])


def p_function(p):
    """function : FUNCTION LP args RP"""

    append_code(('CALL', p[1], p[3]))


def p_args(p):
    """args : args COMMA logic
            | logic
    """

    if len(p) < 3:
        p[0] = p[1]
    else:
        p[0] = (p[1], p[3])
    pass


def p_return(p):
    """return : RETURN logic"""
    append_code(('RET', p[2]))
    pass


def p_empty(_):
    """empty : """

    pass


def p_error(t):
    print("Syntax error at '%s'" % t.value)


parser = yacc.yacc()
