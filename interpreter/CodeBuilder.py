from interpreter.Tokenizer import lexer
from interpreter.Parser import parser


def buildCode(script):
    code = parser.parse(script, lexer=lexer)

    for line in code:
        print(line)

    pass
