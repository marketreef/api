import urllib
import urllib2
import json
import cookielib
import threading
import Queue

class MarketReef(object):
    '''
    Market Reef API client object.
    '''
    def __init__(self, username, password, 
                 url=''):
        '''
        Construct client by supplying your username and password.
        '''
        if not url:
            self.url = 'http://api.marketreef.co/'
        else:
            self.url = url
        self.login_ext = 'login'
        if username and password:
            try:
                self._login(username, password)
            except:
                raise Exception("Failed to login")

    def _login(self, username, password):
        cj = cookielib.CookieJar()
        cookiehandler = urllib2.HTTPCookieProcessor(cj)
        opener = urllib2.build_opener(cookiehandler)
        
        data = "username=%s&password=%s" % (username,
                                            password)

        r = opener.open(self.url + self.login_ext,
                        data, 5).read()

        assert r == "Logged In"
        
        urllib2.install_opener(opener)
            
    def report(self, name, data):
        '''
        The 'report' method takes two arguments:
        'name' refers to the name of the report. "portfolio_performace" is
        the only supported report at this point.

        The 'data' argument takes in a dictionary with the information to
        build the report from. See http://www.marketreef.co/api/docs for
        information on the arguments accepted. 

        The 'data' argument also accepts a list of valid data objects. We
        recommend using this method instead of calling the 'report' method
        multiple times to generate reports individually it provides
        significantly faster results. Billing is not affected either way.

        The method returns a dictionary or list of dictionaries containing
        the rendered reports. See documentation for specific fields.
        '''
        report = self.url + name
        if type(data) != list:
            # Single Report Request
            if type(data) == dict:
                data = urllib.urlencode(data)
            r = urllib2.urlopen(report, data)
            r = json.load(r)
            return r
        else:
            # Multiple Reports Requested
            data_queue = Queue.Queue()
            output_queue = Queue.Queue()

            threads = min(len(data), 5)

            for x in range(threads):
                t = _ReportThread(report, data_queue, output_queue)
                t.setDaemon(True)
                t.start()
            
            for d in data:
                data_queue.put(d)
            
            data_queue.join()
        
            # Returns the reports as a List, not a Queue
            output = []
            for x in range(output_queue.qsize()):
                output.append(output_queue.get())

            return output
        
class _ReportThread(threading.Thread):
    '''
    INTERNAL USE
    Thread for a single query.
    '''
    def __init__(self, report_url, data_queue, report_queue):
        '''
        Constructor sets the authentication url, cookies, input and 
        output queues.
        '''
        threading.Thread.__init__(self)
        self.report = report_url
        self.data = data_queue
        self.output = report_queue

    def run(self):
        '''
        Actual process, grabs jobs from input queue, renders report, then
        puts to the output queue.
        '''
        while True:
            data = self.data.get()
            try:
                if type(data) == dict:
                    data = urllib.urlencode(data)
                r = urllib2.urlopen(self.report, data, 5)
                r = json.load(r)

                self.output.put(r)
            except:
                print "ERROR! %s" % (data)
            self.data.task_done()

if __name__ == "__main__":
    import os
    client = MarketReef(os.environ['API_USER'], os.environ['API_PWD'])
    data = [{'p':'XLK 20.79%, XLF 16.60%, XLV 12.63%, XLY 12.30%, XLE 10.56%, XLP 10.49%, XLI 10.10%, XLB 3.27%, XLU 3.25%'},
            {'p':'XLK'},
            {'p':'XLF'},
            {'p':'XLV'},
            {'p':'XLY'},
            {'p':'XLE'},
            {'p':'XLP'},
            {'p':'XLI'},
            {'p':'XLB'},
            {'p':'XLU'},
        ]
    reports = client.report('portfolio_performance', data)
    
    for r in reports:
        if r['meta']['status'] == '200':
            print r['title']
            print
            print r['text']
            print
            print r['tweet']
            print
            print
                
