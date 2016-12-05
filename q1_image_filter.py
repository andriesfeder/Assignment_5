#!/usr/bin/python

import sys
import struct
import copy
import ctypes

def main() :
    infile = sys.argv[1]
    outfile = sys.argv[2]
    filter_width = sys.argv[3]
    filter_weights = []
    for nums in sys.argv[4:] :
        filter_weights = filter_weights + [nums,]

    clib = ctypes.cdll.LoadLibrary("libfast_filter.so")

    #clib.doFiltering(infile, filter_weights, filter_width, outfile)


if __name__ == '__main__':
    main()
