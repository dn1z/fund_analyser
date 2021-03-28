import argparse
from datetime import datetime

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import requests
import yfinance as yf
from dateutil.relativedelta import relativedelta

_API_LINK = "https://ws.spk.gov.tr/PortfolioValues/api/PortfoyDegerleri/{strTakasCodesArray}/1/{dateBegin}/{dateEnd}"


class _Interval:
    _begin = None
    _end = None

    _registered_func = None
    _arguments = {}

    def _reset(self):
        self._begin = self._end = self._registered_func = None
        self._arguments = {}

    def days(self, days):
        today = datetime.today()
        self._end = today.strftime('%Y-%m-%d')
        self._begin = (today - relativedelta(days=days)).strftime('%Y-%m-%d')

        return self._registered_func(**self._arguments, interval=self)

    def weeks(self, weeks):
        today = datetime.today()
        self._end = today.strftime('%Y-%m-%d')
        self._begin = (today - relativedelta(weeks=weeks)).strftime('%Y-%m-%d')

        return self._registered_func(**self._arguments, interval=self)

    def months(self, months):
        today = datetime.today()
        self._end = today.strftime('%Y-%m-%d')
        self._begin = (today - relativedelta(months=months)
                       ).strftime('%Y-%m-%d')

        return self._registered_func(**self._arguments, interval=self)

    def years(self, years):
        today = datetime.today()
        self._end = today.strftime('%Y-%m-%d')
        self._begin = (today - relativedelta(years=years)).strftime('%Y-%m-%d')

        return self._registered_func(**self._arguments, interval=self)


