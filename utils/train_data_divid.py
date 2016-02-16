# This script help to divid `train_x.csv` and `train_y.csv`
# and pick specific attributes to the format:
# label,attr1 attr2 attr3 ...
# This will also divid the result to 2 files which named
# `train_data.p0.txt` and `train_data.p1.txt`,
# We will use them for training and testing.
import argparse
import json


OUTPUT = 'train_data.p%d.txt'
ATTRNAMES = "x36,x37,x59,x151,x167,x175,x198,x226,x322,x325,x480,x476"
ATTRNAMES = ATTRNAMES.split(',')
ATTRNAMES = [int(i[1:]) for i in ATTRNAMES]


def divid(trainx, trainy, verbose):
    linex = trainx.readline()
    liney = trainy.readline()
    for p in range(0, 2):
        fout = open(OUTPUT % p, 'w')
        for i in range(0, 7500):
            linex = trainx.readline().rstrip('\r\n').split(',')
            liney = trainy.readline().rstrip('\r\n').split(',')[1]
            arr = []
            for i, x in enumerate(ATTRNAMES):
                arr.append(linex[x])
            if '-1' in arr:
                continue
            linex = ' '.join(arr)
            liney += ',%s\n' % linex
            fout.write(liney)
        fout.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Format data.")
    parser.add_argument('--trainx', default=None)
    parser.add_argument('--trainy', default=None)
    parser.add_argument('--verbose', default="0")

    args = parser.parse_args()
    print(args)
    if args.trainx is None or args.trainy is None:
        parser.print_help()
        exit()

    with open(args.trainx) as trainx, open(args.trainy) as trainy:
        divid(trainx, trainy, verbose=args.verbose)
