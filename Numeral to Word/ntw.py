from sys import argv

#Databases
Ones = ['', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']

TenToNineteen = ['ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen']
Tens = ['twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']

Biggers = ['', ' thousand', ' million', ' billion', ' trillion', ' quadrillion', ' pentillion', ' sextillion']

def main():
    if len(argv) != 2:
        print("Usage: python ntw.py [number]")
    
    num = list(argv[1])
    x = convert(num, 0).split()
    print(' '.join(x))
    
def convert(num, n):
    if len(num) == 0:
        return ''

    x1 = setofthree(num[-3:])
    if x1 != '':
        x = (x1 + Biggers[n])
    else:
        x = ''
    y = convert(num[:-3], n + 1)
            
    if x and y:
       return y + ' ' + x
    else:
        return (y + x).strip()

def setofthree(num):
    if len(num) == 1:
        return onedig(''.join(num))
    elif len(num) == 2:
        return twodig(num)
    else:
        return threedig(num)

def onedig(num):
    return Ones[int(num)]

def twodig(num):
    if num[0] == '0':
        return onedig(num[1])
    elif num[0] == '1':
        return TenToNineteen[int(num[1])] 
    else:
        if int(num[1]) == 0:
            return Tens[int(num[0])-2]
        else:
            return Tens[int(num[0])-2] + ' ' + onedig(num[1])

def threedig(num):
    x = twodig(num[1] + num[2])
    y = onedig(num[0])
            
    if x != '':
        x = ' ' + x 
    if y != '':
        y = y + ' Hundred' 
    return y + x

if __name__ == '__main__':
    main()

