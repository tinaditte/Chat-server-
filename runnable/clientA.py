from tkinter import Tk
from GUI import LandingGUI


def clientA():
    master = Tk()
    LandingGUI.GUI(master)
    master.mainloop()

clientA()