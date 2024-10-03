import re
from tkinter import Canvas, Tk, Button, Scale, Label, OptionMenu, StringVar, HORIZONTAL
from tkinter import simpledialog as sd

planets = []
radius_scale, edit_tk, holecanvas, restored, line_var = None, None, None, True, None
prev_conditions = [20, "#0ff", [400, 300], None, 40, False]
def scatter_stars(canvas, amount, height, width):
    import random
    for i in range(amount):
        x = random.randint(0, width)
        y = random.randint(0, height)
        canvas.create_rectangle(x, y, x+1, y+1, fill="#ffffff")
def create_circle(canvas, x, y, r, **kwargs):
    return canvas.create_arc(x - r, y - r, x + r, y + r, **kwargs)
class Planet:
    def __init__(self, radius, x, y, fill, canvas, window, goal):
        self.radius = radius
        self.goal = goal
        self.fill = fill
        self.speed = 0
        self.canvas = canvas
        self.id = create_circle(canvas=self.canvas, x=x, y=y, r=self.radius, start=0, extent=359.9999999999999, fill=self.fill, outline=self.fill)
        self.coords = (x, y)
        self.x = x
        self.y = y
        self.window = window
    def avg(self, a, b):
        return (a + b) * 0.5
    def move(self, x, y):
        self.canvas.move(self.id, x, y)
        self.coords = (self.coords[0]+x, self.coords[1]+y)

    def start_animation(self):
        self.speed = 0
        goal = self.goal
        dist_x = goal[0] - self.coords[0]
        dist_y = goal[1] - self.coords[1]

        distance = ((dist_x ** 2) + (dist_y ** 2)) ** 0.5
        speed = min(distance / 100, 5)  # Adjust these values as needed

        self.move_x = (dist_x / distance) * speed
        self.move_y = (dist_y / distance) * speed

        self.animate()  # Start function. homepage.after will continue function.

    def destroy(self):
        self.canvas.delete(self.id)
        self.canvas.update()
        self.canvas.update_idletasks()

    def animate(self):
        # animate function to move the planet thingy
        global prev_conditions
        self.goal = prev_conditions[2]
        goal = self.goal
        dist_x = goal[0] - self.coords[0]
        dist_y = goal[1] - self.coords[1]
        distance = ((dist_x ** 2) + (dist_y ** 2)) ** 0.5 # distances formula

        # Calculate speed based on distance
        max_speed = 20
        min_distance = 50  # Adjust as needed
        if distance < min_distance:
            speed = max_speed
        else:
            speed = max_speed * (min_distance / distance)

        # Normalize movement vector
        if distance != 0:
            move_x = (dist_x / distance) * speed
            move_y = (dist_y / distance) * speed
        else:
            move_x = 0
            move_y = 0

        self.move(move_x, move_y)
        if prev_conditions[5] == "True":
            self.canvas.create_line(self.coords[0]-move_x, self.coords[1]-move_y, self.coords[0], self.coords[1], fill="#ffffff")

        # Check if the planet is close enough to the goal to stop animating
        if distance > 10:  # Threshold to stop
            self.window.after(int(200/prev_conditions[4]), self.animate)
        else:
            self.destroy()

def change_hex(event=None):
    global prev_conditions
    color = None
    match = False
    while color == None or match == False:
        color = sd.askstring("Choose Color", "Enter color hex starting with #")
        match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', str(color))
    prev_conditions[1] = str(color)

def change_goal_pos():
    global prev_conditions
    goal = [None, None]
    match = False
    while goal[0] is None or match is False:
        try:
            x = int(sd.askstring("Black Hole X", "Enter black hole X coordinate"))
            if 0 < x < 800:
                match = True
                goal[0] = x
        except TypeError:
            match = False

    match = False

    while goal[1] is None or match is False:
        try:
            y = int(sd.askstring("Black Hole Y", "Enter black hole Y coordinate"))
            if 0 < y < 600:
                match = True
                goal[1] = y
        except TypeError:
            match = False

    prev_conditions[2] = goal
    create_hole_image()

def scale_lrh():
    global prev_conditions, radius_scale, edit_tk, restored, hole_scale, line_var
    if not restored:
        chosen_radius = radius_scale.get()
        prev_conditions[0] = int(chosen_radius)
        chosen_hole = hole_scale.get()
        prev_conditions[4] = int(chosen_hole)
        create_hole_image()
        prev_conditions[5] = line_var.get()
        print(line_var.get())
    edit_tk.withdraw()

