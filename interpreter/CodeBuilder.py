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
    expression = flat_tuple(expression)

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
    if chain:
        if chain[0] == 'ELSE':
            end_label = pop_code()
            append_code(('JUMP', data))
            append_code(end_label)
            build_expression(condition)
            elif_label = label('endelif')
            append_code(('JUMPNOT', elif_label))
            build_statements(statements)
            append_code(('LABEL', elif_label))
            build_else(chain[1], data)
            pass
        else:
            end_label = pop_code()
            append_code(('JUMP', data))
            append_code(end_label)
            build_expression(condition)
            elif_label = label('endelif')
            append_code(('JUMPNOT', elif_label))
            build_statements(statements)
            append_code(('LABEL', elif_label))
            build_elif(chain[0][1], chain[0][2], chain[1], data)
            pass

    else:
        end_label = pop_code()
        append_code(('JUMP', data))
        append_code(end_label)
        build_expression(condition)
        elif_label = data
        append_code(('JUMPNOT', elif_label))
        build_statements(statements)
        append_code(('LABEL', elif_label))
    pass


def build_else(statements, data):
    end_label = pop_code()
    append_code(('JUMP', data))
    append_code(end_label)
    elif_label = data
    build_statements(statements)
    append_code(('LABEL', elif_label))
    pass


def build_while(condition, statements):
    pass


def build_repeat(expression, statements):
    pass


def build_for(assign, expression, statements):
    pass


def build_function_call(function, args):
    pass
