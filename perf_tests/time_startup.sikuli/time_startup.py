import sys
import os
import glob
import unittest
import StringIO
import time


class Miro_Suite(unittest.TestCase):
    """Subgroup startup - time startup.

    """
      

    def test_time_startup(self):
        """http://litmus.pculture.org/show_test.cgi?id=000 startup_miro timing.

        Startup miro and capture the startup time.
        

        """
        time.sleep(3)
        times = []
        for x in range(0,9):
            a = time.clock()
            App.open("C:\\Program Files\\Participatory Culture Foundation\\Miro\\Miro.exe")
            wait(Pattern("40_top_left.png"),10)
#            wait(Pattern("351_top_left.png"),10)
            starttime = time.clock() -a
            print "Run time: ",starttime, " seconds"
            click(getLastMatch())
            time.sleep(2)
            type('q',KEY_CTRL)
            times.append(starttime)
            time.sleep(5)
        average = float(sum(times)) / len(times)
        print average

if __name__ == "__main__":
    unittest.main()
