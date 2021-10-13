import re

text = open(input(), 'r', encoding='utf-8').read()

def convert(data):
    ones = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"]
    tens = ["", "X", "XX", "XXX", "XL", "L", "LX", "LXX", "LXXX", "XC"]
    hunds = ["", "C", "CC", "CCC", "CD", "D", "DC", "DCC", "DCCC", "CM"]
    thous = ["", "M", "MM", "MMM", "MMMM"]

    t = thous[data // 1000]
    h = hunds[data // 100 % 10]
    te = tens[data // 10 % 10]
    o = ones[data % 10]

    return t + h + te + o


for num in re.findall(' \d+ | \d(?=, )| \d(?=. )| \d+\.\n', text):
    nu=num.strip()
    #print(num)
    '''if nu[-1]==',':
        nu=nu[0:len(nu)-1]'''
    if nu.isnumeric():
        n = int(nu)
        #print(n)
        n1=convert(n)
        if n < 1 or n > 3100: continue

        if num.endswith(' '):
            text = text.replace(num, ' ' + n1 + ' ')
        elif num.endswith(', '):
            text = text.replace(num, ' ' + n1 + ',')
        elif num.endswith(''):
            text = text.replace(num, ' ' + n1)

print(text)
