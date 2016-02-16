# This script help to get default value of data
# when attribute shows `-1`, we should make a
# default value instead of it for quering.
import argparse
import json


ATTRNAMES = "x36,x37,x59,x151,x167,x175,x198,x226,x322,x325,x480,x476"
ATTRNAMES = ATTRNAMES.split(',')
ATTRNAMES = [int(i[1:]) for i in ATTRNAMES]


def comute(file, count, verbose):
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Format data.")
    parser.add_argument('--file', default=None)
    parser.add_argument('--count', default="7500")
    parser.add_argument('--val', default="30")
    parser.add_argument('--verbose', default="0")

    args = parser.parse_args()
    print(args)
    if args.trainx is None:
        parser.print_help()
        exit()

    with open(args.file) as f:
        compute(f, int(args.count), verbose=args.verbose)
