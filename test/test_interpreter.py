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
            $a = 4
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

        mock.assert_called_with(10)
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


class TestLearn(unittest.TestCase):
    def test_learn_call(self):
        canvas_mock = {
            'print': MagicMock(),
            'fw': MagicMock()
        }

        script = """
            learn add $a, $b {
                return $a + $b                  
            }

            $a = 1
            $b = 2
            print(add($a, $b))
            fw(100)
        """

        interpreter = Interpreter(canvas_mock)
        interpreter.start(script)
        # print(interpreter.memory)
        canvas_mock['print'].assert_called_with(3)
        canvas_mock['fw'].assert_called_with(100)

    def test_learn_call2(self):
        canvas_mock = {
            'reset': MagicMock(),
            'fw': MagicMock()
        }
        script = """
                    reset()
            learn koch $a, $i {            
                fw($a)    
            }
            
            koch(50, 2)
        """

        interpreter = Interpreter(canvas_mock)
        interpreter.start(script)
        canvas_mock['fw'].assert_called_with(50)
        canvas_mock['reset'].assert_called_once()

    def test_param_passing(self):
        canvas_mock = {
            'print': MagicMock(),
        }
        script = """
                            
                learn koch $a, $i {            
                    print($a)    
                }

                koch(50, 2)
                """

        interpreter = Interpreter(canvas_mock)
        interpreter.start(script)
        canvas_mock['print'].assert_called_with(50)


class TestFunctionCall(unittest.TestCase):

    def test_native_call(self):
        canvas_mock = {
            'fw': MagicMock()
        }

        script = """
                   fw(100)
                """

        interpreter = Interpreter(canvas_mock)
        interpreter.start(script)
        canvas_mock['fw'].assert_called_with(100)

        pass

    def test_empty_call(self):
        canvas_mock = {
            'reset': MagicMock()
        }

        script = """
                   reset()
                """

        interpreter = Interpreter(canvas_mock)
        interpreter.start(script)
        canvas_mock['reset'].assert_called_once()


class TestRecursion(unittest.TestCase):

    def test_recursion(self):
        canvas_mock = {
            'print': MagicMock()
        }

        script = """
                learn fac $i {
                    if $i < 2 {
                        return 1
                    }
                    return $i * fac($i - 1)
                }
                
                $v = fac(7)
                print($v)
                """

        interpreter = Interpreter(canvas_mock)
        interpreter.start(script)
        canvas_mock['print'].assert_called_with(5040)
        pass


if __name__ == '__main__':
    unittest.main()
