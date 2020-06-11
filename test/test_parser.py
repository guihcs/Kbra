import unittest

from interpreter.Parser import parser
from interpreter.Tokenizer import lexer


class TestAssignment(unittest.TestCase):
    def test_assignment(self):
        script = """
            $a = 1
            $b = 2
            $c = $a + $b
        """
        result = parser.parse(script, lexer=lexer)

        self.assertEqual(('ASSIGN', ('ID', '$a'), (('CONSTANT', 1),)), result[0])
        self.assertEqual(('ASSIGN', ('ID', '$b'), (('CONSTANT', 2),)), result[1])
        self.assertEqual(('ASSIGN', ('ID', '$c'), ((('ID', '$a'), ('ID', '$b'), ('OP', 'ADD')),)), result[2])


class TestBranching(unittest.TestCase):
    def test_if(self):
        script = """
                    if $a < 3 {
                        $a = 3
                    } elif $b < 4 {
                        $b = 4
                    } else {
                        $c = 5
                    }
                """
        result = parser.parse(script, lexer=lexer)


class TestLoop(unittest.TestCase):
    def test_while(self):
        script = """
                    while $i < 0 {
                        $i = $i + 1
                    }
                        """
        result = parser.parse(script, lexer=lexer)

        self.assertEqual('WHILE', result[0][0])

    def test_repeat(self):
        script = """
                    repeat 20 {
                        $i = $i + 1
                    }
                """
        result = parser.parse(script, lexer=lexer)

        self.assertEqual('REPEAT', result[0][0])

    def test_for(self):
        script = """
                    for $i = 0 to 10 {
                        $i = $i + 1
                    }
                """
        result = parser.parse(script, lexer=lexer)
        self.assertEqual('FOR', result[0][0])


class TestFunction(unittest.TestCase):
    def test_function(self):
        script = """
                    print("test")
                """
        result = parser.parse(script, lexer=lexer)
        self.assertEqual('CALL', result[0][0])
        pass


class TestLearn(unittest.TestCase):
    def test_learn(self):
        script = """
                    learn test $a {
                        print($a)
                    }
                """
        result = parser.parse(script, lexer=lexer)
        self.assertEqual('LEARN', result[0][0])
        self.assertEqual('test', result[0][1])
        self.assertEqual('$a', result[0][2])
        pass


if __name__ == '__main__':
    unittest.main()
