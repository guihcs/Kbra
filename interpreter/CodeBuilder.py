from interpreter.Parser import parser
from interpreter.Tokenizer import lexer

resultCode = []

current_line = [0]

stack_functions = {
    '+': 'ADD',
    '>': 'GT',
    '<': 'LT'
}


def buildCode(script):
    code = parser.parse(script, lexer=lexer)

    buildStatements(code)
    return resultCode


def buildStatements(statements):
    for statement in statements:
        buildInstruction(statement)


def buildInstruction(instruction):
    if instruction[0] == 'ASSIGN':
        buildAssignment(instruction[1], instruction[2])
    elif instruction[0] == 'BRANCH':
        buildBranch(instruction[1], instruction[2], instruction[3])
    elif instruction[0] == 'FUNCTION':
        buildFunctionCall(instruction[1], instruction[2])


def buildAssignment(address, expression):
    buildExpression(expression)
    writeCode(('POP', address[1]))
    pass


def buildBranch(key, expression, statements):
    expression_start = getCurrentLine()
    buildExpression(expression)
    curline = getCurrentLine()
    writeCode((key,))
    buildStatements(statements)

    if key == 'while':
        writeCode(('JUMP', expression_start))

    replaceCode(curline, ('JUMP_NOT', getCurrentLine()))

    pass


def buildExpression(expression):
    if len(expression) < 3:
        buildTerm(expression)
        pass
    else:
        for term in expression:
            buildTerm(term)
            pass


def buildTerm(term):
    if term[0] == 'CONSTANT':
        writeCode(('PUSH', 'CONSTANT', term[1]))
    elif term[0] == 'ID':
        writeCode(('PUSH', 'ID', term[1]))
    elif term[0] == 'OPERATOR':
        writeCode((stack_functions[term[1]], ))
    elif term[0] == 'FUNCTION':
        buildFunctionCall(term[1], term[2])


def buildFunctionCall(function, args):
    if len(args) < 2:
        buildExpression(args[0])
    else:
        for arg in args:
            if len(arg) == 1:
                buildExpression(arg[0])
            else:
                buildExpression(arg)

    writeCode(('CALL', function))


def writeCode(code):
    current_line[0] += 1
    resultCode.append(code)


def replaceCode(line, code):
    resultCode[line] = code


def getCurrentLine():
    return current_line[0]
