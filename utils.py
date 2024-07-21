#!/usr/bin/python

# Chunis Deng (chunchengfh@gmail.com)


def to_sign_value(n):
    if n > 127:
        n -= 256
    return n

def crc(data):
    crc = 0xFF
    for d in data:
        for _ in range(8):
            sum = (crc ^ d) & 0x01
            d >>= 1
            crc >>= 1
            if(sum):
                crc ^= 0x65
    return (crc)

# convert list of bytes to hex string such as: [6, 12] ==> '0x06 0x0c'
def bytes2hexstr(blist, sep=' ', with_0x=True, pad=True):
    fmt = '%'
    if with_0x:
        fmt = '0x' + fmt
    if pad:
        fmt += '02'
    fmt += 'X'
    data = [fmt %x for x in blist]
    return sep.join(data)


def convert_hexstring_to_bytes(arg_list):
    args = [x.lower().replace('0x', '') for x in arg_list]
    args = ['0x' + x for x in args]
    try:
        args = [int(x, 16) for x in args]
        return args
    except:
        print("invalid hex value in %s" %arg_list)
        return None

def extract_int_from_str(data):
    base = 10
    negative = 1

    data = data.strip()
    if data[0] == '-':
        negative = -1
        data = data[1:]
        if not data:
            return None
    if data[:2] == '0x' or data[:2] == '0X':
        base = 16
        data = data[2:]
        if not data:
            return None
    try:
        value = int(data, base)
    except:
        return None
    return value * negative


if __name__ == '__main__':
    y = '34';    print("%s = %s" %(y, extract_int_from_str(y)))
    y = '0x20';  print("%s = %s" %(y, extract_int_from_str(y)))
    y = '-34';   print("%s = %s" %(y, extract_int_from_str(y)))
    y = '-0x20'; print("%s = %s" %(y, extract_int_from_str(y)))
    y = '-0X1F'; print("%s = %s" %(y, extract_int_from_str(y)))
    y = '-0X1H'; print("%s = %s" %(y, extract_int_from_str(y)))
    y = 'X-0X1'; print("%s = %s" %(y, extract_int_from_str(y)))
