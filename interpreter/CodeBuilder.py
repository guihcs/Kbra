from interpreter.Parser import parser
from interpreter.Tokenizer import lexer

result_declarations = []
result_code = []
symbol_table = {}
current_symbol = [0]
current_line = [0]
building_function = False


def reset():
    global result_declarations
    result_declarations = []
    global result_code
    global symbol_table
    global current_symbol
    global current_line
    global building_function
    result_code = []
    symbol_table = {}
    current_symbol = [0]
    current_line = [0]
    building_function = False


def append_code(code):
    current_line[0] += 1
    result_code.append(code)


def replace_code(line, code):
    result_code[line] = code


def pop_code():
    current_line[0] -= 1
    return result_code.pop()


def get_current_line():
    return current_line[0]


def build_code(script):
    code = parser.parse(script, lexer=lexer)
    build_statements(code)
    res = result_code
    reset()
    return res


def build_statements(statements):
    for statement in statements:
        build_instruction(statement)


def build_instruction(instruction):
    function_map = {
        'LEARN': build_learn,
        'ASSIGN': build_assignment,
        'IF': build_if,
        'WHILE': build_while,
        'REPEAT': build_repeat,
        'FOR': build_for,
        'CALL': build_function_call
    }

    function_map[instruction[0]](*instruction[1:])


def build_learn(function, args, statements):
    pass


def build_assignment(address, expression):
    if address[1] not in symbol_table:
        symbol_table[address[1]] = current_symbol[0]
        current_symbol[0] += 1

    build_expression(expression)
    append_code(('POP', 'ID', address[1]))
    pass


def flat_tuple(t):
    res = []
    for up in t:
        if type(up[0]) is not tuple:
            res.append(up)
        else:
            for dp in flat_tuple(up):
                res.append(dp)

    return tuple(res)
    pass


def build_expression(expression):
    expression = flat_tuple(expression) if type(expression[0]) is tuple else (expression, )

    for term in expression:
        if term[0] == 'CONSTANT':
            append_code(('PUSH', 'CONSTANT', term[1]))
        elif term[0] == 'ID':
            append_code(('PUSH', 'ID', term[1]))
        elif term[0] == 'OP':
            append_code((term[1],))
    pass


def label(label):
    return f'#{label}-{get_current_line()}'


def build_if(condition, statements, chain):
    build_expression(condition)
    if_label = label('endif')

    append_code(('JUMPNOT', if_label))
    build_statements(statements)
    append_code(('LABEL', if_label))
    if chain:
        build_elif(chain[0][1], chain[0][2], chain[1], label('end-branch'))

    pass


def build_elif(condition, statements, chain, data):
    inject_jump_label(data)

    build_expression(condition)

    elif_label = label('endelif') if chain else data

    append_code(('JUMPNOT', elif_label))
    build_statements(statements)
    append_code(('LABEL', elif_label))

    if chain[0] == 'ELSE':
        build_else(chain[1], data)
        pass
    else:
        build_elif(chain[0][1], chain[0][2], chain[1], data)
        pass
    pass


def inject_jump_label(data):
    end_label = pop_code()
    append_code(('JUMP', data))
    append_code(end_label)


def build_else(statements, data):
    inject_jump_label(data)

    elif_label = data
    build_statements(statements)
    append_code(('LABEL', elif_label))
    pass


def build_while(condition, statements):
    start_label = label('loop-start')
    end_label = label('loop-end')
    append_code(('LABEL', start_label))
    build_expression(condition)
    append_code(('JUMPNOT', end_label))
    build_statements(statements)
    append_code(('JUMP', start_label))
    append_code(('LABEL', end_label))
    pass


def build_repeat(expression, statements):
    append_code(('PUSH', 'CONSTANT', 0))
    append_code(('POP', 'ID', '_ti'))
    build_expression(expression)
    append_code(('POP', 'ID', '_te'))
    start_repeat = label('start-repeat')
    end_repeat = label('end-repeat')

    append_code(('LABEL', start_repeat))
    append_code(('PUSH', 'ID', '_ti'))
    build_buffer_loop(end_repeat, start_repeat, statements)
    pass


def build_buffer_loop(end_repeat, start_repeat, statements):
    append_code(('PUSH', 'ID', '_te'))
    append_code(('LT',))
    append_code(('JUMPNOT', end_repeat))
    build_statements(statements)
    append_code(('JUMP', start_repeat))
    append_code(('LABEL', end_repeat))


def build_for(assign, expression, statements):
    build_assignment(assign[1], assign[2])
    build_expression(expression)
    append_code(('POP', 'ID', '_te'))
    start_repeat = label('start-repeat')
    end_repeat = label('end-repeat')

    append_code(('LABEL', start_repeat))
    append_code(('PUSH', 'ID', assign[1][1]))
    build_buffer_loop(end_repeat, start_repeat, statements)

    pass


def build_function_call(function, args):
    pass
