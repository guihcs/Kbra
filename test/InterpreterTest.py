import unittest

from interpreter.Interpreter import Interpreter


class MyTestCase(unittest.TestCase):
    def test_something(self):
        canvasMock = {
            'line': print
        }

        script = """
            $i = 0
            $res = 0
            while $i < 4 {
                $res = $res + $i       
                $i = $i + 1     
            }
        
        """

        interpreter = Interpreter(canvasMock)
        interpreter.start(script)

if __name__ == '__main__':
    unittest.main()
