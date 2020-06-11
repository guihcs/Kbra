from interpreter.CodeBuilder import build_code
from interpreter.Linker import Linker
from libs.mat_lib import lib as mat_lib


class Interpreter:

    def __init__(self, canvas_lib):
        self.linker = Linker()
        self.memory = [0 for _ in range(50)]

        self.instruction_pointer = 0
        self.local_pointer = 0
        self.args_pointer = 0
        self.stack_pointer = 10
        self.static_pointer = 0

        self.functions = {
            'PUSH': self.push,
            'POP': self.pop,
            'JUMP': self.jump,
            'JUMPNOT': self.jump_not,
            'CALL': self.call,
            'RET': self.ret,
            'ADD': self.add,
            'MULT': self.mult,
            'SUB': self.sub,
            'DIV': self.div,
            'GT': self.gt,
            'LT': self.lt,
            'LE': self.le,
            'GE': self.ge,
            'EQ': self.eq,
            'NEQ': self.neq

        }
        self.library = {
            # 'message': (2, self.random),
            # 'ask': (2, self.random),
            # 'wait': (1, self.wait)
        }

        self.libs = {**self.library, **canvas_lib, **mat_lib}
        pass

    def start(self, script):
        result, dm = build_code(script)
        code = self.linker.link(result, dm)
        self.execute(code)

        pass

    def execute(self, code):
        self.instruction_pointer = 0
        while self.instruction_pointer < len(code):
            instruction = code[self.instruction_pointer]
            self.functions[instruction[0]](instruction)
            self.instruction_pointer += 1
        pass

    def push(self, code):
        if code[1] == 'CONSTANT':
            self.memory[self.stack_pointer] = code[2]
            self.stack_pointer += 1
        elif code[1] == 'STATIC':
            self.memory[self.stack_pointer] = self.memory[self.static_pointer + code[2]]
            self.stack_pointer += 1
        elif code[1] == 'ARG':
            self.memory[self.stack_pointer] = self.memory[self.args_pointer + code[2]]
            self.stack_pointer += 1
        elif code[1] == 'REGISTER':
            self.push((0, 'CONSTANT', 0))
            self.push((0, 'CONSTANT', self.args_pointer))
            self.push((0, 'CONSTANT', self.local_pointer))
            pass
        pass

    def pop(self, code):
        if code[1] == 'STATIC':
            self.stack_pointer -= 1
            self.memory[self.static_pointer + code[2]] = self.memory[self.stack_pointer]
        pass

    def add(self, _):
        self.stack_pointer -= 1
        v1 = self.memory[self.stack_pointer - 1]
        v2 = self.memory[self.stack_pointer]
        self.memory[self.stack_pointer - 1] = v1 + v2
        pass

    def lt(self, _):
        self.stack_pointer -= 1
        v1 = self.memory[self.stack_pointer - 1]
        v2 = self.memory[self.stack_pointer]
        self.memory[self.stack_pointer - 1] = v1 < v2
        pass

    def jump(self, code):
        self.instruction_pointer = code[1] - 1
        pass

    def jump_not(self, code):
        self.stack_pointer -= 1
        cond = self.memory[self.stack_pointer]
        if not cond:
            self.jump(code)
        pass

    def call(self, code):
        if code[1] == 'DEF':
            self.memory[self.stack_pointer - code[3] - 3] = self.instruction_pointer + 1
            self.args_pointer = self.stack_pointer - code[3]
            self.local_pointer = self.stack_pointer
            for _ in range(code[4]):
                self.push((0, 'CONSTANT', 0))
            self.jump((0, code[2]))
            pass
        else:
            args_address = self.stack_pointer - 1
            args = self.memory[args_address:args_address + code[3]]
            self.libs[code[2]](*args)

            pass

        pass

    def ret(self, _):
        ret_val = self.memory[self.stack_pointer - 1]
        ret_address = self.memory[self.args_pointer - 3]
        l_p = self.memory[self.args_pointer - 1]
        a_p = self.memory[self.args_pointer - 2]
        self.memory[self.args_pointer - 3] = ret_val
        self.stack_pointer = self.args_pointer - 2
        self.local_pointer = l_p
        self.args_pointer = a_p
        self.jump((0, ret_address))
        pass

    def reset(self, _):
        self.stack_pointer = 10
        self.instruction_pointer = 0
        self.libs['reset']()
        pass

    def mult(self, _):
        self.stack_pointer -= 1
        v1 = self.memory[self.stack_pointer - 1]
        v2 = self.memory[self.stack_pointer]
        self.memory[self.stack_pointer - 1] = v1 * v2
        pass

    def sub(self, _):
        self.stack_pointer -= 1
        v1 = self.memory[self.stack_pointer - 1]
        v2 = self.memory[self.stack_pointer]
        self.memory[self.stack_pointer - 1] = v1 - v2
        pass

    def div(self, _):
        self.stack_pointer -= 1
        v1 = self.memory[self.stack_pointer - 1]
        v2 = self.memory[self.stack_pointer]
        self.memory[self.stack_pointer - 1] = v1 // v2
        pass

    def gt(self, _):
        self.stack_pointer -= 1
        v1 = self.memory[self.stack_pointer - 1]
        v2 = self.memory[self.stack_pointer]
        self.memory[self.stack_pointer - 1] = v1 > v2
        pass

    def le(self, _):
        self.stack_pointer -= 1
        v1 = self.memory[self.stack_pointer - 1]
        v2 = self.memory[self.stack_pointer]
        self.memory[self.stack_pointer - 1] = v1 <= v2
        pass

    def ge(self, _):
        self.stack_pointer -= 1
        v1 = self.memory[self.stack_pointer - 1]
        v2 = self.memory[self.stack_pointer]
        self.memory[self.stack_pointer - 1] = v1 >= v2
        pass

    def eq(self, _):
        self.stack_pointer -= 1
        v1 = self.memory[self.stack_pointer - 1]
        v2 = self.memory[self.stack_pointer]
        self.memory[self.stack_pointer - 1] = v1 == v2
        pass

    def neq(self, _):
        self.stack_pointer -= 1
        v1 = self.memory[self.stack_pointer - 1]
        v2 = self.memory[self.stack_pointer]
        self.memory[self.stack_pointer - 1] = v1 != v2
        pass
