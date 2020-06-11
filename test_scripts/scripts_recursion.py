

rec1 = """
            learn fac $i {
                if $i < 2 {
                    return 1
                }
                return $i * fac($i - 1)
            }
            
            $v = fac(7)
            print($v)
"""