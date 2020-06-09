from interpreter.Parser import parser
from interpreter.Tokenizer import lexer

result_declarations = []
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


def get_current_line():
    return current_line[0]


def build_code(script):
    code = parser.parse(script, lexer=lexer)

    build_statements(code)
    print(symbol_table)
    return result_code


def build_statements(statements):
    for statement in statements:
        build_instruction(statement)


def build_instruction(instruction):
    function_map = {
        'LEARN': build_learn,
        'ASSIGN': build_assignment,
        'BRANCH': build_branch,
        'LOOP': build_loop,
        'FUNCTION': build_function_call
    }

    function_map[instruction[0]](*instruction[1:])


def build_learn():
    pass


def build_assignment(address, expression):
    if address[1] not in symbol_table:
        symbol_table[address[1]] = current_symbol[0]
        current_symbol[0] += 1

    symbol_address = symbol_table[address[1]]
    build_expression(expression)
    append_code(('POP', 'ID', symbol_address))
    pass


def build_expression(expression):

    for term in expression:

        if term[0] == 'CONSTANT':
            append_code(('PUSH', 'CONSTANT', term[1]))
        elif term[0] == 'ID':
            append_code(('PUSH', 'ID', symbol_table[term[1]]))
        elif term[0] == 'OP':
            append_code((term[1],))
    pass


def build_branch():
    pass


def build_loop():
    pass


def build_function_call():
    pass
