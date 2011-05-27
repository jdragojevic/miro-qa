import sys
import os
import unittest
import httplib
import urllib
import time
import platform
import StringIO



def find_logs():
    log_list = []
    miro_dir = os.path.join(os.getenv("PCF_TEST_HOME"),"Miro")
    log_dir = os.path.join(miro_dir,"last_run")
    for x in os.listdir(log_dir):
        try:
            log = os.path.join(log_dir,x)
            send_result(log)
        except:
            print "log: " +x+" not sent."
    



def send_result(log):
    f = open(log)
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
    find_logs()




