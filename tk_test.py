from tkinter import *

def hello():
    print("hello!")

class Application(Tk):
    def createWidgets(self):
       self.menuBar = Menu(master=self)
       self.filemenu = Menu(self.menuBar, tearoff=0)
       self.filemenu.add_command(label="Hello!", command=hello)
       self.filemenu.add_command(label="Quit!", command=self.quit)
       self.menuBar.add_cascade(label="File", menu=self.filemenu)

    def __init__(self):
       Tk.__init__(self)
       self.createWidgets()
       self.config(menu=self.menuBar)

if __name__ == "__main__":
    ui = Application()
    ui.mainloop()