import unittest

from interpreter.CodeBuilder import build_code
from interpreter.Linker import Linker


class MyTestCase(unittest.TestCase):
    def test_something(self):
        script = """
                    learn add $i, $b {
                        return $a + $b                  
                    }

                    $a = 1
                    $b = 2
                    print(add($a, $b))
                            
                        """
        result, dm = build_code(script)
        linker = Linker()
        linked_code = linker.link(result, dm)

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
        result, dm = build_code(script)
        linker = Linker()
        linked_code = linker.link(result, dm)


if __name__ == '__main__':
    unittest.main()
