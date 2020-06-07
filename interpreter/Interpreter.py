from interpreter.CodeBuilder import buildCode


class Interpreter:

    def __init__(self, canvas):
        self.canvas = canvas
        self.code = []
        self.stack = []
        self.var = {}
        self.currentLine = 0
        self.functions = {
            'PUSH': self.push,
            'POP': self.pop,
            'ADD': self.add,
            'LT': self.lt,
            'JUMP': self.jump,
            'JUMP_NOT': self.jump_not,
            'CALL': self.call
        }
        self.library = {
            'fw': (1, self.canvas['line']),
            'tr': (1, lambda a: self.canvas['turn'](-a)),
            'tl': (1, self.canvas['turn'])

        }
        pass

    def start(self, script):
        self.code = buildCode(script)
        self.currentLine = 0
        while self.currentLine < len(self.code):
            self.execute(self.code[self.currentLine])

        pass

    def execute(self, line):
        self.functions[line[0]](line)
        self.currentLine += 1
        pass

    def push(self, code):
        if code[1] == 'CONSTANT':
            self.stack.append(code[2])
        elif code[1] == 'ID':
            value = self.var[code[2]]
            self.stack.append(value)
        pass

    def pop(self, code):
        self.var[code[1]] = self.stack.pop()
        pass

    def add(self, code):
        v1 = self.stack.pop()
        v2 = self.stack.pop()
        self.stack.append(v1 + v2)
        pass

    def lt(self, code):
        v2 = self.stack.pop()
        v1 = self.stack.pop()
        self.stack.append(v1 < v2)
        pass

    def jump(self, code):
        self.currentLine = code[1]-1
        pass

    def jump_not(self, code):
        val = self.stack.pop()
        if not val:
            self.currentLine = code[1]
        pass

    def call(self, code):
        if code[1] in self.library:
            fun = self.library[code[1]]
            args = []
            for i in range(fun[0]):
                args.insert(0, self.stack.pop())
            res = fun[1](*args)
            if res:
                self.stack.append(res)
        else:
            pass
        pass