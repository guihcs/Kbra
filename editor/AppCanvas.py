from math import sin, cos, radians
from tkinter import *
from PIL import Image, ImageTk


class AppCanvas(object):
    def __init__(self, root):
        self.pilImage = None
        self.__bg = '#FF0000'
        self.__canv_width = 550
        self.__canv_height = 550
        self.start_posx = self.__canv_width / 2
        self.start_posy = self.__canv_height / 2
        self.__cur_pos_x = self.start_posx
        self.__cur_pos_y = self.start_posy
        self.__cur_dir = 90
        self.__can_draw = True
        self.line_width = 1
        self.line_color = '#000000'

        self.functions = {
            'line': self.draw_line,
            'turn': self.turn,
            'getdir': self.get_dir,
            'dir': self.set_dir,
            'direction': self.set_dir,
            'center': self.center,
            'go': self.set_pos,
            'getx': self.get_current_x,
            'gety': self.get_current_y,
            'draw': self.set_draw,
            'pc': self.set_line_color,
            'pw': self.set_line_width,
            'cc': self.set_bg,
            'clear': self.clear,
            'reset': self.reset,
            'print': self.draw_text
        }

        self.canvas = Canvas(root, width=self.__canv_width, height=self.__canv_height, bg='white', borderwidth=2,
                             highlightthickness=5, cursor='X_cursor', relief='groove')

        # self.canvas.create_rectangle(20, 20, self.canvas.winfo_reqwidth() - 20, self.canvas.winfo_reqheight() - 20)
        #
        # self.canvas.create_rectangle(self.__cur_pos_x - 10, self.__cur_pos_y - 10, self.__cur_pos_x + 10,
        #                              self.__cur_pos_y + 10,
        #                              fill='green', tag='main')

        self.pilImage = Image.open("resources/Kbra.png")
        self.pilImage = self.pilImage.resize((int(self.pilImage.width * 0.3), int(self.pilImage.height * 0.2)), Image.ANTIALIAS)

        self.spriteImage = ImageTk.PhotoImage(self.pilImage)

        self.canvas.create_image(self.__cur_pos_x, self.__cur_pos_y, image= self.spriteImage, tag='main')
        pass

    # Returns the formatted direction
    def get_dir(self):
        _dir = 90 - self.__cur_dir
        if not (_dir < 360) or not (_dir > 0) and not (_dir > -360):
            return _dir % 360
        elif _dir < 0:
            return 360 + _dir
        else:
            return _dir

    # def clear
    def clear(self):
        self.canvas.delete('all')
        self.canvas.create_rectangle(20, 20, self.canvas.winfo_reqwidth() - 20, self.canvas.winfo_reqheight() - 20)

        # self.set_sprite_dir(self.__cur_dir)

        self.canvas.create_rectangle(self.__cur_pos_x - 10, self.__cur_pos_y - 10, self.__cur_pos_x + 10,
                                     self.__cur_pos_y + 10,
                                     fill='green', tag='main')

    # set reset
    def reset(self):
        self.set_dir(0)
        self.center()
        self.clear()

    # Place the pointer in the middle
    def center(self):
        self.__cur_pos_x = self.start_posx
        self.__cur_pos_y = self.start_posy

    def set_bg(self, r, g, b):
        r_hex = hex(r)[2:].upper().rjust(2, '0')
        g_hex = hex(g)[2:].upper().rjust(2, '0')
        b_hex = hex(b)[2:].upper().rjust(2, '0')

        color = '#%s%s%s' % (r_hex, g_hex, b_hex)
        self.canvas['bg'] = color

    def get_current_x(self):
        return self.__cur_pos_x

    def get_current_y(self):
        return self.__cur_pos_y

    # Set current pos
    def set_pos(self, x, y):

        move_x = x - self.__cur_pos_x
        move_y = y - self.__cur_pos_y

        self.__cur_pos_x = x
        self.__cur_pos_y = y

        self.canvas.move('main', move_x, move_y)

    def set_sprite_dir(self, _dir):
        img = self.pilImage.rotate(-90 + _dir, expand=True, resample=Image.BICUBIC)

        self.spriteImage = ImageTk.PhotoImage(img)
        self.canvas.create_image(self.__cur_pos_x, self.__cur_pos_y, image=self.spriteImage, tag='main')
        # self.canvas.update()
        pass

    # set current direction
    def set_dir(self, _dir):
        self.__cur_dir = 90 - _dir
        # self.set_sprite_dir(self.__cur_dir)
        pass

    # Turn left with the angle _dir
    def turn(self, _dir):
        self.__cur_dir = self.__cur_dir + _dir
        # self.set_sprite_dir(self.__cur_dir)

    def set_line_width(self, width):
        self.line_width = width[0]

    def set_line_color(self, r, g, b):
        r_hex = hex(r)[2:].upper().rjust(2, '0')
        g_hex = hex(g)[2:].upper().rjust(2, '0')
        b_hex = hex(b)[2:].upper().rjust(2, '0')

        color = '#%s%s%s' % (r_hex, g_hex, b_hex)
        self.line_color = color

        pass

    def set_draw(self, val):
        self.__can_draw = val

    def draw_text(self, text):

        if self.line_width < 10:
            width = 10
        else:
            width = self.line_width

        self.canvas.create_text(self.__cur_pos_x, self.__cur_pos_y, text=text,
                                fill=self.line_color, font=('Arial', width), anchor=W)

    # Draw a line using the current directio
    def draw_line(self, length):
        vec_dir_x = cos(radians(self.__cur_dir))
        vec_dir_y = sin(radians(self.__cur_dir))

        new_pointx = self.__cur_pos_x + vec_dir_x * length
        new_pointy = self.__cur_pos_y - vec_dir_y * length

        if self.__can_draw:
            self.canvas.create_line(self.__cur_pos_x, self.__cur_pos_y, new_pointx, new_pointy,
                                    width=self.line_width, fill=self.line_color)

        self.__cur_pos_x = new_pointx
        self.__cur_pos_y = new_pointy

        self.canvas.move('main', vec_dir_x * length, -vec_dir_y * length)
        self.canvas.tag_raise('main')
        pass

    pass
