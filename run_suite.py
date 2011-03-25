import os
import time
import glob
import sys
import subprocess

sys.path.append(os.path.join(os.getcwd(),'myLib'))



from optparse import OptionParser
parser = OptionParser()
parser.add_option("-q", "--quicktest", action="store_true", dest="quicktest", default=False,
                  help='Runs the quicktest suite')



(options, args) = parser.parse_args()
qt = options.quicktest

###Run all the subgroups:

if sys.platform.startswith("darwin"):
    if os.getenv("PCF_TEST_HOME") == None:
        raw_input("Must set PCF_TEST_HOME env to current dir, press key to exit")
else:
    os.putenv("PCF_TEST_HOME",os.getcwd())


if os.getenv("SIKULI_HOME") == None:
    raw_input("Must set SIKULI_HOME environment var to dir containing sikuli-script.jar \
              Press any key to exit")

jar_path = os.path.join(os.getenv("SIKULI_HOME"),"sikuli-script.jar")
sik_run_cmd = ['java', '-jar', jar_path]


for subgroup in glob.glob(os.path.join(os.getcwd(), '*.sikuli')):
    print subgroup
    sik_run_cmd.append(subgroup)
    p = subprocess.Popen(sik_run_cmd).communicate()
    


#To run just one test:
##os.system("java -jar $SIKULI_HOME/sikuli-script.jar test.sikuli Miro_Suite.test_x")

    


