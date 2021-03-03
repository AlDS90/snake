import tkinter as tk
import PIL


W = 1000
H = 1000
b_size = 50
delay = 200
len_ = 3
c_body_w = W / b_size
c_body_h = H / b_size
x = [0] * int(c_body_w)
y = [0] * int(c_body_h)


class Snake(tk.Canvas):
    def __init__(self):
        tk.Canvas.__init__(self, width=W, height=H, bg='black')
        self.focus_get()
        self.bind_all('<Key>', self.on_key_pressed)

    def on_key_pressed(self):
        pass


root = tk.Tk()
root.title('Snake')
root.board = Snake
root.resizable(False, False)
w = root.winfo_reqwidth()
h = root.winfo_reqheight()
ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()
x = int((ws - w) / 2)
y = int((hs - h) / 2)
root.geometry('+{0}+{1}'.format(x, y))
root.mainloop()