def restore_conditions_default():
    global prev_conditions, restored
    prev_conditions = [20, "#0ff", [400, 300], 40, 40, "False"]
    create_hole_image()
    restored = True

def edit_prev_conditions():
    global prev_conditions, radius_scale, edit_tk, restored, hole_scale, line_var
    restored = False
    edit_tk = Tk()
    edit_tk.title("Change Planet Conditions")
    edit_tk.geometry("550x650")
    edit_tk.configure(background="#000")
    colorchange = Button(edit_tk, text="Change Hex Color Code", command=change_hex, highlightbackground="#000")
    colorchange.pack(pady=25)
    goalsetting = Button(edit_tk, text="Change Black Hole Position", command=change_goal_pos, highlightbackground="#000")
    goalsetting.pack(pady=25)
    radius_scale = Scale(edit_tk, from_=10, to=100, orient=HORIZONTAL)
    radius_scale.configure(highlightbackground="#000", background="#999")
    radius_scale.pack(pady=25)
    radius_label = Label(edit_tk, text="Planet Size (Slider)")
    radius_label.configure(highlightbackground="#000", background="#000")
    radius_label.pack(pady=2)
    hole_scale = Scale(edit_tk, from_=20, to=80, orient=HORIZONTAL)
    hole_scale.configure(highlightbackground="#000", background="#999")
    hole_scale.pack(pady=25)
    hole_label = Label(edit_tk, text="Black Hole Size (Slider)")
    hole_label.configure(highlightbackground="#000", background="#000")
    hole_label.pack(pady=2)
    options = ["False", "True"]
    line_var.set("False")
    line_check = OptionMenu(edit_tk, line_var, *options)
    line_check.update()
    print(line_var.get())
    line_check.configure(highlightbackground="#000", background="#000")
    line_check.pack(pady=25)
    line_label = Label(edit_tk, text="Paths On/Off (Default value is False)", highlightbackground="#000", background="#000")
    line_label.pack(pady=2)
    edit_tk.protocol("WM_DELETE_WINDOW", scale_lrh)
    restore = Button(edit_tk, text="Restore to Defaults", command=restore_conditions_default, highlightbackground="#000")
    restore.pack(pady=25)
    remember = Label(edit_tk, text="Close Window to Save Choices", highlightbackground="#000", background="#000")
    remember.pack(pady=25)

def create_hole_image():
    global holecanvas, prev_conditions
    holecanvas.itemconfig(prev_conditions[3], state='hidden')
    x = prev_conditions[2][0]
    y = prev_conditions[2][1]
    radius = prev_conditions[4]
    prev_conditions[3] = holecanvas.create_oval(x-radius, y-radius, x+radius, y+radius, fill="", outline="#fff")

def add_planet(holecanvas, holepage, event=None):
    global planets, prev_conditions
    x = event.x
    y = event.y
    new_planet = Planet(prev_conditions[0], x, y, prev_conditions[1], holecanvas, holepage, prev_conditions[2])
    planets.append(new_planet)
    new_planet.start_animation()

def stop_game(old_tk, new_tk):
    old_tk.deiconify()
    new_tk.withdraw()

def play_game(old_tk):
    global planets, prev_conditions, holecanvas, line_var
    holepage = Tk()
    holepage.title("Black Hole Simulator")
    line_var = StringVar()
    holecanvas = Canvas(holepage, height=600, width=800, highlightthickness=0, border=0)
    holecanvas.pack()
    old_tk.withdraw()
    holecanvas.create_rectangle(-100, -100, 900, 700, fill="#000000")
    scatter_stars(holecanvas, 75, 600, 800)
    planets = []
    holecanvas.bind("<Button-1>", lambda event: add_planet(holecanvas, holepage, event))
    holepage.protocol("WM_DELETE_WINDOW", lambda :stop_game(old_tk, holepage))
    edit = Button(holepage, text="Edit Conditions", command= lambda: edit_prev_conditions())
    edit.pack()
    label = Label(holepage, text="Click around the screen to spawn planets!\nThe planets get faster as they get closer.\nChanging the size of the black hole will make planets faster.")
    label.pack()
    prev_conditions = [20,
                       "#0ff",
                       [400, 300],
                       holecanvas.create_oval(400 - 40, 300 - 40, 400 + 40, 300 + 40, fill="", outline="#fff"),
                       40,
                       False
                       ]
    while True:
        holecanvas.update()
        holecanvas.update_idletasks()
        holepage.update()
        holepage.update_idletasks()
