Market Reef API Module

Sample code:

import marketreef
client = MarketReef("USERNAME", "PASSWORD")


# Latest performance on Homebuilders
name = 'portfolio_performance'
data = {'p':'XHB'}
report = client.report(name, data)

print report['title']
print report['text']


# Latest performance on the Tech, Financials and Health Care Sectors
name = 'portfolio_performance'
data = [{'p':'XLK'},
        {'p':'XLF'},
        {'p':'XLV'}]
report = client.report(name, data)

for report in reports:
    print report['title']	
    print report['text']

# By personal portfolio YTD
name = 'portfolio_performance'
data = {'p':'AAPL 20%, KO 20%, GOOG 15%, BRK-B 15%, XHB 10%, CMCSA 5%, FB 5%, ZNGA 5%, LNKD 5%', 's':"2012-12-31"}
report = client.report(name, data)

for report in reports:
    print report['title']	
    print report['text']