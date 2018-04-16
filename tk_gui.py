"""This module contains code from
Think Python by Allen B. Downey
http://thinkpython.com

Copyright 2012 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html

"""

from rtu_conf.swampy.TurtleWorld import *
from rtu_conf.swampy.World import Interpreter

from rtu_conf.swampy.Gui import *


from rtu_conf.serial_cmm import *


class SimpleTurtleWorld(TurtleWorld):
    """An environment for Turtles and TurtleControls.

    This class is similar to TurtleWorld, but the code that
    lays out the GUI is simplified for explanatory purposes.
    """

    def setup(self):
        """create the GUI"""


        self.row()

        self.canvas = self.ca(width=400, height=400, bg='white')

        # right frame
        self.col()

        # buttons
        self.gr(cols=2)
        self.bu(text='Print canvas', command=self.canvas.dump)
        self.bu(text='Quit', command=self.quit)
        self.bu(text='Make Turtle', command=self.make_turtle)
        self.bu(text='Clear', command=self.clear)
        self.endgr()


        # run file
        self.row([0,1], pady=30)
        self.bu(text='Run file', command=self.run_file)
        self.en_file = self.en(text='snowflake.py', width=5)
        self.endrow()

        # run this code
        self.te_code = self.te(width=25, height=10)
        self.te_code.insert(END, 'world.clear()\n')
        self.te_code.insert(END, 'bob = Turtle(world)\n')

        self.bu(text='Run code', command=self.run_text)

        # leave the column open to accomodate Turtle control panels
        #self.endcol()
class Rtu_gui(TurtleWorld):
    """An environment for Turtles and TurtleControls.

    This class is similar to TurtleWorld, but the code that
    lays out the GUI is simplified for explanatory purposes.
    """

    def setup(self):
        """create the GUI"""
        ava_list_name = SER_Get_available_com_name()
        ava_seq = [ str(i) for i in range(len(ava_list_name))]
        com_opts = dict(zip(ava_seq, ava_list_name))
        self.row()

        self.canvas = self.ca(width=400, height=400, bg='white')

        # right frame
        self.col()

        # buttons
        self.gr(cols=2)
        #self.bu(text='串口', command=self.canvas.dump)
        #self.bu(text='Quit', command=self.quit)
        #self.bu(text='Make Turtle', command=self.make_turtle)
        #self.bu(text='Clear', command=self.clear)
        #self.endgr()
        print(com_opts)
        fuck = 1
        eat = 2
        self.mb(fuck='you', eat='shit')

        # run file
        self.row([0,1], pady=30)
        self.bu(text='Run file', command=self.run_file)
        self.en_file = self.en(text='snowflake.py', width=5)
        self.endrow()

        # run this code
        self.te_code = self.te(width=25, height=10)
        self.te_code.insert(END, 'world.clear()\n')
        self.te_code.insert(END, 'bob = Turtle(world)\n')

        self.bu(text='Run code', command=self.run_text)

        # leave the column open to accomodate Turtle control panels
        #self.endcol()

if __name__ == '__main__':
    world = Rtu_gui()
    world.inter = Interpreter(world, globals())
    world.mainloop()
