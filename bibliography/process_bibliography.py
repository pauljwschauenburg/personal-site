# -*- coding: utf-8 -*-
"""
Some material courtesy of Jonathan Gillian.
(https://github.com/jonathan-g/jonathangilligan.hugo/blob/master/bibliography/process_bibliography.py)
"""
import glob
import os
import shutil
import sys
from datetime import datetime
from pybtex.database import parse_file


def gen_md(bib):
    for (key, entry) in bib.entries.items():
        outfile = open(os.path.join('content', key + '.md'), 'w', encoding="utf-8")
        printout = lambda x: print(x, file=outfile)
        printout('---')
        printout('author:')
        for author in entry.persons['author']:
            printout(f" - family: {' '.join(author.prelast_names + author.last_names)}")
            printout(f"   given: {' '.join(author.first_names + author.middle_names)}")
        day = '01' if 'day' not in entry.fields else entry.fields['day']
        date = datetime.strptime(f"{entry.fields['year']} {entry.fields['month']} {day}", "%Y %B %d")
        printout(f"pubdate: '{datetime.strftime(date, '%Y-%m-%d')}'")
        printout(f"title: '{entry.fields['title'].replace('}', '').replace('{', '')}'")
        if 'prevenue' in entry.fields:
            printout(f"prevenue: {entry.fields['prevenue']}")
        printout(f"venue: {entry.fields['venue']}")
        printout("links:")
        for key in entry.fields:
            if key.startswith('link'):
                printout(f" - text: {key[4:]}")
                printout(f"   url: {entry.fields[key]}")
        printout('---')
        outfile.close()

def move_md_files(src = 'content', dest = '../content/publications'):
    files = glob.glob(os.path.join(src, '*.md'))
    if not os.path.isdir(dest):
        os.makedirs(dest)
    for f in files:
        base = os.path.split(f)[1]
        dest_file = os.path.join(dest, base)
        shutil.copyfile(f, dest_file)
            


def main():
    bibliography = parse_file(sys.argv[1])
    gen_md(bibliography)
    move_md_files()
    # move_pdf_files()

if __name__ == '__main__':
    main()
