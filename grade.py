#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import json
from os.path import isfile, join
import filecmp
import time
import subprocess

PROGRAM = 'poly.py'
FULL_SCORE = 80
TIME_LIMIT = 1.0
DATA_PATH = 'data'

if len(sys.argv) > 1:
    PROGRAM = sys.argv[1]

if sys.version_info[0] != 3:
    print("Plz use python3")
    sys.exit()


def file_lines(file):
    lines = []
    with open(file, 'r') as fd:
        for line in fd:
            line = line.strip()
            if len(line) > 0:
                lines.append(line)
    return lines


if __name__ == '__main__':

    grade = 0
    data = dict()
    files = [f for f in os.listdir(DATA_PATH) if isfile(join(DATA_PATH, f)) and f.startswith('in')]

    for file in sorted(files):
        file_in = join(DATA_PATH, file)
        num = int(file[2:-4])
        file_ans = join(DATA_PATH, f'ans{num}.txt')
        file_out = join(DATA_PATH, f'out{num}.txt')
        try:
            os.remove(file_out)
        except FileNotFoundError:
            pass
        p = subprocess.Popen([sys.executable, PROGRAM], stdin=open(
            file_in, 'r'), stdout=open(file_out, 'w'), stderr=subprocess.PIPE)
        start_time = time.time()

        while p.poll() is None:
            if time.time() - start_time > TIME_LIMIT:
                p.kill()

        ans, out = file_lines(file_ans), file_lines(file_out)
        if ans == out:
            grade += FULL_SCORE / len(files)
        elif os.isatty(1):
            print('Data %d: expected %s, but got %s' %
                (num, repr(ans), repr(out)))
            stdout, stderr = p.communicate(timeout=1)
            if len(stderr) > 0:
                print('       : your program exited with:')
                sys.stdout.buffer.write(stderr)

    # output grade
    grade = int(grade)
    data['grade'] = grade
    if os.isatty(1):
        print(f'Grade: {grade}/{int(FULL_SCORE)}')
    else:
        print(json.dumps(data))

    if grade < FULL_SCORE:
        sys.exit(1)
