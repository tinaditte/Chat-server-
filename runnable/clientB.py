from tkinter import Tk

from GUI import LandingGUI

def clientB():
    master = Tk()
    LandingGUI.GUI(master)
    master.mainloop()

clientB()