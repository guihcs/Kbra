from interpreter.CodeBuilder import build_code
from interpreter.Linker import Linker


class Interpreter:

    def __init__(self, canvas):
        self.linker = Linker()
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
            'bw': (1, lambda l: self.canvas['line'](-l)),
            'tl': (1, self.canvas['turn']),
            'tr': (1, lambda a: self.canvas['turn'](-a)),
            'dir': (1, self.canvas['dir']),
            'getdir': (0, self.canvas['getdir']),
            'center': (0, self.canvas['center']),
            'go': (2, self.canvas['go']),
            'gx': (1, lambda x: self.canvas['go'](x, self.canvas['gety']())),
            'gy': (1, lambda y: self.canvas['go'](self.canvas['gety'](), y)),
            'getx': (0, self.canvas['getx']),
            'gety': (0, self.canvas['gety']),
            'pu': (0, self.canvas['draw'](False)),
            'pd': (0, self.canvas['draw'](True)),
            'pw': (1, self.canvas['pw']),
            'pc': (3, self.canvas['pc']),
            # 'cs': (2, self.canvas['pc']),
            'cc': (3, self.canvas['cc']),
            'clear': (0, self.canvas['clear']),
            'reset': (0, self.reset),
            # 'ss': (0, self.reset),
            # 'sh': (0, self.reset),
            'print': (1, self.canvas['print']),
            # 'fontsize': (1, self.canvas['print']),
            # 'round': (1, self.round),
            # 'rnd': (2, self.random),
            # 'mod': (2, self.random),
            # 'sqrt': (2, self.random),
            # 'pi': (2, self.random),
            # 'sin': (2, self.random),
            # 'cos': (2, self.random),
            # 'tan': (2, self.random),
            # 'arcsin': (2, self.random),
            # 'arccos': (2, self.random),
            # 'arctan': (2, self.random),
            # 'message': (2, self.random),
            # 'ask': (2, self.random),
            # 'wait': (1, self.wait)


        }
        pass

    def start(self, script):
        result, dm = build_code(script)
        self.code = self.linker.link(result, dm)
        self.currentLine = 0
        while self.currentLine < len(self.code):
            self.execute(self.code[self.currentLine])

        pass

    def execute(self, line):
        self.functions[line[0]](line)
        self.currentLine += 1
        pass

    def push(self, code):

        pass

    def pop(self, code):

        pass

    def add(self, _):

        pass

    def lt(self, _):

        pass

    def jump(self, code):

        pass

    def jump_not(self, code):

        pass

    def call(self, code):

        pass

    def reset(self, code):

        pass