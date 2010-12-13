import os
import time
import glob
import sys

sys.path.append(os.path.join(os.getcwd(),'myLib'))

import litmusresult
                 
###Run all the subgroups:
##for subgroup in glob.glob(os.path.join(os.getcwd(), '*.sikuli')):
##    print subgroup
##    os.system("cd ../; java -d32 -Dpython.path=Lib/ -jar sikuli-script.jar "+ subgroup)
##    litmusresult.send_result(fn=os.path.join(os.path.dirname(os.getcwd()),"log.xml"))
        


#To run just one test:
os.system("cd ../; java -d32 -Dpython.path=Lib/ -jar sikuli-script.jar Miro/sg72_conversions.sikuli")
