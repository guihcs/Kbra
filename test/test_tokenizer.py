import unittest

from interpreter.Tokenizer import lexer


class TestTokenizer(unittest.TestCase):
    def test_recursion(self):
        script = """
                        learn fac $i {
                            if $i < 2 {
                                return 1
                            }
                            return $i * fac($i - 1)
                        }

                        $v = fac(8)
                        print($v)
                        """
        lexer.input(script)


if __name__ == '__main__':
    unittest.main()
