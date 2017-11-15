#!/usr/bin/python
# -*- coding: UTF-8 -*-
import argparse


def main(files, output):
    points = dict().fromkeys(files, 0)
    with open(output, 'w', encoding='utf-8') as of:
        for file in files:
            with open(file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.lstrip():
                        print(line.strip(), file=of)
                        points[file] += 1
            print(points[file])


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-fs', '--files', nargs='+', help='the list of files to be merged')
    ap.add_argument('-o', '--output', nargs='?', help='the output file')
    args = ap.parse_args()
    main(args.files, args.output)
