import urllib
import urllib2
import json
import cookielib
import threading
import Queue

DESCRIPTION = '''
              Market Reef API client.

              For more information check out www.marketreef.co/api/docs.
              '''
class MarketReef(object):
    DESCRIPTION
    def __init__(self, key = '', username = '',
                 password = '', url=''):
        '''
        Construct client by supplying your address key 
        (http://www.marketreef.co/api/dashboard) 
        OR your username and password.
        '''
        self.key = key
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
                        data).read()

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
            # Single Report Reques
            if self.key:
                data['key'] = self.key
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
            
            count = 0
            for d in data:
                d['n'] = count
                if self.key:
                    d['key'] = self.key
                data_queue.put(d)
                count += 1
            
            data_queue.join()
        
            # Returns the reports as a List, not a Queue
            output = []
            for x in range(output_queue.qsize()):
                output.append(output_queue.get())

            output.sort(key=lambda x: x['meta']['n'])

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
                r = urllib2.urlopen(self.report, data)
                r = json.load(r)

                self.output.put(r)
            except:
                print "ERROR! %s" % (data)
            self.data.task_done()

if __name__ == "__main__":
    import os
    import json
    import argparse
    import ast
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('-p', help='Pretty pring option.',
                        action="store_true")
    parser.add_argument('--report', type=str, default='portfolio_performance',
                        help='Report of choice. Defaults for Portfolio Performance')
    parser.add_argument('-data', type=str, nargs="+",
                        help='JSON input data. Overrides every other data input.')
    parser.add_argument('-portfolios', type=str, nargs='+',
                        help='The portfolio variable can be a ETF ticker or a list of comma-separated ticker-share pairs. See www.marketreef.co/api/docs for details and examples.')
    parser.add_argument('-s', metavar='START', type=str, default='',
                        help='ISO-formatted start date of reporting period.')
    parser.add_argument('-f', metavar='FINISH', type=str, default='',
                        help='ISO-formatted finish date of reporting period.')
    parser.add_argument('-key', type=str, default='',
                        help='ISO-formatted start date of reporting period.')
    parser.add_argument('--filter', type=str, nargs='+',
                        help='Selects sub-items from the report objects. Note that using the filter causes reports that returned a status other than 200 to be scrapped without notice and therefore should not be used for production.')

    args = parser.parse_args()

    if args.data:
        data = [ast.literal_eval(x) for x in args.data]
    else:
        data = []
        for p in args.portfolios:
            data.append({'p': p,
                         's': args.s,
                         'f': args.f,})
    
    if args.key:
        key = args.key
    elif os.environ.get('MARKETREEF_KEY', ''):
        key = os.environ['MARKETREEF_KEY']
    else:
        print "Please provide a key. See -h for details."
        exit()

    client = MarketReef(key=key)

    report = client.report(args.report, data)
    
    if args.filter:
        report = [x for x in report if x['meta']['status'] == '200']
        for f in args.filter:
            report = [x[f] for x in report]

    if args.p:
        print json.dumps(report, indent=4, separators=(',', ': '))
    else:
        print json.dumps(report)

    
