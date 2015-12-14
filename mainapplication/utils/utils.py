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