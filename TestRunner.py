#Test Runner making use of the XmlTestRunner by by Sebastian Rittau <srittau@jroger.in-berlin.de>

import sys
import unittest
import xmlrunner



class TestRunner(unittest.TestCase):
    def __init__(self, suiteclass):
        print sys.argv
        if len(sys.argv) > 1:
            args = sys.argv[1:]
            self.suite = unittest.TestSuite()
            for x in args:
                self.suite.addTest(suiteclass(x))
        else:
            self.suite = unittest.TestLoader().loadTestsFromTestCase(suiteclass)
        self.suitename = sys.argv[0].split('.sikuli')[0]
                    
    def run_tests(self):
        r = xmlrunner.XMLTestRunner()
        r.run(self.suite, self.suitename)


