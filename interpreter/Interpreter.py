from interpreter.CodeBuilder import buildCode


class Interpreter:

    def __init__(self, canvas):
        self.canvas = canvas
        pass

    def start(self, script):
        res = buildCode(script)
        print(res)
        # self.canvas['line'](res)
        pass
