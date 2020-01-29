from tkinter import Tk
from GUI import LandingGUI


def clientk():
    master = Tk()
    LandingGUI.GUI(master)
    master.mainloop()

clientk()