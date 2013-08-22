from marketreef import MarketReef

def basic(key):
    # Make sure you enter your address key.
    # Registering now at http://www.marketreef.co will get you
    # 100 free API queries.
    client = MarketReef(key)
    
    # EXAMPLE 1
    name = 'portfolio_performance'
    data = {'p':'XHB'} # Latest performance on Homebuilders ETF
    report = client.report(name, data)

    if report['meta']['status'] == '200':
        print report['title']
        print report['text']
        print
    else:
        print report['meta']['msg']

    # EXAMPLE 2
    name = 'portfolio_performance'

    data = [{'p':'XLK'}, # Latest performance on the Tech, 
            {'p':'XLF'}, # Financials 
            {'p':'XLV'}] # and Health Care Sectors

    reports = client.report(name, data)

    for report in reports:
        print report['title']	
        print report['text']
        print


    # EXAMPLE 3
    name = 'portfolio_performance'
    data = {'p':'AAPL 20, KO 20, GOOG 15, BRK-B 15, XHB 10, CMCSA 5, FB 5, ZNGA 5, LNKD 5', # My custom portfolio
            's':"2013-01-01"} # Performance YTD

    report = client.report(name, data)

    print report['title']	
    print report['text']
    print

def sector_performance(key):
    client = MarketReef(key)

    name = 'portfolio_performance'
    data = [{'p':'SPY'},
            {'p':'XLK'},
            {'p':'XLF'},
            {'p':'XLV'},
            {'p':'XLY'},
            {'p':'XLE'},
            {'p':'XLP'},
            {'p':'XLI'},
            {'p':'XLB'},
            {'p':'XLU'}]

    reports = client.report(name, data)

    for report in reports:
        if report['meta']['status'] == '200':
            print report['title']	
            print report['text']
            print
        else:
            print "Failed %s: %s" % (report['meta']['_POST'], 
                                     report['meta']['msg'])
            print
