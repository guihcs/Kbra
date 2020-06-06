import unittest
from interpreter.CodeBuilder import buildCode


class MyTestCase(unittest.TestCase):

    def test_something(self):
        script = """
            $a = 1 + 1 * 2
            $b = 2 * 2
            $c = $a + $b
            
        """

        res = buildCode(script)



if __name__ == '__main__':
    unittest.main()
