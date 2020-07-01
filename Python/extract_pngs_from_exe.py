import struct
import os
import re


def find_png(filename):
    PNG_HEADER =  b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'
    END_MARKER = b'IEND'

    # extract binary data from file
    data = open(filename, 'rb').read()
    binary = os.path.basename(filename)
    header_pos = 0

    # find all PNGs by PNG Header
    for png in re.finditer(PNG_HEADER, data):
        header_pos = png.start()
        
        # Extract data of PNG (chunk by chunk)
        pos = header_pos + 8
        while True:
            if data[pos + 4 : pos + 8] == END_MARKER:
                open(f'{binary}-@{header_pos:06X}.png', 'wb').write(data[header_pos : pos + 12])
                break
            pos += 12 + struct.unpack('>I', data[pos : pos + 4])[0]     #">I" stands for big-endian


find_png(r'C:\your.exe')