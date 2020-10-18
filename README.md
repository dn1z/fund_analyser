# fund_analyser
A script that provides plotting functions for prices and yields of funds in [tefas.gov.tr](https://tefas.gov.tr)

## Installation
```
pip install -r requirements.txt
python setup.py install
```

## Usage
* As a command line script
```
usage: fund_analyser plot [-h] [-c] [-t [TICKERS [TICKERS ...]]] (-m MONTHS | -d DAYS | -w WEEKS | -y YEARS) funds [funds ...]
usage: fund_analyser table [-h] [-t [TICKERS [TICKERS ...]]] (-m MONTHS | -d DAYS | -w WEEKS | -y YEARS) funds [funds ...]
usage: fund_analyser hist [-h] [-t [TICKERS [TICKERS ...]]] (-m MONTHS | -d DAYS | -w WEEKS | -y YEARS) funds [funds ...]

positional arguments:
  funds                 Takas codes of funds

optional arguments:
  -h, --help            show this help message and exit
  -c, --compare         Compare funds and tickers
  -t [TICKERS [TICKERS ...]], --tickers [TICKERS [TICKERS ...]]
                        Symbol of tickers (Yahoo! Finance)
  -m MONTHS, --months MONTHS
  -d DAYS, --days DAYS
  -w WEEKS, --weeks WEEKS
  -y YEARS, --years YEARS
```
* As a library
```python
from fund_analyser import FundAnalyser

a = FundAnalyser()

a.plot('AAA').weeks(1)  # plots last weeks performance of the fund
a.plot('BBB', 'CCC').months(2)  # plots multiple funds
a.plot('DDD', tickers=['USDTRY=X']).years(3)  # plots a ticker with fund
a.plot('EEE', 'FFF', tickers=['^IXIC', 'USDTRY=X'], compare=True).days(10)  # plots yields of all elements in single plot

a.table('GGG', tickers=['USDTRY=X']).months(1)  # prints table of prices and yields to console

a.hist('HHH', 'III', tickers=['^IXIC']).days(30)  # creates bar graph of overall return in given interval

# You can also get raw data
my_data = a.data('VVV', 'YYY', 'ZZZ', tickers=['USDTRY=X']).years(5)
```

## License
Copyright (c) M. Deniz Kızılırmak. All rights reserved.

Licensed under the MIT license.