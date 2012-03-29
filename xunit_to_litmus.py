from lxml import etree
import os
import glob
import httplib
import urllib



class ProcessResults():
    RESULTS_DIR = os.path.join(os.getenv("PCF_TEST_HOME"), "Miro", "Results")
    def to_litmus_xml(self):
#        o = open(output_xml, 'w')
                          
        root = etree.Element("litmusresults")
        root.set("action", "submit")
        root.set("useragent", "UberSikuliAgent/1.0 (machine foobar)")
        root.set("machinename", "sikuli_machine")
        
        results = etree.Element("testresults")
        results.set("username", "jed@pculture.org")
        results.set("authtoken", "sik-machine")
        results.set("product", "Miro")
        results.set("platform", "Windows")
        results.set("opsys", "Vista")
        results.set("branch", "git-Master")
        results.set("buildid", "2012032002")
        results.set("locale", "en-US")

        for f in glob.glob(os.path.join(self.RESULTS_DIR, '*.xml')):
            print f
            curr_xunit = etree.parse(f)
            rroot = curr_xunit.getroot()
            for element in rroot.iter("testcase"):
                tc = element.attrib["name"].split('_')[-1]
                if tc == "001setup" or tc == "999reset":
                    continue
                timestamp = element.attrib["time"]
                err_msg = None
                if not element.find("error") == None:
                    status = "fail"
                    err_msg = element.findtext("error")
                elif not element.find("failure") == None:
                    status = "fail"
                    err_msg = element.findtext("failure")
                else:
                    status = "pass"
                result_element = etree.Element("result",
                                           testid=tc,
                                           is_automated_result="0",
                                           resultstatus=status,
                                           exitstatus="0",
                                           timestamp=timestamp,
                                           )
                comment = etree.Element("comment")
                if not err_msg == None:
                    comment.text = etree.CDATA(err_msg)
                    result_element.append(comment)
                results.append(result_element)
            root.append(results)
        litmus_log = etree.tostring(root, encoding=unicode)
        print(etree.tostring(root, pretty_print=True, encoding=unicode))
        return litmus_log


    def send_result(self, litmus_results):
        params = urllib.urlencode({'data':litmus_results,                               
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

if __name__ == "__main__":
    p = ProcessResults()
    test_run_results = p.to_litmus_xml()
    p.send_result(test_run_results)

    

                      
