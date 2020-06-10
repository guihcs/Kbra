import unittest
from unittest.mock import MagicMock
from interpreter.Interpreter import Interpreter


class MyTestCase(unittest.TestCase):
    def test_something(self):

        canvas_mock = MagicMock()

        script = """
            $a = 1
        """

        interpreter = Interpreter(canvas_mock)
        interpreter.start(script)
        print(interpreter.stack)


if __name__ == '__main__':
    unittest.main()
