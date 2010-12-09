#Submit test results to litmus automatically

import sys
import os
import httplib
import urllib
import time
import platform

def set_test_id(test_id):
    tid = test_id.split()
    s = str(tid[0]).strip(">,<,[,]")
    L = s.split('_')
    testid = L.pop()
    print testid
    return testid


def set_status(stat):
    print stat
    if stat == ".":
        status = "pass"
    else:
        status = "fail"
    return status



def set_litmus_os(test_os):
    """Returns the os string for the SUT

    """
    if str(test_os) == "osx":
        v, _, _ = platform.mac_ver()
        v = str('.'.join(v.split('.')[:2]))
        lit_os = ["OS X", v]
        return lit_os
    elif str(test_os) == "win":
        v = platform.release()
        lit_os = ["Windows", v]
        return lit_os
    else:
        print ("I don't know how to handle platform '%s'", test_os)


def set_buildid():
    buildid = time.strftime("%Y%m%d", time.gmtime()) + "99"
    buildid = "2010112900" #set custom build id here.
    return buildid


HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<litmusresults action="submit" useragent="UberSikuliAgent/1.0 (machine foobar)" machinename="sikuli_machine">
   <testresults
   username="pcf.subwriter@gmail.com"
   authtoken="autotester"
   product="Miro"
   platform="%(opsys)s"
   opsys="%(platform)s"  
   branch="git-Master"
   buildid="%(buildid)s"
   locale="en-US"
   >
"""

STORY = """<result testid="%(testid)s"
        is_automated_result="0"
        resultstatus="%(status)s"
        exitstatus="0"
        timestamp="%(timestamp)s"
        >
         <comment><![CDATA[
         %(error_msg)s
         ]]>
         </comment>
       </result>
"""

FOOTER = """</testresults>
</litmusresults>
"""

def write_header(test_os):
    f = open("log.xml",'w')
    f.write(HEADER % {"buildid": set_buildid(),
                      "opsys": set_litmus_os(test_os)[0],
                      "platform": set_litmus_os(test_os)[1]
                      })
    f.close
    


def write_log(testid,stat,error_info=""):
    f = open("log.xml", 'a')
 
    
    f.write(STORY % {"testid": set_test_id(testid),
                     "status": set_status(stat),
                     "timestamp": time.strftime("%Y%m%d%H%M%S", time.gmtime()),
                     "error_msg": error_info.lstrip('.')
                         })
    f.close

def write_footer():
    f = open("log.xml", 'a')
    f.write(FOOTER)
    f.close


def send_result(fn):
    f = open(fn)
    log_data = f.read()
    params = urllib.urlencode({'data':log_data,                               
                                })
    headers = {"Content-type": "application/x-www-form-urlencoded",
               "Accept": "text/plain"}
    conn = httplib.HTTPConnection("litmus.pculture.org")

    print "sending test result..."
    conn.request("POST", "/process_test.cgi", params, headers)
    response = conn.getresponse()
    data = response.read()
    print data
    conn.close()
    f.close()


if __name__ == "__main__":
    write_header("osx")
    #send_result()

