import tkinter as tk
from PIL import Image, ImageTk


W: int = 1000
H: int = 1000
B_SIZE: int = 50
DELAY: int = 200
LEN: int = 3
c_body_w = W / B_SIZE
c_body_h = H / B_SIZE
x = [0] * int(c_body_w)
y = [0] * int(c_body_h)


class Snake(tk.Canvas):
    def __init__(self):
        tk.Canvas.__init__(self, width=W, height=H, bg='black', highlightthickness=0)
        self.head_image = None
        self.head = None
        self.body = None
        self.apple = None
        self.delay: int = 0
        self.direction: str = 'Right'
        self.loss: bool = False
        self.focus_get()
        self.bind_all('<Key>', self.on_key_pressed)
        self.load_resources()
        self.begin_play()
        self.pack()

    def on_key_pressed(self):
        pass

    def load_resources(self):
        self.head_image = Image.open('img/head.png')
        self.head = ImageTk.PhotoImage(self.head_image.resize((B_SIZE, B_SIZE), Image.ANTIALIAS))
        self.body = ImageTk.PhotoImage(Image.open('img/body.png').resize((B_SIZE, B_SIZE), Image.ANTIALIAS))
        self.apple = ImageTk.PhotoImage(Image.open('img/apple.png').resize((B_SIZE, B_SIZE), Image.ANTIALIAS))

    def begin_play(self):
        self.delay = DELAY
        self.direction = 'Right'
        self.loss = False
        self.delete(tk.ALL)
        self.spawn_actors()

    def spawn_actors(self):
        x[0] = int(c_body_w / 2) * B_SIZE
        y[0] = int(c_body_h / 2) * B_SIZE
        for i in range(1, LEN):
            x[i] = x[0] - B_SIZE * i
            y[i] = y[0]
        self.create_image(x[0], y[0], image=self.head, anchor='nw', tag='head')
        for i in range(1, LEN):
            self.create_image(x[i], y[i], image=self.body, anchor='nw', tag='body')


root = tk.Tk()
root.title('Snake')
root.board = Snake()
root.resizable(False, False)
ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()
x_center = int((ws - W) / 2)
y_center = int((hs - H) / 2)
root.geometry('+{}+{}'.format(x_center, y_center))
root.mainloop()
