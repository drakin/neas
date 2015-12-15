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


def arrayDisc(size, center, radius, alghoritmIndex=0):
    array = np.zeros(size)
    if alghoritmIndex == 0:
        x, y = draw.circle_perimeter(center[1], center[0], radius, shape=size)
        array[x, y] = 1
        x, y = draw.circle(center[1], center[0], radius, shape=size)
        array[x, y] = 1
        return array

    if alghoritmIndex == 1:
        x, y, val = draw.circle_perimeter_aa(center[1], center[0], radius, shape=size)
        array[x, y] = val
        x, y = draw.circle(center[1], center[0], radius, shape=size)
        array[x, y] = 1
        return array
    return None