class FundAnalyser:
    def __init__(self):
        self._interval = _Interval()

    @staticmethod
    def _create_link(takas_codes, interval):
        return _API_LINK.format(strTakasCodesArray=','.join(
            takas_codes), dateBegin=interval._begin, dateEnd=interval._end)

    @staticmethod
    def _get_data(url):
        data = {}
        ret = requests.get(url)

        try:
            json = ret.json()
        except:
            print('Funds could not be loaded')
            exit()

        for row in json:
            fund = row['FonKodu']
            date = row['Tarih'][:10]
            price = row['BirimPayDegeri']

            try:
                data[fund][0].append(date)
                data[fund][1].append(price)
            except:
                data[fund] = [[date], [price]]

        return data

    @staticmethod
    def _get_ticker_data(ticker, interval):
        t = yf.Ticker(ticker)
        h = t.history(start=interval._begin, end=interval._end)['Close']

        if h.empty:
            return

        x = []
        y = []
        for k, i in h.items():
            x.append(k.to_pydatetime())
            y.append(i)
        return (x, y)

    def plot(self, *takas_codes, tickers=None):
        '''
        Plots prices and percent changes of takas codes and tickers.
        PARAMETERS
        ----------
        takas_codes: str
            Funds takas code(s)
        tickers: list
            Tickers of symbols (Yahoo! Finance)
        '''
        self._interval._reset()

        args = locals().copy()
        del args['self']

        self._interval._arguments = args
        self._interval._registered_func = FundAnalyser._plot
        return self._interval

    def table(self, *takas_codes, tickers=None):
        '''
        Prints daily price and percent changes of funds and tickers as well as their
        overall change
        PARAMETERS
        ----------
        takas_codes: str
            Funds takas code(s)
        tickers: list
            Tickers of symbols (Yahoo! Finance)
        '''
        self._interval._reset()

        args = locals().copy()
        del args['self']

        self._interval._arguments = args
        self._interval._registered_func = FundAnalyser._table
        return self._interval

    def hist(self, *takas_codes, tickers=None):
        '''
        Draws overall change of funds and tickers in hist plot.
        PARAMETERS
        ----------
        takas_codes: str
            Funds takas code(s)
        tickers: list
            Tickers of symbols (Yahoo! Finance)
        '''
        self._interval._reset()

        args = locals().copy()
        del args['self']

        self._interval._arguments = args
        self._interval._registered_func = FundAnalyser._hist
        return self._interval

    def data(self, *takas_codes, tickers=None):
        '''
        Returns raw data of daily prices of takas codes and tickers
        Format is
        {
            "Fund1": [[dates (datetime)], [prices (float)]],
            "Ticker1": [[dates (datetime)], [prices (float)]],
            ...
        }
        PARAMETERS
        ----------
        takas_codes: str
            Funds takas code(s)
        tickers: list
            Tickers of symbols (Yahoo! Finance)
        '''
        self._interval._reset()

        args = locals().copy()
        del args['self']

        self._interval._arguments = args
        self._interval._registered_func = FundAnalyser._data
        return self._interval

    @staticmethod
    def _plot(takas_codes, tickers, interval):
        url = FundAnalyser._create_link(takas_codes, interval)
        data = FundAnalyser._get_data(url)

        if tickers:
            for t in tickers:
                res = FundAnalyser._get_ticker_data(t, interval)
                if res:
                    data[t] = res

        for e in data:
            x = data[e][0]
            if type(x[0]) == str:
                x = [datetime.strptime(d, "%Y-%m-%d").date()
                     for d in x]
            first = next(a for a in data[e][1] if a > 0)
            y = [v * 100 / first - 100 for v in data[e][1]]
            plt.plot(x, y, label=e)

        plt.ylabel(r'% change')
        plt.gca().yaxis.grid(True)
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %d %Y'))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=max(len(x) // 7, 1)))
        plt.gcf().autofmt_xdate()
        plt.legend()

        plt.show()

    @staticmethod
    def _table(takas_codes, tickers, interval):
        url = FundAnalyser._create_link(takas_codes, interval)
        data = FundAnalyser._get_data(url)

        if tickers:
            for t in tickers:
                res = FundAnalyser._get_ticker_data(t, interval)
                if res:
                    data[t] = res

        overall = {}

        for el in data:
            print('\n' + el)
            last_price = None

            dates = data[el][0]
            prices = data[el][1]
            for i, date in enumerate(dates):
                price = prices[i]
                percentage = '' if last_price == None else (
                    '-%' if price < last_price else ' %') + "{:.2f}".format(abs(100 - (price * 100 / last_price)))
                print(str(date)[:10] + ': ' +
                      "{:.6f}".format(price) + ' ' + percentage)
                last_price = price

            first_price = prices[0]
            overall[el] = ('-%' if last_price < first_price else ' %') + "{:.2f}".format(
                abs(100 - (last_price * 100 / first_price)))

        print('\n')
        for f in overall.keys():
            print(f + ' overall change: ' + overall[f])

    @staticmethod
    def _hist(takas_codes, tickers, interval):
        url = FundAnalyser._create_link(takas_codes, interval)
        data = FundAnalyser._get_data(url)

        if tickers:
            for t in tickers:
                res = FundAnalyser._get_ticker_data(t, interval)
                if res:
                    data[t] = res

        heights = []
        names = data.keys()
        for e in names:
            first = next(x for x in data[e][1] if x > 0)
            last = data[e][1][-1]
            heights.append(last * 100 / first - 100)

        plt.ylabel(r'% change')
        plt.bar(names, heights)
        plt.show()

    @staticmethod
    def _data(takas_codes, tickers, interval):
        url = FundAnalyser._create_link(takas_codes, interval)
        data = FundAnalyser._get_data(url)

        for k in data.keys():
            data[k][0] = [datetime.strptime(d, "%Y-%m-%d").date()
                          for d in data[k][0]]

        if tickers:
            for t in tickers:
                res = FundAnalyser._get_ticker_data(t, interval)
                if res:
                    data[t] = res

        return data


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command', required=True)

    plot = subparsers.add_parser('plot')
    hist = subparsers.add_parser('hist')
    table = subparsers.add_parser('table')

    def check_positive(value):
        ivalue = int(value)
        if ivalue <= 0:
            raise argparse.ArgumentTypeError(
                "%s is an invalid value" % value)
        return ivalue

    for _, subp in subparsers.choices.items():
        subp.add_argument('funds', nargs='+', help='Takas codes of funds')
        subp.add_argument('-t', '--tickers', nargs='*',
                          help='Symbol of tickers (Yahoo! Finance)')
        g = subp.add_mutually_exclusive_group(required=True)
        g.add_argument('-m', '--months', type=check_positive)
        g.add_argument('-d', '--days', type=check_positive)
        g.add_argument('-w', '--weeks', type=check_positive)
        g.add_argument('-y', '--years', type=check_positive)

    args = parser.parse_args()

    a = FundAnalyser()
    if args.command == 'plot':
        t = a.plot(*args.funds, tickers=args.tickers)
    elif args.command == 'hist':
        t = a.hist(*args.funds, tickers=args.tickers)
    elif args.command == 'table':
        t = a.table(*args.funds, tickers=args.tickers)

    if args.years:
        t.years(args.years)
    elif args.months:
        t.months(args.months)
    elif args.weeks:
        t.weeks(args.weeks)
    elif args.days:
        t.days(args.days)


if __name__ == '__main__':
    main()
