import unittest

from interpreter.CodeBuilder import build_code
from interpreter.Linker import Linker


class MyTestCase(unittest.TestCase):
    def test_something(self):
        script = """
                    learn add $a, $b {
                        return $a + $b                  
                    }

                    $a = 1
                    $b = 2
                    print(add($a, $b))
                            
                        """
        result, dm = build_code(script)
        linker = Linker()
        linked_code = linker.link(result, dm)
        # for i, c in zip(range(len(linked_code)), linked_code):
        #     print(f'{i} : {c}')


if __name__ == '__main__':
    unittest.main()
