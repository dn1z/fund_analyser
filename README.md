# fund_analyser
TR: [tefas.gov.tr](https://tefas.gov.tr) sitesinde yer alan fonların fiyat ve getirileri için çizim programı  
ENG: A script that provides plotting functions for prices and yields of funds in [tefas.gov.tr](https://tefas.gov.tr)

## Installation (tr. kurulum)
* Make sure python, pip, and git is installed. (tr. python, pip ve git uygulamaları kurulu değilse kurun)
* Execute following commands in console. (tr. konsolda aşağıdaki komutları çalıştırın)
```
git clone https://github.com/dn1z/fund_analyser
cd fund_analyser
pip install -r requirements.txt
python setup.py install
```

## Usage (tr. kullanım)
* As a command line script (tr. konsol uygulaması olarak)
```
usage: fund_analyser plot [-h] [-t [TICKERS [TICKERS ...]]] (-m MONTHS | -d DAYS | -w WEEKS | -y YEARS) funds [funds ...]
usage: fund_analyser table [-h] [-t [TICKERS [TICKERS ...]]] (-m MONTHS | -d DAYS | -w WEEKS | -y YEARS) funds [funds ...]
usage: fund_analyser hist [-h] [-t [TICKERS [TICKERS ...]]] (-m MONTHS | -d DAYS | -w WEEKS | -y YEARS) funds [funds ...]

positional arguments:
  funds                 Takas codes of funds

optional arguments:
  -h, --help            show this help message and exit
  -t [TICKERS [TICKERS ...]], --tickers [TICKERS [TICKERS ...]]
                        Symbol of tickers (Yahoo! Finance)
  -m MONTHS, --months MONTHS
  -d DAYS, --days DAYS
  -w WEEKS, --weeks WEEKS
  -y YEARS, --years YEARS
```
* As a library (tr. yazılım kütüphanesi olarak)
```python
from fund_analyser import FundAnalyser

a = FundAnalyser()

a.plot('AAA').weeks(1)  # plots last weeks performance of the fund
a.plot('BBB', 'CCC').months(2)  # plots multiple funds
a.plot('DDD', tickers=['USDTRY=X']).years(3)  # plots a ticker with fund

a.table('GGG', tickers=['USDTRY=X']).months(1)  # prints table of prices and yields to console

a.hist('HHH', 'III', tickers=['^IXIC']).days(30)  # creates bar graph of overall return in given interval

# You can also get raw data
my_data = a.data('VVV', 'YYY', 'ZZZ', tickers=['USDTRY=X']).years(5)
```

## License
Copyright (c) M. Deniz Kızılırmak. All rights reserved.

Licensed under the MIT license.
