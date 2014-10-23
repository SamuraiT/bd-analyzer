#! /usr/bin/env python
# coding: utf-8
"""
Copyright 2014 Tatsuro Yasukawa.

Distributed under the GNU General Public License at
gnu.org/licenses/gpl.html.
"""
from bs4 import BeautifulSoup
import csv
import re
import os
CSV_DIR = 'csv_files'

def mkdir():
    try:
        os.mkdir(CSV_DIR)
    except FileExistsError:
        pass


def xml2csv(filename, is_one_file=False, dist_file=''):
    with open(filename) as f:
        try:
            soup = BeautifulSoup(f,'html5lib')
        except UnicodeDecodeError:
            return
    headers = soup.find_all('header')
    if not is_one_file:
        fout = open(os.path.join(CSV_DIR, filename.replace('xml','csv')),'wt')
    else:
        fout = open(os.path.join(CSV_DIR,
                    'only_header_{dist}.csv'.format(dist=dist_file)
                    ),'a+')
    writer = csv.writer(fout)
    writer.writerow(
            ['post_id','mention_id','user_id','title','datetime'])
    for header in headers:
        rows = re.sub(r'\s', '', header.text).split(',')
        if re.search('\**',rows[3]).group(): continue
        writer.writerow(rows)
    fout.close()

def divide_by_years(filename, dist, first_year='96', second_year='97'):
    mkdir()
    fin = csv.reader(open(filename))
    header = fin.__next__()
    fyear_dir = os.path.join(CSV_DIR, '{fyear}.csv'.format(fyear=first_year))
    syear_dir = os.path.join(CSV_DIR, '{syear}.csv'.format(syear=second_year))
    if os.path.exists(fyear_dir):
        fyear = csv.writer(open(fyear_dir),'a+')
        fyear.writerow(header)
    else:
        fyear = csv.writer(open(fyear_dir),'a+')
    if os.path.exists(syear_dir):
        syear = csv.writer(open(syear_dir),'a+')
        syear.writerow(header)
    else:
        syear = csv.writer(open(syear_dir),'a+')
    for line in fin:
        if line[4].startswith(first_year):
            fyear.writerow(line)
        elif line[4].startswith(second_year):
            syear.writerow(line)

def traverse_dirs(is_one_file=True, starts='frm', skip=False):
    mkdir()
    for dirs in os.listdir():
        if not (dirs.startswith(starts) and os.path.isdir(dirs)):continue
        dist = 'only_header_{dist}.csv'.format(dist=dirs)
        if skip and os.path.exists(os.path.join(CSV_DIR,dist)):continue
        print(dirs)
        for f in os.listdir(dirs):
            if 'xml' in f:
                xml2csv(os.path.join(dirs,f), is_one_file, dirs)
       
if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("""
            you need to pass arguments:
            [1]if you wanna have results as one file as a first arguments:
                one_file
            [2]src file you wanna exmine:
                'dir_name'
            [3]distination's file name:
                'filename'

            example.
            if you wanna examine the frm005 directory and name the results file
            as only_header_005 command this:
                
                python cleaner.py one_file frm005 005

            if you want to traverse all the dirs that starts with 
            frm enter this:
                python cleaner.py traverse
            or 
                python cleaner.py -t
            and if you wanna skip files you wrote already add -s
                python cleaner.py -t -s
             """)
        exit()
    print("triming data.\nwait a moment...")
    if sys.argv[1] == 'traverse' or sys.argv[1] =='-t':
        try:
            skip = True if sys.argv[2] == '-s' else False
        except IndexError:
            skip = False
        print("traverse dirs...")
        traverse_dirs(skip=skip)
        exit()
    if sys.argv[1] == 'one_file':
        is_one_file = True
    else:
        is_one_file = False
    try:
        src = sys.argv[2]
    except:
        src = ''
    try:
        dist = sys.argv[3]
    except:
        dist = ''

    for files in os.listdir(src):
        if 'xml' in files:
            xml2csv(os.path.join(src,files), is_one_file, dist)

