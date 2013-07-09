import requests
import os
import threading
import Queue

class ReportThread(threading.Thread):
    def __init__(self, report_url, login_cookies, 
                 data_queue, report_queue):
        threading.Thread.__init__(self)
        self.report = report_url
        self.cookies = login_cookies
        self.data = data_queue
        self.output = report_queue
    def run(self):
        while True:
            data = self.data.get()
            try:
                r = requests.post(self.report, cookies=self.cookies, 
                                  data=data, timeout = 5)

                self.output.put(r)
            except:
                print "ERROR! %s" % (data)
            self.data.task_done()

class MarketReef(object):
    '''
    '''
    def __init__(self, username = None, password = None, 
                 url=''):
        '''
        '''
        if not url:
            self.url = 'http://api.marketreef.co/'
        else:
            self.url = url
        self.login_ext = 'login'
        if username and password:
            self.login(username, password)

    def login(self, username, password):
        '''Login method.'''
        client = requests.session()
        client.get(self.url)
        data = dict(username=username, password=password)
        r = client.post(self.url + self.login_ext, data=data)
        self.cookies = dict(sessionid=r.cookies['sessionid'])

    def report(self, name, data):
        '''Reporting method'''
        report = self.url + name
        if type(data) != list:
            # Single Report Request
            r = requests.post(report, cookies=self.cookies, data=data)
            return r
        else:
            # Multiple Reports Requested
            data_queue = Queue.Queue()
            output_queue = Queue.Queue()

            threads = min(len(data), 5)

            for x in range(threads):
                t = ReportThread(report, self.cookies, 
                                 data_queue, output_queue)
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
        
