from machine import SD
import time
import machine
import os

def csv_parse():
    """
    :csv_parse(): Automatically detect the DIS csv files and transform the data into dictionaries. The returned objects are the PHY and SEN DIS is dictionary with the form of {FieldName: [type, value]}
    """
    sd = SD()
    mntpt = "/s"+str(time.ticks_ms())
    print("[SYS] SD Card Mounted on " +mntpt)
    os.mount(sd, mntpt)
    ls = os.listdir(mntpt)
    for path in ls:                                         ##Scanning Physical DIS path
        if ("phy" in path) and ("csv" in path):
            p_path = path
            print("[SYS] Physical DIS found: "+ p_path)

        if ("sen" in path) and ("csv" in path):             ##Scanning Sensor DIS path
            s_path = path
            print("[SYS] Sensor DIS found: "+ s_path)

    f = open( mntpt+"/"+p_path, 'r')                        ##Reading Physical DIS
    data = f.read()
    f.close()
    print("[SYS] Reading CSV file")
    lines = data.split()
    fname = []
    value=[]
    for line in lines:
        t = line.split(',')
        fname.append(t[0])
        value.append([t[1], t[2]])
    p_dis_dict = dict(zip(fname, value))

    f = open( mntpt+"/"+s_path, 'r')                        ##Reading Sensor DIS path
    data = f.read()
    f.close()
    print("[] Reading CSV file")
    lines = data.split()
    fname = []
    value=[]
    for line in lines:
        t = line.split(',')
        fname.append(t[0])
        value.append([t[1], t[2]])
    s_dis_dict = dict(zip(fname, value))

    return p_dis_dict, s_dis_dict

def print_dis(dis_dict):
    """
    :print_dis(): Input a dictionary in the form of {FieldName: [type, value]} to print the DIS in a readable format.
    """
    print("{:<16} {:<10} {:<10}".format('Key','Type','Value'))
    print("="*(32+24))
    for k, v in dis_dict.items():
        tp, vl = v
        print("{:<16} {:<10} {:<10}".format(k, tp, vl))
    print("-\n")
