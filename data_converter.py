"""
    SED data file converter
    [Usage]
    python data_converter.py --source [datafile.xxx | list-of-file-to-be-converted.txt] --type [data | dt | dtm | pkl | xml]
    --source        datafile.xxx (xxx can be data/dt/dtm/pkl/xml) or a list file contains datafile names
    --savetype      the objective type to be converted to
    --savedir       directory to save converted file(s)
"""

import argparse
import os
import progressbar
import struct
import time
import cPickle as pickle

TYPES = ('.data', '.dt', '.dtm', '.pkl')

DATA_INDICES = {
        'CONF' : 0,
        'CLS' : 1,
        'COORDS' : 2
        }

def read_from_file(filename):
    assert os.path.exists(filename), "Cannot find {}".format(filename)
    ext = os.path.splitext(filename)[1]
    if ext == '.data':
        data = _read_data(filename)
    elif ext == '.dt':
        data = _read_data(filename)
    elif ext == '.dtm':
        data = _read_dtm(filename)
    elif ext == '.pkl':
        data = _read_pkl(filename)
    elif ext == '.xml':
        data = _read_xml(filename)
    else:
        assert ext in TYPES, "Unsupported file type ".format(ext)
    return data


def _read_data(filename):
    data = {}
    append = list.append
    with open(filename, 'rb') as f:
        while True:
            raw = f.read(8)
            if not raw:
                break
            fid, num = struct.unpack('ii', raw)
            data[fid] = []
            for i in range(num):
                det = f.read(20)
                x1, y1, x2, y2, conf = struct.unpack('4if', det)
                # class_id is set to be -1
                append(data[fid], (conf, -1, (x1, y1, x2, y2)))
    return data

def _read_dt(filename):
    data = {}
    append = list.append
    with open(filename, 'rb') as f:
        while True:
            raw = f.read(20)
            fid, x1, y1, x2, y2 = struct.unpack('5i', raw)
            if data[fid] is None:
                data[fid] = []
            append(data[fid], (1.0, -1, (x1, y1, x2, y2)))
    return data

def _read_dtm(filename):
    data = {}
    append = list.append
    with open(filename, 'rb') as f:
        while True:
            raw = f.read(28)
            fid, conf, classid, x1, y1, x2, y2 = struct.unpack('if5i', raw)
            if data[fid] is None:
                data[fid] = []
            append(data[fid], (conf, classid, (x1, y1, x2, y2)))
    return data

def _read_pkl(filename):
    f = open(filename)
    data = pickle.load(f)
    return data

def _read_xml(filename):
    pass

def cvt(data, savename):
    assert data is not None, 'data is None'
    ext = os.path.splitext(savename)[1]
    if ext == '.data':
        _cvt2data(data, savename)
    elif ext == '.dt':
        _cvt2dt(data, savename)
    elif ext == '.dtm':
        _cvt2dtm(data, savename)
    elif ext == '.pkl':
        _cvt2pkl(data, savename)
    elif ext == '.xml':
        _cvt2xml(data, savename)
    else:
        assert ext in TYPES, "Unsupported file type {}".format(ext)

def _cvt2data(data, savename):
    f = open(savename, 'wb')
    assert f is not None, "cannot open {}".format(savename)
    for fid, dets in data.items():
        ndets = len(dets)
        raw = struct.pack('2i', fid, ndets)
        f.write(raw)
        for box in dets:
            rawdet = struct.pack('4if',
                    box[DATA_INDICES['COORDS']][0],
                    box[DATA_INDICES['COORDS']][1],
                    box[DATA_INDICES['COORDS']][2],
                    box[DATA_INDICES['COORDS']][3],
                    box[DATA_INDICES['CONF']])
            f.write(rawdet)
    f.close()

def _cvt2dt(data, savename):
    f = open(savename, 'wb')
    assert f is not None, "cannot open {}".format(savename)
    for fid, dets in data.items():
        if not dets:
            continue
        for box in dets:
            rawdet = struct.pack('5i',
                    fid,
                    box[DATA_INDICES['COORDS']][0],
                    box[DATA_INDICES['COORDS']][1],
                    box[DATA_INDICES['COORDS']][2],
                    box[DATA_INDICES['COORDS']][3])
            f.write(rawdet)
    f.close()

def _cvt2dtm(data, savename):
    f = open(savename, 'wb')
    assert f is not None, "cannot open {}".format(savename)
    for fid, dets in data.items():
        if not dets:
            continue
        for box in dets:
            rawdet = struct.pack('if5i',
                    fid,
                    box[DATA_INDICES['CONF']],
                    box[DATA_INDICES['CLS']],
                    box[DATA_INDICES['COORDS']][0],
                    box[DATA_INDICES['COORDS']][1],
                    box[DATA_INDICES['COORDS']][2],
                    box[DATA_INDICES['COORDS']][3])
            f.write(rawdet)
    f.close()

def _cvt2pkl(data, savename):
    f = open(savename, 'wb')
    assert f is not None, "cannot open {}".format(savename)
    pickle.dump(data, f)

def _cvt2xml(data, savename):
    pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Data file converter')
    parser.add_argument('-s', '--source', help="source file")
    parser.add_argument('-t', '--savetype', help="type to convert to")
    parser.add_argument('-d', '--savedir', help="where to save results")
    
    args = parser.parse_args()
    source, savetype, savedir = args.source, args.savetype, args.savedir
    savetype = ".{}".format(savetype)

    assert os.path.exists(source), "cannot find {}".format(source)
    if os.path.exists(savedir) is not True:
        os.mkdir(savedir)
    assert os.path.exists(savedir), "cannot find {}".format(savedir)
    assert savetype in TYPES, "Unsupported file type {}".format(savetype)

    list_of_files = []
    append = list.append
    ext = os.path.splitext(source)[1]
    if ext == '.txt':
        with open(source) as f:
            for line in f.readlines():
                append(list_of_files, line)
    else:
        append(list_of_files, source)

    print "Num of file to be processed: {}".format(len(list_of_files))

    nb_skipped = 0
    nb_processed = 0
    pb = progressbar.ProgressBar(maxval=len(list_of_files))
    pb.start()
    for datafile in list_of_files:
        name, ext = os.path.splitext(os.path.split(datafile)[1])
        if ext == savetype:
            print "{} has the same type of the type to be coverted, skipped".format(datafile)
            nb_skipped += 1
        else:
            data = read_from_file(datafile)
            savename = os.path.join(savedir, name + savetype)
            cvt(data, savename) 
        nb_processed += 1
        time.sleep(0.1)
        pb.update(nb_processed)
    pb.finish()

    print "finished, {} skipped, {} processed".format(nb_skipped, len(list_of_files)-nb_skipped)

