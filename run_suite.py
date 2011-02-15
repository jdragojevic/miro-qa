import os
import time
import glob
import sys
import subprocess

sys.path.append(os.path.join(os.getcwd(),'myLib'))

import litmusresult






###Run all the subgroups:

if sys.platform.startswith("darwin"):
    if os.getenv("SIKULI_TEST_HOME") == None:
        raw_input("Must set SIKULI_TEST_HOME env to current dir, press key to exit")

if os.getenv("SikHome") == None:
    raw_input("Must set SikHome environment var to dir containing sikuli-script.jar \
              Press any key to exit")

jar_path = os.path.join(os.getenv("SikHome"),"sikuli-script.jar")
sik_run_cmd = ['java', '-jar', jar_path]

for subgroup in glob.glob(os.path.join(os.getcwd(), '*.sikuli')):
    print subgroup
    sik_run_cmd.append(subgroup)
    p = subprocess.Popen(sik_run_cmd).communicate()

##litmusresult.send_result(fn=os.path.join(os.path.dirname(os.getcwd()),"log.xml"))
        


#To run just one test:
##os.system("java -jar $SikHome/sikuli-script.jar test.sikuli")

    


