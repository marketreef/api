# Market Reef API Module

Sample code:

import marketreef
client = MarketReef("USERNAME", "PASSWORD")


name = 'portfolio_performance'
data = {'p':'XHB'} #Latest performance on Homebuilders
report = client.report(name, data)

print report['title']
print report['text']



name = 'portfolio_performance'
data = [{'p':'XLK'}, # Latest performance on the Tech, 
        {'p':'XLF'}, # Financials 
        {'p':'XLV'}] # and Health Care Sectors
report = client.report(name, data)

for report in reports:
    print report['title']	
    print report['text']



name = 'portfolio_performance'
data = {'p':'AAPL 20%, KO 20%, GOOG 15%, BRK-B 15%, XHB 10%, CMCSA 5%, FB 5%, ZNGA 5%, LNKD 5%', 
        's':"2012-12-31"} # My personal portfolio YTD
report = client.report(name, data)

for report in reports:
    print report['title']	
    print report['text']

##For details on the valid arguments for portfolio performance, check out http://www.marketreef.co/api/docs