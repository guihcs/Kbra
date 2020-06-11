def link_definition(code, args):
    result_code = []
    symbol_table = {}
    current_symbol = 0
    for line in code:
        if line[0] == 'PUSH' and line[1] == 'ID':
            if line[2] in args:
                result_code.append(('PUSH', 'ARG', args[line[2]]))
            else:
                if line[2] not in symbol_table:
                    symbol_table[line[2]] = current_symbol
                    current_symbol += 1
                result_code.append(('PUSH', 'LOCAL', symbol_table[line[2]]))
        elif line[0] == 'POP':
            if line[2] in args:
                result_code.append(('POP', 'ARG', args[line[2]]))
            else:
                if line[2] not in symbol_table:
                    symbol_table[line[2]] = current_symbol
                    current_symbol += 1
                result_code.append(('POP', 'LOCAL', symbol_table[line[2]]))
        else:
            result_code.append(line)

    return result_code, current_symbol


def resolve_dependencies(code, definitions):
    resolved_code = []
    code.insert(0, ('LABEL', '#_main'))
    for line in code:
        if line[0] == 'CALL' and line[1] in definitions and not definitions[line[1]][0]:
            f_def = definitions[line[1]]
            linked_definition, locals_count = link_definition(f_def[3], f_def[2])
            resolved_code = linked_definition + resolved_code
            definitions[line[1]][0] = True
            definitions[line[1]].append(locals_count)

        resolved_code.append(line)

    resolved_code.insert(0, ('JUMP', '#_main'))

    return resolved_code


class Linker:
    def __init__(self):
        self.definitions = {}
        self.result = []
        self.symbol_table = {}
        self.label_table = {}
        self.current_symbol = 0

    def link(self, code, definitions):
        self.definitions = definitions
        call_map = {
            'PUSH': self.link_push,
            'POP': self.link_pop,
            'CALL': self.link_call,
            'JUMP': self.link_jump,
            'JUMPNOT': self.link_jump
        }

        resolved_code = resolve_dependencies(code, definitions)
        resolved_code = self.resolve_labels(resolved_code)

        for line in resolved_code:
            if line[0] in call_map:
                call_map[line[0]](line)
            else:
                self.result.append(line)
            pass

        return self.result

    def resolve_labels(self, code):
        current_line = 0
        result = []
        for line in code:
            if line[0] == 'LABEL':
                self.label_table[line[1]] = current_line
            else:
                result.append(line)
                current_line += 1
            pass
        return result
        pass

    def link_push(self, line):
        if line[1] == 'ID':
            self.append_code(('PUSH', 'STATIC', self.symbol_table[line[2]]))
            pass
        else:
            self.append_code(line)
        pass

    def link_pop(self, line):
        if line[1] == 'ID':
            if line[2] not in self.symbol_table:
                self.symbol_table[line[2]] = self.current_symbol
                self.current_symbol += 1
            pass
            self.append_code(('POP', 'STATIC', self.symbol_table[line[2]]))
        else:
            self.append_code(line)

    def link_call(self, line):
        if line[1] in self.definitions:
            f_def = self.definitions[line[1]]
            self.append_code(('CALL', 'DEF', self.label_table[f_def[1]], line[2], f_def[4]))
        else:
            self.append_code(('CALL', 'NATIVE', line[1], line[2]))
        pass

    def link_jump(self, line):
        self.append_code((line[0], self.label_table[line[1]]))
        pass

    def append_code(self, code):
        self.result.append(code)
