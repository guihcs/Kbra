from Interpreter import Interpreter
from AppCanvas import AppCanvas
from Editor import Editor, EditorThread

from tkinter import *


def run(event):
    interpreter = Interpreter(canvas.functions)
    interpreter.start(editor.get_text())
    pass

def keyDown(e):
    #editor_thread.isPressing = True

    pass
def keyUp(e):
    #editor_thread.isPressing = False
    editor.color()
    pass

window = Tk()
window.wm_title('Kbra Project')
window.resizable(0,0)

window.bind('<KeyPress>', keyDown)
window.bind('<KeyRelease>', keyUp)

def exit_app():
    editor_thread.request_stop()
    window.after(200, window.destroy)
    pass

window.protocol('WM_DELETE_WINDOW', exit_app)



frame = Frame(window)

button = Button(window, text='Play', borderwidth=2, highlightthickness=5)

editor = Editor(frame)
editor_thread = EditorThread(editor.editor)

canvas = AppCanvas(frame)

button.bind('<Button-1>', run)
button.pack()

canvas.canvas.pack(side=RIGHT)
editor.edit.pack(side=RIGHT)

frame.pack()

#editor_thread.start()
window.mainloop()
