import os
import time
import glob
import sys
import subprocess


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


QUICK_TESTS = [['sg11_torrents.sikuli', 'test_419', 'test_719'],
               ['sg2_search.sikuli', 'test_82'],
               ['sg19_system.sikuli', 'test_55'],
               ['sg_21_sites.sikuli', 'test_182', 'test_143'],
               ['sg24_shortcuts.sikuli', 'test_92'],
               ['sg31_playback.sikuli', 'test_160'],
               ['sg42_feedsearch.sikuli', 'test_720'],
               ['sg58_items.sikuli', 'test_361'],
               ['sg6_feeds.sikuli', 'test_338', 'test_117'],
               ['sg1_install.sikuli', 'test_4']
    ]


jar_path = os.path.join(os.getenv("SIKULI_HOME"),"sikuli-script.jar")
if qt == True:
    # runs the quicktest suite
    #To run just one test:
    #java -jar "$SIKULI_HOME/sikuli-script.jar" sg_xx_xxx.sikuli test_x test_y ...")
    for tests in QUICK_TESTS:
        sik_run_cmd = ['java', '-jar', jar_path]
        for x in tests:
            sik_run_cmd.append(x)
            print "running... ",tests
        print sik_run_cmd
        p = subprocess.Popen(sik_run_cmd).communicate()
else:
    #get all the tests in the directory and make a list
    sglist = []
    alltests = glob.glob(os.path.join(os.getcwd(), '*.sikuli'))
    for x in alltests:
        sglist.append(os.path.basename(x))
    #sort the list, then drop subgroup_1 install tests to the back of the list.
    sglist.sort()
    sg1index = sglist.index('sg1_install.sikuli')
    sg1 = sglist.pop(int(sg1index))
    sglist.append(sg1)
      
    #Run all the subgroups:
    #To run all the tests in 1 subgroup:
    #java -jar $SIKULI_HOME/sikuli-script.jar sgxx_xxx.sikuli"
    for subgroup in sglist:
        jar_path = os.path.join(os.getenv("SIKULI_HOME"),"sikuli-script.jar")
        sik_run_cmd = ['java', '-jar', jar_path]
        sik_run_cmd.append(subgroup)
        p = subprocess.Popen(sik_run_cmd).communicate()
        


    


