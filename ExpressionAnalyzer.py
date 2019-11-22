from SyntaxAnalyzer import Token, get_integer, contains, contains_type, replace_tok


# Info to buffer expressions
class ExpressionInfo(object):
    def __init__(self, line, expression):
        self.line = line
        self.expression = expression

    def __repr__(self):
        expr = []
        for tok in self.expression:
            expr.append(tok.value)
        return "line: %d expression: %s" % (self.line + 1, ''.join(expr))


# class to resolve expressions
class Parser(object):
    # the supported language operators
    operations = {
        '^': lambda x, y: x ** y,
        '*': lambda x, y: x * y,
        '/': lambda x, y: x / y,
        '+': lambda x, y: x + y,
        '#-': lambda x: -x,
        '-': lambda x, y: x - y,
        '>': lambda x, y: x > y,
        '<': lambda x, y: x < y,
        '>=': lambda x, y: x >= y,
        '<=': lambda x, y: x <= y,
        '==': lambda x, y: x == y,
        '!=': lambda x, y: x != y,
        '#not': lambda x: not x,
        'and': lambda x, y: x and y,
        'or': lambda x, y: x or y

    }

    def __init__(self, global_map, local_map, function_map, gfunc_map, built_func_map, flag, pc):
        self.global_map = global_map
        self.local_map = local_map
        self.usr_function_map = function_map
        self.built_func_map = built_func_map
        self.gfunc_map = gfunc_map
        self.flag = flag
        self.pc = pc
        self.expression_buffer = []

    # get argument list to use in function
    def get_args(self, args):
        # last_tok_type = None
        last_col_index = -1
        args_list = []
        for i in range(len(args)):
            if args[i].value == ',':
                args_list.append(args[last_col_index + 1:i])
                last_col_index = i
                pass
        else:
            args_list.append(args[last_col_index + 1:])

        return args_list
        pass

    # function to process function call
    def exec_func(self, exp, f_index, f_map):
        func_id = exp[f_index].value
        arg_number = f_map[func_id][0]
        func = f_map[func_id][1]
        exec = True
        args = self.get_args(exp[f_index + 1:])
        if arg_number > 0:
            for i in range(len(args)):
                arg = self.parse(args[i])[0].get_value()

                if arg is None: exec = False
                args[i] = arg



        if exec:
            res = Token(str(func(args)))
        else:
            res = Token('None')
        del exp[f_index + 1:]
        exp[f_index] = res

        pass

    # Solve expression without brackets
    def solve_exp(self, expression):
        # exec stack operations
        if self.flag[0] == 2:
            val = self.expression_buffer.pop()
            expr_info = self.expression_buffer.pop()
            expr = expr_info.expression
            replace_tok(Token('@'), val, expr, 1)
            expr_info.expression = expr
            self.expression_buffer.append(expr_info)
            self.flag[2] = expr_info.line
            return
        elif self.flag[0] == 3:
            exp_info = self.expression_buffer.pop()
            expression = exp_info.expression
            self.flag[0] = 0

        # check for var
        for i in range(len(expression)):

            tok = expression[i]
            if tok.tok_type == 'identifier':
                # is variable
                if tok.value[0] == '$':
                    if tok.value in self.global_map.keys():
                        var_value = self.global_map[tok.value][0]
                        expression[i] = var_value
                    elif tok.value in self.local_map.keys():
                        var_value = self.local_map[tok.value][0]
                        expression[i] = var_value
                    else:
                        raise ReferenceError("Variable not declared")

            pass


        # check for func
        while contains_type('identifier', expression):
            for i in range(len(expression)):
                tok = expression[i]
                if tok.tok_type == 'identifier':

                    # Check if function exists in user defined functions and execute
                    if tok.value in self.usr_function_map.keys():
                        args = []
                        if len(expression) > 0:

                            args = self.get_args(expression[1:])
                            if len(args) > 0 and len(args[0]) > 0:
                                fmap = self.usr_function_map[tok.value]
                                fargs = fmap[1:]
                                for i in range(len(args)):
                                    self.local_map[fargs[i]] = args[i]
                                    pass
                                    expression = expression[:1]

                        replace_tok(tok, Token('@'), expression, 1)
                        self.expression_buffer.append(ExpressionInfo(self.pc[0], expression))
                        expression = [Token('None')]
                        # set function call
                        self.flag[0] = 1
                        # set func info
                        self.flag[1] = tok.value
                        self.flag[2] = self.pc[0]
                        pass
                    # Check if function exists in graphic functions
                    elif tok.value in self.gfunc_map:
                        self.exec_func(expression, i, self.gfunc_map)
                    # Check if function exists in built functions
                    elif tok.value in self.built_func_map:
                        self.exec_func(expression, i, self.built_func_map)
                    # Function doesn't exists.
                    else:
                        raise ReferenceError("Function not declared")

                    break

        if len(expression) <= 1:
            return expression

        # Define order of operations
        operators_add = ('#', '^', '*', '+', '>', '=', '#', 'and', 'or')
        operators_sub = ('-', '', '/', '-', '<', '!', 'not', '', '')
        for op in range(len(operators_add)):
            op_add = operators_add[op]
            op_sub = operators_sub[op]
            for i in range(len(expression)):
                operator = expression[i].value
                if operator == operators_add[op] or operator == operators_sub[op]:

                    left_express = []
                    right_express = []
                    left_op = expression[i - 1].get_value()
                    right_op = expression[i + 1].get_value()
                    op_result = 0

                    # Deal with unary operator at start of expression
                    if op_add == '#' and (op_sub == '-' or op_sub == 'not') and i == 0:

                        if expression[i + 1].tok_type == 'symbol': continue
                        right_express = expression[i + 2:]
                        op_result = self.operations[op_add + op_sub](right_op)
                        pass
                    # deal with unary operator in middle of expression
                    elif op_add == '#' and (op_sub == '-' or op_sub == 'not') and i > 0:
                        if expression[i + 1].tok_type == 'symbol': continue
                        left_express = expression[:i]
                        right_express = expression[i + 2:]
                        op_result = self.operations[op_add + op_sub](right_op)

                        if left_express[-1].tok_type == 'number' and operator == '-':
                            left_express.append(Token('+'))
                            pass
                        pass

                    # deal with binary operator
                    else:
                        left_express = expression[:i - 1]
                        right_express = expression[i + 2:]
                        # check if comparison operator hav equals symbol
                        if (operator == '>' or operator == '<' or operator == '=' or operator == '!') and expression[
                                    i + 1].value == '=':
                            operator = operator + '='
                            right_express = expression[i + 3:]
                            right_op = expression[i + 2].get_value()
                            pass

                        op_result = self.operations[operator](left_op, right_op)
                        if expression[i - 1].tok_type == 'string' or expression[i + 1].tok_type == 'string':
                            op_result = "\"%s\"" % op_result
                        pass

                    op_result = get_integer(op_result)
                    rb = [Token(str(op_result))]
                    result = left_express + rb + right_express
                    return self.solve_exp(result)

    # resolve a full expression with braces
    def parse(self, expression):
        if len(expression) == 1: return self.solve_exp(expression)
        if len(expression) <= 1: return expression
        in_bra = 0
        out_bra = 0
        if contains('(', expression):
            for i in range(len(expression)):

                if expression[i].value == '(': in_bra = i
                if expression[i].value == ')':
                    out_bra = i
                    break
            if out_bra:
                lef_exp = expression[0:in_bra]
                rig_exp = expression[out_bra + 1:]
                sub = expression[in_bra + 1:out_bra]
                sub = self.solve_exp(sub)
                expression = lef_exp + sub + rig_exp
            else:
                raise SyntaxError("Brace inconsistency")

        else:
            sub = self.solve_exp(expression)
            expression = self.solve_exp(sub)

        return self.parse(expression)
