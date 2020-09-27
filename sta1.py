def read_file(filename): # 讀取檔案
    prices = []
    with open(filename, 'r') as f:
        for line in f:
            if 'Adj Close' in line:
                continue
            data = line.strip().split(',')
            prices.append(data[5])
    return prices


def three_days(data): # 判斷買進、賣出訊號
    signal = []
    for i in range(len(data)):
        if i < 3: # 在判斷的當下是不會知道當天收盤價的，所以我們應該要做的事情為判斷"前三天"的收盤價狀況。
            signal.append(0) # e.g. 第四天判斷第一、二、三天的收盤價
        elif data[i] > data[i - 1] > data[i - 2] > data[i - 3]:
            signal.append(1)
        elif data[i] < data[i - 1] < data[i - 2] < data[i - 3]:
            signal.append(-1)
        else:
            signal.append(0)
    return signal


def owned_stock(signal): # 將交易訊號轉換成股票擁有狀況
    stock = []
    for i in range(len(signal)):
        if i < 1:
            stock.append(0)
        elif signal[i] == 0:
            stock.append(stock[i - 1]) 
        elif signal[i] == 1:
            stock.append(signal[i])
        elif signal[i] == -1:
            stock.append(signal[i])
    return stock


def owned_cash(stock, prices): # 利用股票持有狀況來計算資金增減
    cash = 1000000
    for i in range(len(stock)):
        if stock[i] == 0:
            continue
        elif stock[i] == 1 and stock[i - 1] == 0:
            cash = cash - float(prices[i]) * 1000
        elif stock[i] == -1 and stock[i - 1] == 0:
            cash = cash + float(prices[i]) * 1000
        elif stock[i] == 1 and stock[i - 1] == -1:
            cash = cash - float(prices[i]) * 1000 * 2
        elif stock[i] == -1 and stock[i - 1] == 1:
            cash = cash + float(prices[i]) * 1000 * 2
    cash = cash + float(prices[len(stock) - 1]) * float(stock[len(stock) - 1]) # 強制變現
    return cash


def main():
    prices = read_file('2330.csv')
    signal = three_days(prices)
    stock = owned_stock(signal)
    cash = owned_cash(stock, prices)
    print('完成投資後的總利潤為', cash - 1000000, '元')
    roi = (cash - 1000000) / 1000000
    print('投資報酬率為', roi, '%')


main()