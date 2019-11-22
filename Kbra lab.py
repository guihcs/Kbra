from tkinter import *
from PIL import Image, ImageTk

wind = Tk()
canvas = Canvas(wind, background='white')

pilImage = Image.open("Kbra.png")
pilImage = pilImage.resize((int(pilImage.width * 0.6), int(pilImage.height * 0.4)), Image.ANTIALIAS)
pilImage = pilImage.rotate(90, expand=True, resample=Image.BICUBIC)
image = ImageTk.PhotoImage(pilImage)

canvas.create_image(200,200, image=image)
canvas['bg'] = 'red'


canvas.pack()
wind.mainloop()