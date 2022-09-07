__author__ = 'marco'

# from datetime import datetime
import math
import re
import os
import sys

regex = re.compile(r"\.[0-9]{3}")
headersize = 0x202
dstfolder = "C:\\tmp"

with open(sys.argv[1], "rb") as f:
    while True:
        header = f.read(headersize)
        if header[0] == 0:
            break
        filename = header.decode("utf-8").split("\x00")[0][:-4]
        folder = regex.sub("", header[0x101:0x200].decode("utf-8").split("\x00")[0])
        headerdata = [x for x in header[0x7c:0x9a].decode("utf-8").split(" ") if x]
        payloadsize = int(headerdata[0], 8) - 2
        utime = int(headerdata[1], 8)
        blocksize = 0x200 * math.ceil((payloadsize + headersize) / 0x200)
        fullfolder = "{0}/{1}".format(dstfolder, folder)
        if not os.path.exists(fullfolder):
            os.makedirs(fullfolder)
        fullfilename = "{0}/{1}".format(fullfolder, filename)

        print("Processing {0}/{1}...".format(folder, filename))
        # print("Size: ", payloadsize)
        # print("Time: ", datetime.fromtimestamp(utime).strftime('%Y-%m-%d %H:%M:%S'))
        # print("Block size: ", format(blocksize, '#04x'))
        payload = f.read(payloadsize)
        with open(fullfilename, "wb") as g:
            g.write(payload)
        utimes = int(headerdata[1], 8)
        os.utime(fullfilename, (utime, utime))
        f.read(blocksize - headersize - payloadsize)
