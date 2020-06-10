import unittest
from unittest.mock import MagicMock
from interpreter.Interpreter import Interpreter


class TestInterpreter(unittest.TestCase):

    def test_branching(self):
        mock = MagicMock()

        canvas_mock = {
            'print': mock
        }

        script = """
            $a = 5
            if $a < 4 {
                $a = 9
            } elif $a < 5 {
                $a = 10
            } else {
                $a = 11
            }
            
            print($a)
        """

        interpreter = Interpreter(canvas_mock)
        interpreter.start(script)

        mock.assert_called_with(11)
        # print(interpreter.memory)

    def test_loop(self):
        mock = MagicMock()

        canvas_mock = {
            'print': mock
        }

        script = """
            $i = 0
            while $i < 5 {
                $i = $i + 1
            }
            print($i)
        """

        interpreter = Interpreter(canvas_mock)
        interpreter.start(script)
        mock.assert_called_with(5)
        # print(interpreter.memory)

    def test_learn_call(self):
        mock = MagicMock()

        canvas_mock = {
            'print': mock
        }

        script = """
            learn add $a, $b {
                return $a + $b                  
            }

            $a = 1
            $b = 2
            print(add($a, $b))
        """

        interpreter = Interpreter(canvas_mock)
        interpreter.start(script)
        # print(interpreter.memory)
        mock.assert_called_with(3)


if __name__ == '__main__':
    unittest.main()
