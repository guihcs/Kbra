from SyntaxAnalyzer import tokenize, index_of, contains_type
from ExpressionAnalyzer import Parser
from time import sleep
from random import randint


# Class to store block info
class BlockInfo(object):
    def __init__(self, block_start, block_end, calling_key, key_info):
        self.block_start = block_start
        self.block_end = block_end
        self.calling_key = calling_key
        self.key_info = key_info

    def __repr__(self):
        return "start: %s, end: %s, key: %s, info: %s" % (
        str(self.block_start + 1), str(int(self.block_end) + 1), self.calling_key, self.key_info)


# Class to store function info
class FunctionInfo(object):
    def __init__(self):
        pass

    pass


# Class to run script
class Interpreter(object):
    block_start = {}
    block_end = {}

    # the builtin functions
    built_func_map = {
        'print': [1, lambda x: print(x[0])],
        'rand': [2, lambda args: randint(args[0], args[1])]

    }

    def __init__(self, graph_func_map):
        # flags to share info between modules.
        # Flag 0 (jump info) -> 1:function call.  2:function return
        # Flag 1 (function start line)
        # Flag 2 (function name)
        # Flag 3 (misc info)

        self.flag = [0, 0, 0, 0]
        self.pc = [0]
        self.global_var_map = {}
        self.local_var_map = {}
        self.usrdef_func_map = {}
        self.gfunc_map = graph_func_map

        self.parser = Parser(self.global_var_map, self.local_var_map,
                             self.usrdef_func_map, self.gfunc_map, self.built_func_map, self.flag, self.pc)
        self.parse = self.parser.parse

        pass

    # Pre-parse the code, creating the block list and processing user functions
    def preparse(self, lines):
        block_count = 0
        for i in range(len(lines)):
            if '}' in lines[i] and '{' in lines[i]:
                block_count -= 1
                # process the block end
                for key in self.block_start:
                    if self.block_start[key].block_end == block_count:
                        self.block_start[key].block_end = str(i)
                        self.block_end[i] = self.block_start[key]
                        pass
                    pass
                self.block_start[i] = BlockInfo(i, block_count, tokenize(lines[i])[1].value, '')
                block_count += 1

                pass
            elif '{' in lines[i]:
                self.block_start[i] = BlockInfo(i, block_count, tokenize(lines[i])[0].value, '')
                block_count += 1
            elif '}' in lines[i]:
                block_count -= 1
                for key in self.block_start:
                    if self.block_start[key].block_end == block_count:
                        self.block_start[key].block_end = str(i)
                        self.block_end[i] = self.block_start[key]

            pass
        pass

    # execute the 'wait' statement
    def execute_wait(self, line, pc):

        return -1


        pass


    # execute the 'if' statement
    def execute_if(self, line, pc):
        block_start = index_of('{', line)
        express = line[1:block_start]
        value = self.parse(express)[0].value.lower()
        self.block_start[pc].key_info = value
        if value == 'true':
            return -1
        else:
            return int(self.block_start[pc].block_end)

        pass

    # execute 'else'
    def execute_else(self, line, pc):
        endblock_info = self.block_end[pc]
        block_info = self.block_start[pc]
        end_info = endblock_info.key_info
        if end_info == 'true':
            return int(block_info.block_end)
        else:
            return -1
        pass

    # execute the 'while' statement
    def execute_while(self, line, pc):
        block_start = index_of('{', line)
        express = line[1:block_start]
        value = self.parse(express)[0].value

        if value.lower() == 'true':
            return -1
        else:
            val = int(self.block_start[pc].block_end) + 1
            return val
        pass

    # execute 'learn'
    def execute_learn(self, line, pc):
        block_start = index_of('{', line)
        declaration = line[1:block_start]
        args = self.parser.get_args(declaration[1:])
        self.usrdef_func_map[declaration[0].value] = [pc]
        if len(args) > 0 and len(args[0]) > 0:
            for arg in args:
                self.usrdef_func_map[declaration[0].value].append(arg[0].value)


        return int(self.block_start[pc].block_end) + 1
        pass

    # execute return
    def execute_return(self, line, pc):

        expr = line[1:]
        return_val = self.parse(expr)
        if return_val[0].value != 'None':
            # set return flag
            self.flag[0] = 2
            self.parser.expression_buffer.append(return_val[0])

        args = self.usrdef_func_map[self.flag[1]][1:]
        for arg in args:
            del self.local_var_map[arg]
            pass
        return -1

        pass

    # execute a raw line
    def execute_statement(self, line, pc):
        token_list = tokenize(line)

        if contains_type('Null', token_list): raise NameError("Null token error")
        if len(token_list) <= 0 or not token_list: return -1
        start_token = token_list[0].value
        # check for if statement
        if start_token == 'if':
            jump = self.execute_if(token_list, pc)

            return jump
            pass

        # check for while statement
        elif start_token == 'while':
            jump = self.execute_while(token_list, pc)
            return jump
            pass

        # check for learn statement
        elif start_token == 'learn':
            jump = self.execute_learn(token_list, pc)
            return jump
            pass
        # check for return
        elif start_token == 'return':
            jump = self.execute_return(token_list, pc)
            return jump
            pass
        # check for assignment
        elif start_token[0] == '$' and token_list[1].value == '=':

            identifier = start_token
            expression = token_list[2:]
            self.global_var_map[identifier] = self.parse(expression)
            pass
        # check for end block
        elif start_token == '}':
            block_info = self.block_end[pc]
            # process while end block
            if block_info.calling_key == 'while':
                return int(block_info.block_start)
                pass
            # return of user function
            elif block_info.calling_key == 'learn':

                args = self.usrdef_func_map[self.flag[1]][1:]
                for arg in args:
                    del self.local_var_map[arg]
                    pass

                jump = self.flag[2] +1
                self.flag[0] = 0
                self.flag[2] = 0
                return jump

                pass
            else:
                if len(token_list) > 1:
                    # execute else
                    if token_list[1].value == 'else':
                        return self.execute_else(token_list, pc)
                        pass

                pass

            pass
        # resolve expression
        else:
            self.parse(token_list)
            pass
        return -1

    # main
    def start(self, script):
        lines = script.splitlines()
        lineBuff = ""
        self.preparse(lines)

        while self.pc[0] < len(lines):
            line = lines[self.pc[0]]
            if not (line.isspace() or line == ''):

                jump = self.execute_statement(lines[self.pc[0]], self.pc[0])

                # exec func call
                if self.flag[0] == 1:
                    func_def = self.usrdef_func_map[self.flag[1]]
                    jump = func_def[0] + 1
                    self.flag[0] = 0
                    pass
                elif self.flag[0] == 2:
                    self.parser.solve_exp(None)
                    jump = self.flag[2]
                    self.flag[0] = 3


                if self.flag[3] == 1:
                    print(line)
                    return

                if jump >= 0:
                    # print(jump)
                    self.pc[0] = jump
                    # print(lines[pc])
                    continue
                pass

            self.pc[0] += 1
            pass
        # print(self.flag[0], self.flag[1], self.flag[2], self.flag[3])
        pass

    pass
'''
from AppCanvas import AppCanvas

canv = AppCanvas(None)
intr = Interpreter(canv.functions)
file = open('test.txt', 'r')
txt = file.read()
intr.start(txt)

file.close()
'''