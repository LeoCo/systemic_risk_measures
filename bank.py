import pandas

class Bank(object):

    def __init__(self, name='', ticker='', datas=pandas.DataFrame(),prices=pandas.DataFrame()):
        self.name = name
        self.ticker = ticker
        self.datas = datas
        self.prices = prices