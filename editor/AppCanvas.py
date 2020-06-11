from math import sin, cos, radians
from tkinter import *

from PIL import Image, ImageTk


def rgb_to_hex(b, g, r):
    r_hex = hex(r)[2:].upper().rjust(2, '0')
    g_hex = hex(g)[2:].upper().rjust(2, '0')
    b_hex = hex(b)[2:].upper().rjust(2, '0')
    color = '#%s%s%s' % (r_hex, g_hex, b_hex)
    return color


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

        self.library = {
            'fw': self.draw_line,
            'bw': lambda l: self.draw_line(-l),
            'tl': self.turn,
            'tr': lambda a: self.turn(-a),
            'dir': self.set_dir,
            'getdir': self.get_dir,
            'center': self.center,
            'go': self.set_pos,
            'gx': lambda x: self.set_pos(x, self.canvas['gety']()),
            'gy': lambda y: self.set_pos(self.canvas['gety'](), y),
            'getx': self.get_current_x,
            'gety': self.get_current_y,
            'pu': self.set_draw(False),
            'pd': self.set_draw(True),
            'pw': self.set_line_width,
            'pc': self.set_line_color,
            # 'cs': self.canvas['pc'],
            'cc': self.set_bg,
            'clear': self.clear,
            'reset': self.reset,
            # 'ss': self.reset,
            # 'sh': self.reset,
            'print': self.draw_text,
            # 'fontsize': self.canvas['print'],

        }

        self.canvas = Canvas(root, width=self.__canv_width, height=self.__canv_height, bg='white', borderwidth=2,
                             highlightthickness=5, cursor='X_cursor', relief='groove')

        self.pilImage = Image.open("resources/Kbra.png")
        self.pilImage = self.pilImage.resize((int(self.pilImage.width * 0.3), int(self.pilImage.height * 0.2)),
                                             Image.ANTIALIAS)

        self.spriteImage = ImageTk.PhotoImage(self.pilImage)

        self.canvas.create_image(self.__cur_pos_x, self.__cur_pos_y, image=self.spriteImage, tag='main')
        pass

    def get_dir(self):
        _dir = 90 - self.__cur_dir
        if not (_dir < 360) or not (_dir > 0) and not (_dir > -360):
            return _dir % 360
        elif _dir < 0:
            return 360 + _dir
        else:
            return _dir

    def clear(self):
        self.canvas.delete('all')
        self.set_sprite_dir(self.__cur_dir)

    def reset(self):
        self.set_dir(0)
        self.center()
        self.clear()

    def center(self):
        self.__cur_pos_x = self.start_posx
        self.__cur_pos_y = self.start_posy

    def set_bg(self, r, g, b):
        color = rgb_to_hex(b, g, r)
        self.canvas['bg'] = color

    def get_current_x(self):
        return self.__cur_pos_x

    def get_current_y(self):
        return self.__cur_pos_y

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

        pass

    def set_dir(self, _dir):
        self.__cur_dir = 90 - _dir
        self.set_sprite_dir(self.__cur_dir)
        pass

    def turn(self, _dir):
        self.__cur_dir = self.__cur_dir + _dir
        self.set_sprite_dir(self.__cur_dir)

    def set_line_width(self, width):
        self.line_width = width[0]

    def set_line_color(self, r, g, b):
        color = rgb_to_hex(b, g, r)
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
