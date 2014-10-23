import csv
import re
import os
DIST_DIR = 'csv_div_year'
def mkdir():
    try:
        os.mkdir(DIST_DIR)
    except FileExistsError:
        pass

def divide_by_years(filename, first_year='96', second_year='97'):
    mkdir()
    fin = csv.reader(open(filename))
    header = fin.__next__()
    fyear_dir = os.path.join(DIST_DIR, '{fyear}s_data.csv'.format(fyear=first_year))
    syear_dir = os.path.join(DIST_DIR, '{syear}s_data.csv'.format(syear=second_year))
    if not os.path.exists(fyear_dir):
        fyear = csv.writer(open(fyear_dir,'a+'))
        fyear.writerow(header)
    else:
        fyear = csv.writer(open(fyear_dir,'a+'))
    if not os.path.exists(syear_dir):
        syear = csv.writer(open(syear_dir,'a+'))
        syear.writerow(header)
    else:
        syear = csv.writer(open(syear_dir,'a+'))
    try:
        for line in fin:
            if not line:continue
            if line[4].startswith(first_year):
                fyear.writerow(line)
            elif line[4].startswith(second_year):
                syear.writerow(line)
    except csv.Error as e:
        print("error occured {0}".format(e))
if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("""
            you need to pass arguments:
            [1]src file you wanna exmine:
                'dir_name'
            example
                python year_divider.py csv_files
             """)
        exit()
    print("triming data.\nwait a moment...")
    src = sys.argv[1]
    for files in os.listdir(src):
        if 'csv' in files:
            print(files)
            divide_by_years(os.path.join(src,files))

