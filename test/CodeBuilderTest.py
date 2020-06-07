import unittest
from interpreter.CodeBuilder import buildCode


class MyTestCase(unittest.TestCase):

    def test_something(self):
        script = """
                    $a = 1        



                    if $a > 2 {


                        print($a)


                        print($b)


                        if $b < 3 {


                            pow($c, 2)


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


if __name__ == '__main__':
    unittest.main()
