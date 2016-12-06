#!/usr/bin/python

import sys
import struct
import copy
import ctypes

def main() :
    infile =  open(sys.argv[1], 'rb')
    img_data = file.read(infile)
    out_file = open(sys.argv[2], 'wb+')
    filter_width = ctypes.c_int(int(sys.argv[3]))
    pyarr = []
    for nums in sys.argv[4:] :
        pyarr = pyarr + [ctypes.c_float(float(nums)),]
    arr = (ctypes.c_float * len(pyarr))(*pyarr)
    clib = ctypes.cdll.LoadLibrary("libfast_filter.so")
    clib.doFiltering(img_data, arr, filter_width, img_data)

    out_file.write( img_data )

if __name__ == '__main__':
    main()
