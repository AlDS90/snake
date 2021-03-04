import tkinter as tk
import random as rnd
from PIL import Image, ImageTk

W: int = 1000
H: int = 1000
B_SIZE: int = 50
DELAY: int = 300
MIN_DELAY: int = 100
STEP: int = 5
LEN: int = 3
DIRECTION: str = 'Right'
DIRECTION_TMP: str = 'Right'
c_body_w = int(W / B_SIZE)
c_body_h = int(H / B_SIZE)
x = [0] * c_body_w
y = [0] * c_body_h


class Snake(tk.Canvas):
    def __init__(self):
        tk.Canvas.__init__(self, width=W, height=H, bg='black', highlightthickness=0)
        self.head_image = None
        self.head = None
        self.body = None
        self.apple = None
        self.delay: int = 0
        self.direction: str = DIRECTION
        self.direction_tmp: str = DIRECTION_TMP
        self.loss: bool = False
        self.focus_get()
        self.bind_all('<Key>', self.on_key_pressed)
        self.load_resources()
        self.begin_play()
        self.pack()

    def on_key_pressed(self, e):
        key = e.keysym
        if key == 'Left' and self.direction != 'Right':
            self.direction_tmp = 'Left'
        elif key == 'Right' and self.direction != 'Left':
            self.direction_tmp = 'Right'
        elif key == 'Up' and self.direction != 'Down':
            self.direction_tmp = 'Up'
        elif key == 'Down' and self.direction != 'Up':
            self.direction_tmp = 'Down'
        elif key == 'space' and self.loss:
            self.begin_play()

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
        self.after(self.delay, self.timer)

    def spawn_actors(self):
        self.spawn_apple()
        x[0] = int(c_body_w / 2) * B_SIZE
        y[0] = int(c_body_h / 2) * B_SIZE
        for i in range(1, LEN):
            x[i] = x[0] - B_SIZE * i
            y[i] = y[0]
        self.create_image(x[0], y[0], image=self.head, anchor='nw', tag='head')
        for i in range(LEN - 1, 0, -1):
            self.create_image(x[i], y[i], image=self.body, anchor='nw', tag='body')

    def spawn_apple(self):
        apple = self.find_withtag('apple')
        if apple:
            self.delete(apple[0])
        r_x = rnd.randint(0, c_body_w - 1)
        r_y = rnd.randint(0, c_body_h - 1)
        self.create_image(r_x * B_SIZE, r_y * B_SIZE, anchor='nw', image=self.apple, tag='apple')

    def check_apple(self):
        apple = self.find_withtag('apple')[0]
        head = self.find_withtag('head')[0]
        body = self.find_withtag('body')[-1]
        x_1, y_1, x_2, y_2 = self.bbox(head)
        overlaps = self.find_overlapping(x_1, y_1, x_2, y_2)
        for actor in overlaps:
            if actor == apple:
                tmp_x, tmp_y = self.coords(body)
                self.spawn_apple()
                self.create_image(tmp_x, tmp_y, image=self.body, anchor='nw', tag='body')
                if self.delay < MIN_DELAY:
                    self.delay -= STEP

    def check_collision(self):
        head = self.find_withtag('head')
        body = self.find_withtag('body')
        x_1, y_1, x_2, y_2 = self.bbox(head)
        overlaps = self.find_overlapping(x_1, y_1, x_2, y_2)
        for b in body:
            for actor in overlaps:
                if actor == b:
                    self.loss = True
        if x_1 < 0:
            self.loss = True
        if x_2 > W:
            self.loss = True
        if y_1 < 0:
            self.loss = True
        if y_2 > H:
            self.loss = True

    def timer(self):
        self.check_collision()
        if not self.loss:
            self.check_apple()
            self.update_direction()
            self.move_snake()
            self.after(self.delay, self.timer)
        else:
            self.game_over()

    def update_direction(self):
        self.direction = self.direction_tmp
        head = self.find_withtag('head')
        head_x, head_y = self.coords(head)
        self.delete(head)
        if self.direction == 'Left':
            self.head = ImageTk.PhotoImage(self.head_image.transpose(Image.FLIP_LEFT_RIGHT).resize((B_SIZE, B_SIZE),
                                                                                                   Image.ANTIALIAS))
        else:
            rotates = {'Right': 0, 'Up': 90, 'Down': -90}
            self.head = ImageTk.PhotoImage(self.head_image.rotate(rotates[self.direction]).resize((B_SIZE, B_SIZE),
                                                                                                  Image.ANTIALIAS))
        self.create_image(head_x, head_y, image=self.head, anchor='nw', tag='head')

    def move_snake(self):
        head = self.find_withtag('head')
        body = self.find_withtag('body')
        items = body + head
        for i in range(len(items) - 1):
            current_x_y = self.coords(items[i])
            next_x_y = self.coords(items[i + 1])
            self.move(items[i], next_x_y[0] - current_x_y[0], next_x_y[1] - current_x_y[1])
        if self.direction == 'Left':
            self.move(head, -B_SIZE, 0)
        elif self.direction == 'Right':
            self.move(head, B_SIZE, 0)
        elif self.direction == 'Up':
            self.move(head, 0, -B_SIZE)
        elif self.direction == 'Down':
            self.move(head, 0, B_SIZE)

    def game_over(self):
        body = self.find_withtag('body')
        self.delete(tk.ALL)
        self.create_text(self.winfo_width() / 2, self.winfo_height() / 2 - 60,
                         text='You lose!', fill='white', font='tahoma 40', tag='text')
        self.create_text(self.winfo_width() / 2, self.winfo_height() / 2,
                         text='Length your snake: %s.' % len(body), fill='white', font='tahoma 40', tag='text')
        self.create_text(self.winfo_width() / 2, self.winfo_height() / 2 + 60,
                         text='Press space to run new game.', fill='white', font='tahoma 40', tag='text')


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
