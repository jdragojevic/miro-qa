import os
import time
import glob
import sys
import subprocess
import shutil
import re

from optparse import OptionParser
parser = OptionParser()
parser.add_option("-q", "--quicktest", action="store_true", dest="quicktest", default=False,
                  help='Runs the quicktest suite')

(options, args) = parser.parse_args()
qt = options.quicktest

##if sys.platform.startswith("darwin"):
os.putenv("MACOSX_DEPLOYMENT_TARGET","10.5")
if os.getenv("PCF_TEST_HOME") == None:
    raw_input("Must set PCF_TEST_HOME env to current dir, press key to exit")
##else:
##    os.putenv("PCF_TEST_HOME",os.getcwd())


if os.getenv("SIKULI_HOME") == None:
    raw_input("Must set SIKULI_HOME environment var to dir containing sikuli-script.jar \
              Press any key to exit")


JAR_PATH = os.path.join(os.getenv("SIKULI_HOME"),"sikuli-script.jar")
RESULTS_DIR = os.path.join(os.getenv("PCF_TEST_HOME"), "Miro", "last_run")
QUICK_TESTS = [['sg11_torrents.sikuli', 'test_419', 'test_719'],
               ['sg2_search.sikuli', 'test_82'],
               ['sg19_system.sikuli', 'test_55'],
               ['sg_21_sites.sikuli', 'test_182', 'test_143'],
               ['sg24_shortcuts.sikuli', 'test_92'],
               ['sg31_playback.sikuli', 'test_160'],
               ['sg11_torrents.sikuli', 'test_001setup'],
               ['sg42_feedsearch.sikuli', 'test_720'],
               ['sg58_items.sikuli', 'test_361'],
               ['sg6_feeds.sikuli', 'test_338', 'test_117'],
    ]


def _clear_out_the_old_results():
    for f in glob.glob(os.path.join(RESULTS_DIR, '*.xml')):
       os.unlink(f)

def count_results(status):
    STAT_STRING = 'resultstatus=\"%s' % status
    STAT_COUNT = 0
    for f in glob.glob(os.path.join(RESULTS_DIR, '*.xml')):
        result = os.path.expandvars(f)
        rez = open(result, 'r')
        count = len(re.findall (STAT_STRING, rez.read()))
        STAT_COUNT += count
    return STAT_COUNT
        

def check_the_results():
    total_pass = count_results(status="pass")
    total_fail = count_results(status="fail")
    print """Test run complete:
             %(#pass)d passing tests 
             %(#fail)d failing tests""" \
               % {"#pass": total_pass, "#fail": total_fail}


def _run_the_quicktests():
    """Only run the quicktest suite.

    #To run just one test:
    #java -jar "$SIKULI_HOME/sikuli-script.jar" sg_xx_xxx.sikuli test_x test_y ...")
    """
    for tests in QUICK_TESTS:
        sik_run_cmd = ['java', '-jar', JAR_PATH]
        for x in tests:
            sik_run_cmd.append(x)
            print "running... ",tests
        print sik_run_cmd
        p = subprocess.Popen(sik_run_cmd).communicate()

def _run_the_full_suite():
    """Runs all the subgroups.

    java -jar $SIKULI_HOME/sikuli-script.jar sgxx_xxx.sikuli"
    """

    #get all the tests in the directory and make a list
    sglist = []
    alltests = glob.glob(os.path.join(os.getcwd(), '*.sikuli'))
    for x in alltests:
        sglist.append(os.path.basename(x))
    #sort the list, then drop subgroup_1 and subgroup 89 install tests to the back of the list.
    sglist.sort()
    sg1index = sglist.index('sg1_install.sikuli')
    sg1 = sglist.pop(int(sg1index))
    sglist.append(sg1)
    sg89index = sglist.index('sg89_prefs.sikuli')
    sg89 = sglist.pop(int(sg89index))
    sglist.append(sg89)

    for subgroup in sglist:
        jar_path = os.path.join(os.getenv("SIKULI_HOME"),"sikuli-script.jar")
        sik_run_cmd = ['java', '-jar', jar_path]
        sik_run_cmd.append(subgroup)
        p = subprocess.Popen(sik_run_cmd).communicate()
    



try:
    #Clear out old results before executing tests
    _clear_out_the_old_results()
    print "testing_results"
    if qt == True:
        _run_the_quicktests()
    else:
        _run_the_full_suite()

finally:
    check_the_results()

    
    







