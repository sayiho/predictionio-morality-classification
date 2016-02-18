# This script help to test data and output as format
import argparse
import json
import math
import predictionio


ATTRNAMES = "x36,x37,x59,x151,x167,x175,x198,x226,x322,x325,x480,x476"
ATTRNAMES = ATTRNAMES.split(',')
ATTRNAMES = [int(i[1:]) for i in ATTRNAMES]


def query(attrs):
    ret = {
        'features': []
    }
    for i, attr in enumerate(attrs):
        ret['features'].append(float(attr))
    return ret


def test(client, file, out, verbose, val):
    linein = file.readline()
    out.write('"uid","score"\n')
    count = 0
    label0 = 0
    label1 = 0
    for line in file:
        line = line.rstrip('\r\n').split(",")
        attr = []
        for j, x in enumerate(ATTRNAMES):
            attr.append(line[x])
        request = client.send_query(query(attr))
        out.write('%s,%f\n' % (
            line[0], request['probabilities']['values'][1] * val))
        count += 1
        if request['label'] == 0:
            label0 += 1
        else:
            label1 += 1
        print(count)
    print('done')
    print('------------RESULT------------')
    print('Test Count: %d' % count)
    print('Label 0   : %d(%f%%)' % (label0, label0 / count * 100))
    print('Label 1   : %d(%f%%)' % (label1, label1 / count * 100))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Format data.")
    parser.add_argument('--url', default="http://localhost:8000")
    parser.add_argument('--file', default=None)
    parser.add_argument('--out', default=None)
    parser.add_argument('--val', default="100")
    parser.add_argument('--verbose', default="0")

    args = parser.parse_args()
    print(args)
    if args.file is None or args.out is None:
        parser.print_help()
        exit()

    with open(args.file) as filein, open(args.out, 'w') as fileout:
        client = predictionio.EngineClient(url=args.url)
        test(
            client,
            filein,
            fileout,
            verbose=args.verbose,
            val=float(args.val)
        )
