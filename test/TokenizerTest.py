import unittest
from interpreter.Tokenizer import lexer

class MyTestCase(unittest.TestCase):
    def test_something(self):
        script = """
                    $a = 1 + 1 * 2
                    $b = 2 * 2
                    $c = $a + $b
                """
        lexer.input(script)
        while True:
            tok = lexer.token()
            if not tok:
                break  # No more input
            print(tok)


if __name__ == '__main__':
    unittest.main()
