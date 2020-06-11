from threading import Thread
from tkinter import *


class EditorThread(Thread):
    def __init__(self, editor):
        super().__init__()
        self.flag = 0
        self.isPressing = False
        self.editor = editor

        self.editor.tag_config('key', foreground='blue')
        self.editor.tag_config('com', foreground='gray')
        self.editor.tag_config('var', foreground='purple')

        self.keywords = "if|else|while|learn|return|None|wait|none"
        self.funcs = "print|rand|fw|bw|tl|tr|dir|getdirection|center|go|getx|gety|pu|pd|pw|pc|clear|reset"

    def run(self):
        while self.flag == 0:

            while self.flag == 0:
                if self.isPressing: continue

                textlines = self.editor.get('1.0', END + '-1c').splitlines()

                self.editor.method_name(textlines)

            pass
        pass

    def request_stop(self):
        self.flag = 1
        pass


class Editor(object):
    def __init__(self, root):
        self.edit = Frame(root)

        self.editor = Text(self.edit, width=35, height=33, borderwidth=2, tabs='0.6c', wrap='none')

        vsb = Scrollbar(self.edit, orient='vertical', command=self.editor.yview)
        hsb = Scrollbar(self.edit, orient='horizontal', command=self.editor.xview)

        self.editor['yscrollcommand'] = vsb.set
        self.editor['xscrollcommand'] = hsb.set

        self.editor.grid()
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, sticky='ew')

        self.editor.tag_config('key', foreground='blue')
        self.editor.tag_config('com', foreground='gray')
        self.editor.tag_config('var', foreground='purple')

        self.keywords = "if|else|while|learn|return|None|wait|none"
        self.funcs = "print|rand|fw|bw|tl|tr|dir|getdirection|center|go|getx|gety|pu|pd|pw|pc|clear|reset"

    pass

    def get_text(self):
        return self.editor.get('1.0', 'end-1c')

    def color(self):

        textlines = self.get_text().splitlines()

        # check for keywords
        self.method_name(textlines)

    def method_name(self, textlines):
        for i in range(len(textlines)):
            find = re.finditer(r"\b(%s|%s)\b" % (self.keywords, self.funcs), textlines[i])
            for match in find:
                span = match.span()
                self.editor.tag_add('key', '%d.%d' % (i + 1, span[0]), '%d.%d' % (i + 1, span[1]))
                pass
        # light comments
        for i in range(len(textlines)):
            find = re.finditer(r"(?=#).+", textlines[i])
            for match in find:
                span = match.span()
                self.editor.tag_add('com', '%d.%d' % (i + 1, span[0]), '%d.%d' % (i + 1, span[1]))
                pass
        # remove all other
        for i in range(len(textlines)):
            if '#' in textlines[i]:
                line = re.match(r"^.+?(?=#)", textlines[i])
                if line is None:
                    continue
                line = line.group()
            else:
                line = textlines[i]
            find = re.finditer(r"(?!(%s|%s)\b)\b\w+" % (self.keywords, self.funcs), line)
            for match in find:
                span = match.span()
                self.editor.tag_remove('key', '%d.%d' % (i + 1, span[0]), '%d.%d' % (i + 1, span[1]))
                self.editor.tag_remove('com', '%d.%d' % (i + 1, span[0]), '%d.%d' % (i + 1, span[1]))
                pass

    pass
