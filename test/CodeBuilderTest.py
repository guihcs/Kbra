import unittest
from interpreter.CodeBuilder import buildCode


class MyTestCase(unittest.TestCase):

    def test_something(self):
        script = """
                    $a = 1  + 1      
                    
                    if $a > 2 {
                    
                        print($a)
                        
                        print($b + 1)

                        if $b < 3 {

                            pow($c + 1, 2 + 2)

                        }

                    }

                    if $c > 4 {

                        $a = 2

                        print($a)            
                    }

                    $i = 0

                    while $i < 3 {

                        $i = $i + 1

                    }
                """

        res = buildCode(script)
        for line, re in zip(range(len(res)), res):
            print(f'{line} : {re}')

if __name__ == '__main__':
    unittest.main()
