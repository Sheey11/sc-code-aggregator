import os, io
import os.path
import re
from typing import List
ignores = []
with open('./.aggignore') as f:
    ignores = f.read().splitlines()
    ignores = [ ignore.replace('.', '\\.').replace('*', '.*') for ignore in ignores ]

def is_ignored(filename, parent='', folder=False):
    for ignore in ignores:
        if re.match(ignore, filename):
            return True
        if folder and ignore[-1] == '/' and re.match(ignore[:-1], filename):
            return True
    return False

def combine_files(dir, parent = '') -> List[str]:
    files = os.listdir(dir)
    result = []
    for file in files:
        if is_ignored(file, parent, os.path.isdir(parent + file)):
            continue
        if os.path.isfile(parent + file):
            with io.open(parent + file, encoding='utf-8') as f:
                try:
                    lines = f.readlines()
                    lines = [ line.replace('\n', '') for line in lines if line.replace('\n', '').strip() != '' ]
                except:
                    print('Error: ' + parent + file)
                    continue
            result += lines
        else:
            result += combine_files(parent + file + '/', parent + file + '/')
    return result

with io.open('out.txt', mode='w', encoding='utf-8') as f:
    lines = combine_files('.')
    i = 0
    while i < len(lines):
        i += 50 - 1
        lines.insert(i + 1, '########################PAGE BREAK########################')
        i += 2
    f.write('\n'.join(lines))