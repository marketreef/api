import marketreef

# Make sure you enter your username and password below.
# Registering now at http://www.marketreef.co will get you
# 100 free API queries.
client = MarketReef("USERNAME", "PASSWORD")

# EXAMPLE 1
name = 'portfolio_performance'
data = {'p':'XHB'} # Latest performance on Homebuilders ETF
report = client.report(name, data)

print report['title']
print report['text']
print

# EXAMPLE 2
name = 'portfolio_performance'

data = [{'p':'XLK'}, # Latest performance on the Tech, 
        {'p':'XLF'}, # Financials 
        {'p':'XLV'}] # and Health Care Sectors

report = client.report(name, data)

for report in reports:
    print report['title']	
    print report['text']
    print


# EXAMPLE 3
name = 'portfolio_performance'
data = {'p':'AAPL 20%, KO 20%, GOOG 15%, BRK-B 15%, XHB 10%, CMCSA 5%, FB 5%, ZNGA 5%, LNKD 5%', # My custom portfolio
        's':"2012-12-31"} # Performance YTD

report = client.report(name, data)

for report in reports:
    print report['title']	
    print report['text']
    print
