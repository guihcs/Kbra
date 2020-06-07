import unittest
from interpreter.CodeBuilder import buildCode


class MyTestCase(unittest.TestCase):

    def test_something(self):
        script = """
                $i = 0
                $res = 0
                while $i < 3 {
                    $res = $res + $i            
                }
                """

        res = buildCode(script)
        for line, re in zip(range(len(res)), res):
            print(f'{line} : {re}')

if __name__ == '__main__':
    unittest.main()
