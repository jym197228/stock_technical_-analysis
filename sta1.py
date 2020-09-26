def read_file(filename):
    prices = []
    with open(filename, 'r') as f:
        for line in f:
            if 'Adj Close' in line:
                continue
            data = line.strip().split(',')
            prices.append(data[5])
    return prices


def three_days(data):
    output = []
    for i in range(len(data)):
        if i < 3: 
            output.append(0)
        elif data[i] > data[i - 1] > data[i - 2] > data[i - 3]:
            output.append(1)
        elif data[i] < data[i - 1] < data[i - 2] < data[i - 3]:
            output.append(-1)
        else:
            output.append(0)
    return output


def trading_timing(output):
    timing = []
    for i in range(len(output)):
        if i < 1:
            timing.append(0)
        elif output[i] == 0:
            timing.append(timing[i - 1]) 
        elif output[i] == 1:
            timing.append(output[i])
        elif output[i] == -1:
            timing.append(output[i])
    return timing


def owned_asset(timing, prices):
    cash = 1000000
    for i in range(len(timing)):
        if timing[i] == 0:
            continue
        elif timing[i] == 1 and timing[i - 1] == 0:
            cash = cash - float(prices[i]) * 1000
        elif timing[i] == -1 and timing[i - 1] == 0:
            cash = cash + float(prices[i]) * 1000
    return cash

def main():
    prices = read_file('2330.csv')
    output = three_days(prices)
    timing = trading_timing(output)
    cash = owned_asset(timing, prices)
    print(cash - 1000000)
    roi = (cash - 1000000) / 1000000
    print('投資報酬率為', roi, '%')

main()