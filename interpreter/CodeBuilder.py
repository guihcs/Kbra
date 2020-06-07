from interpreter.Tokenizer import lexer
from interpreter.Parser import parser


def buildCode(script):
    code = parser.parse(script, lexer=lexer)
    return code
