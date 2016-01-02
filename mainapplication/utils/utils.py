import draw
import numpy as np


def num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)


def delimited(inputFile, delimiter='\n', bufsize=4096):
        buf = ''
        while True:
            newbuf = inputFile.read(bufsize)
            if not newbuf:
                yield buf
                return
            buf += newbuf
            lines = buf.split(delimiter)
            for line in lines[:-1]:
                yield line
            buf = lines[-1]


def arrayRing(size, center, radius, alghoritmIndex=0, delta=0.1):
    array = np.zeros(size)
    tmp = radius[0]
    if alghoritmIndex == 0:
        while tmp < radius[1]:
            x, y = draw.circle_perimeter(center[1], center[0], tmp, shape=size)
            array[x, y] = 1
            tmp += delta
        return array

    if alghoritmIndex == 1:
        while tmp < radius[1]:
            x, y, val = draw.circle_perimeter_aa(center[1], center[0], tmp, shape=size)
            for x2,y2,val2 in zip(x,y,val):
                if array[x2, y2] < val2:
                    array[x2, y2] = val2
            tmp += delta
        return array
    return None
