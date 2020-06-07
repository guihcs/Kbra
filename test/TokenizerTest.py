import unittest
from interpreter.Tokenizer import lexer


class MyTestCase(unittest.TestCase):
    def test_something(self):
        script = """
                    $a = 1        
                    
                    
                       
                    if $a > 2 {
                    
                    
                        print($a)
                        
                        
                        print($b)
                        
                        
                        if $b < 3 {
                        
                        
                            print($c)
                            
                            
                        }
                        
                    }

                    if $c > 4 {
                    
                        $a = 1
                        
                        print($a)            
                    }

                    $i = 0
                    
                    while $i < 3 {
                    
                        $i = $i + 1
                        
                    }
                """
        lexer.input(script)
        while True:
            tok = lexer.token()
            if not tok:
                break  # No more input
            print(tok)


if __name__ == '__main__':
    unittest.main()
