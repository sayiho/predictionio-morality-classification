import argparse
import json
import random


def make_data(args, file):
    f = open(file, 'w')
    for arg in args:
        for x in range(0, arg['count']):
            line = ''
            line += str(arg['label'])
            line += ','
            args = []
            for ar in arg['args']:
                args.append(str(random.randint(ar[0], ar[1])))
            line += ' '.join(args)
            print(line)
            f.write(line + '\r\n')
    f.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Import sample data for classification engine")
    parser.add_argument('--file', default="./data/data_test.txt")
    parser.add_argument('--args', default='[\
    {\
    "label":0,"count":50,"args":[\
    [45,60],[20,35],[10,15],[20,30]\
    ]},{\
    "label":1,"count":50,"args":[\
    [57,90],[15,30],[15,25],[35,60]\
    ]}]')

    args = parser.parse_args()
    print(args)

    make_data(json.loads(args.args), args.file)
