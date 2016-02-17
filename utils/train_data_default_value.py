# This script help to get default value of data
# when attribute shows `-1`, we should make a
# default value instead of it for quering.
import argparse
import json
import math


ATTRNAMES = "x36,x37,x59,x151,x167,x175,x198,x226,x322,x325,x480,x476"
ATTRNAMES = ATTRNAMES.split(',')
ATTRNAMES = [{
    'index': int(i[1:]),
    'name': i,
    'max': None,
    'min': None,
    'default': None,
    'count': 0,
    'distribution': None
} for i in ATTRNAMES]


def output(verbose):
    print('------------RESULT------------')
    for attr in ATTRNAMES:
        print('feature: %s' % attr['name'])
        print('count  : %s' % attr['count'])
        print('max    : %s' % attr['max'])
        print('min    : %s' % attr['min'])
        print('default: %s' % attr['default'])
        if verbose != '0':
            print('distribution:')
            print(attr['distribution'])
        print('------------------------------')


def compute(file, count, val, verbose):
    file.readline()
    # get max and min
    for i in range(0, count):
        line = file.readline().rstrip('\r\n').split(',')
        for j, x in enumerate(ATTRNAMES):
            value = float(line[x['index']])
            if value != -1:
                if x['max'] is None or value > x['max']:
                    x['max'] = value
                if x['min'] is None or value < x['min']:
                    x['min'] = value
                x['count'] += 1
    # make distribution
    file.seek(0)
    file.readline()
    for attr in ATTRNAMES:
        attr['distribution'] = [[0, 0] for i in range(0, val + 1)]
        attr['_val'] = (attr['max'] - attr['min']) / val
    for i in range(0, count):
        line = file.readline().rstrip('\r\n').split(',')
        for j, x in enumerate(ATTRNAMES):
            value = float(line[x['index']])
            if value != -1:
                idx = math.floor((value - x['min']) / x['_val'])
                x['distribution'][idx][0] += 1
                x['distribution'][idx][1] += value
    for attr in ATTRNAMES:
        maxd = max(attr['distribution'], key=lambda x: x[0])
        attr['default'] = maxd[1] / maxd[0]
    # output
    output(verbose)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Format data.")
    parser.add_argument('--file', default=None)
    parser.add_argument('--count', default="7500")
    parser.add_argument('--val', default="50")
    parser.add_argument('--verbose', default="0")

    args = parser.parse_args()
    print(args)
    if args.file is None:
        parser.print_help()
        exit()

    with open(args.file) as f:
        compute(f, int(args.count), int(args.val), verbose=args.verbose)
