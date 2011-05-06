import sys
import os
import unittest
import httplib
import urllib
import time
import platform
import StringIO

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
    logfile = "Log5027.xml"
    send_result(logfile)




