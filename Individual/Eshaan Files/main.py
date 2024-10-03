# Black Hole Simulation
# Created by Eshaan Buddhisagar: YoungWonks Hackathon September 2024 Thematic Project Round 2

from otherfiles.game import *
def get_x_y(event):
    global x, y, last_event
    try:
        (x, y) = (event.x, event.y)
    except AttributeError:
        (x, y) = (last_event.x, last_event.y)
    except:
        return False
    else:
        last_event = event
        return True
x, y = 0, 0
class LastEvent:
    def __init__(self):
        self.x = 0
        self.y = 0
last_event = LastEvent()
homepage = Tk()
homepage.title("Black Hole Homepage")
black = "#000000"
homecanvas = Canvas(homepage, width=500, height=500, highlightthickness=0, borderwidth=0)
homecanvas.pack()
homecanvas.create_rectangle(-100, -100, 700, 600, fill=black)
scatter_stars(homecanvas, 50, 600, 500)
homecanvas.create_rectangle(50, 100, 450, 200, fill="#ffffff")
homecanvas.create_rectangle(50, 300, 450, 400, fill="#ffffff")
homecanvas.create_text(100, 150, text="Play", font=("Arial", 30), fill="#000")
homecanvas.create_text(100, 350, text="Quit", font=("Arial", 30), fill="#000")
homecanvas.bind("<Motion>", lambda event: get_x_y(event))
authorization = Label(homepage, text="Made by Eshaan Buddhisagar 2024.")
authorization.pack()
def check_game(event=None, old_tk=None):
    global x, y
    get_x_y(None)
    if x > 50 and y > 100 and x < 450 and y < 200:
        play_game(old_tk)
    if x > 50 and y > 350 and x < 450 and y < 450:
        print("Qutting the simulator... please wait: 0 seconds.")
        quit()
homecanvas.bind("<Button-1>", lambda event: check_game(event=event, old_tk=homepage))
homepage.update_idletasks()
homepage.mainloop()
