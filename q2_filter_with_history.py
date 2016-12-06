#!/usr/bin/python

import sys
import struct
import copy
import ctypes
import pickle

def main() :

    if sys.argv[1] == 'load':

        infile =  open(sys.argv[2], 'rb')
        img_data = file.read(infile)
        out_file = open("result.bmp", 'wb')
        out_file.write( img_data )

        undo = []
        redo = []
        pickle.dump( [undo, redo], open( "history.pickle", "wb" ) )

    elif sys.argv[1] == 'filter':
        check = FileCheck("result.bmp")
        if check == 0:
            print "Please load a file first."
        else:
            infile =  open("result.bmp", 'rb')
            img_data = file.read(infile)
            undo, redo = pickle.load(open("history.pickle", "rb"))
            if len(undo) == 0:
                undo = [img_data,]
                redo = []
                pickle.dump( [undo, redo], open( "history.pickle", "wb" ) )

            else :
                undo = [img_data,] + undo
                redo = []
                pickle.dump( [undo, redo], open( "history.pickle", "wb" ) )

            filter_width = ctypes.c_int(int(sys.argv[2]))
            pyarr = []
            for nums in sys.argv[3:] :
                pyarr = pyarr + [ctypes.c_float(float(nums)),]
            arr = (ctypes.c_float * len(pyarr))(*pyarr)
            clib = ctypes.cdll.LoadLibrary("libfast_filter.so")
            clib.doFiltering(img_data, arr, filter_width, img_data)
            out_file = open("result.bmp", 'wb+')
            out_file.write( img_data )

    elif sys.argv[1] == 'undo':
        check = FileCheck("result.bmp")
        if check == 0:
            print "Please load a file first."
            return
        undo, redo = pickle.load(open("history.pickle", "rb"))
        if len(undo) == 0:
            print "There is nothing to be undone"
        else :
            infile =  open("result.bmp", 'rb')
            img_data = file.read(infile)
            infile.close()
            redo = [img_data,]+redo
            img_data = undo[0]
            out_file = open("result.bmp", 'wb+')
            out_file.write( img_data )
            out_file.close()
            del undo[0]
            pickle.dump( [undo, redo], open( "history.pickle", "wb" ) )

    elif sys.argv[1] == 'redo':
        check = FileCheck("result.bmp")
        if check == 0:
            print "Please load a file first."
            return
        undo, redo = pickle.load(open("history.pickle", "rb"))
        if len(redo) == 0:
            print "There is nothing to be redone"
        else :
            infile =  open("result.bmp", 'rb')
            img_data = file.read(infile)
            infile.close()
            undo = [img_data,]+undo
            img_data = redo[0]
            out_file = open("result.bmp", 'wb+')
            out_file.write( img_data )
            out_file.close()
            del redo[0]
            pickle.dump( [undo, redo], open( "history.pickle", "wb" ) )

    else :
        print "I don't understand."

def FileCheck(fn):
    try:
        open(fn, "r")
        return 1
    except IOError:
        print "Error: No active file."
        return 0

if __name__ == '__main__':
    main()
