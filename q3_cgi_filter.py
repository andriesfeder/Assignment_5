#!/usr/bin/python

import sys
import struct
import copy
import ctypes
import pickle
import cgi
import cgitb
cgitb.enable()

if __name__ == '__main__':
    print "Content-type: text/html\n"
    form = cgi.FieldStorage()
    out_text = []
    if form['submit'] == 'load':

        infile =  open(form['file'], 'rb')
        img_data = file.read(infile)
        out_file = open("result.bmp", 'wb')
        out_file.write( img_data )

        undo = []
        redo = []
        pickle.dump( [undo, redo], open( "history.pickle", "wb" ) )
        out_text = 'success'
    elif form['submit'] == 'filter':
        check = FileCheck("result.bmp")
        if check == 0:
            out_text = "Please load a file first."
        else:
            infile =  open("result.bmp", 'rb')
            img_data = file.read(infile)
            undo, redo = pickle.load(open("history.pickle", "rb"))
            if len(undo) == 0:
                undo = [img_data,]
                redo = []
                pickle.dump( [undo, redo], open( "history.pickle", "wb" ) )
                out_text = 'success'
            else :
                undo = [img_data,] + undo
                redo = []
                pickle.dump( [undo, redo], open( "history.pickle", "wb" ) )
                out_text = 'success'

            filter_width = ctypes.c_int('3')
            pyarr = [ctypes.c_float(float(form[00])),]
            pyarr = pyarr + [ctypes.c_float(float(form[01])),]
            pyarr = pyarr + [ctypes.c_float(float(form[02])),]
            pyarr = pyarr + [ctypes.c_float(float(form[10])),]
            pyarr = pyarr + [ctypes.c_float(float(form[11])),]
            pyarr = pyarr + [ctypes.c_float(float(form[12])),]
            pyarr = pyarr + [ctypes.c_float(float(form[20])),]
            pyarr = pyarr + [ctypes.c_float(float(form[21])),]
            pyarr = pyarr + [ctypes.c_float(float(form[22])),]
            arr = (ctypes.c_float * len(pyarr))(*pyarr)
            clib = ctypes.cdll.LoadLibrary("libfast_filter.so")
            clib.doFiltering(img_data, arr, filter_width, img_data)
            out_file = open("result.bmp", 'wb+')
            out_file.write( img_data )

    elif form['submit'] == 'undo':
        check = FileCheck("result.bmp")
        if check == 0:
            out_text = "Please load a file first."
            return
        undo, redo = pickle.load(open("history.pickle", "rb"))
        if len(undo) == 0:
            out_text = "There is nothing to be undone"
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
            out_text = 'success'
    elif form['submit'] == 'redo':
        check = FileCheck("result.bmp")
        if check == 0:
            out_text = "Please load a file first."
            return
        undo, redo = pickle.load(open("history.pickle", "rb"))
        if len(redo) == 0:
            out_text = "There is nothing to be redone"
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
            out_text = 'success'
    else :
        out_text = "I don't understand."

    print """<html>

<body>
<form name="input" action="./q3_cgi_filter.py" method="post" enctype="multipart/form-data">

    <p>Status of previous command: %s </p>
    <p>New photo to load: <input type="file" name="photo" /></p>
    <p>Next filter to apply:</p>
    <p><input type="text" name="00" value="1.000000"> <input type="text" name="01" value="1.000000"> <input type="text" name="02" value="1.000000"> </p>
    <p><input type="text" name="10" value="1.000000"> <input type="text" name="11" value="-7.000000"> <input type="text" name="12" value="1.000000"> </p>
    <p><input type="text" name="20" value="1.000000"> <input type="text" name="21" value="1.000000"> <input type="text" name="22" value="1.000000"> </p>
    <input type="submit" value="Load" name="load">
    <input type="submit" value="Filter" name="filter">
    <input type="submit" value="Undo" name="undo">
    <input type="submit" value="Redo" name="redo">

</form>

<hl>

<img src="%s"/>
</body>
</html>


    """ %(out_text, "result.bmp")



def FileCheck(fn):
    try:
        open(fn, "r")
        return 1
    except IOError:
        print "Error: No active file."
        return 0
