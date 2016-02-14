import argparse
import json


def getContentArray(line):
    return json.loads('[' + line + ']')


def getHead(line, featurestype):
    data = getContentArray(line)[1:]
    ret = {}
    for i, x in enumerate(data):
        obj = {
            'key': x,
        }
        ret[x] = obj
        ret[i] = obj
    with open(featurestype, 'r') as f:
        line = f.readline()
        for line in f:
            line = line.rstrip('\r\n')
            line = getContentArray(line)
            target = ret[line[0]]
            target['type'] = line[1]
            if line[1] == 'numeric':
                target['info'] = {
                    1: {
                        'max': None,
                        'min': None,
                        'avg': 0,
                        '-1': 0
                    },
                    0: {
                        'max': None,
                        'min': None,
                        'avg': 0,
                        '-1': 0
                    }
                }
    return ret, len(data)


def getLabel(label):
    ret = {}
    line = label.readline()
    for line in label:
        line = line.rstrip('\r\n')
        line = getContentArray(line)
        ret[line[0]] = line[1]
    return ret


def statistics(file, label, out, featurestype, verbose):
    line = file.readline().rstrip('\r\n')
    head, feature_count = getHead(line, featurestype)
    labels = getLabel(label)
    count = 0
    for line in file:
        line = line.rstrip('\r\n')
        line = getContentArray(line)
        uid = line[0]
        line = line[1:]
        for i, x in enumerate(line):
            target = head[i]
            if target['type'] == 'numeric':
                info = target['info'][labels[uid]]
                x = float(x)
                if x == -1:
                    info['-1'] += 1
                else:
                    if info['max'] is None or x > info['max']:
                        info['max'] = x
                    if info['min'] is None or x < info['min']:
                        info['min'] = x
                    info['avg'] = (info['avg'] * count + x) / (count + 1)
        count += 1
        if count % 200 == 0:
            print('deal %d lines' % count)
    for i in range(0, feature_count):
        out.write(json.dumps(head[i]) + '\r\n')
    print('done')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Make a train data features distribution statistics.")
    parser.add_argument('--file', default=None)
    parser.add_argument('--out', default=None)
    parser.add_argument('--featurestype', default=None)
    parser.add_argument('--label', default=None)
    parser.add_argument('--verbose', default="0")

    args = parser.parse_args()
    print(args)
    if args.file is None or args.featurestype is None:
        parser.print_help()
        exit()

    with open(args.file, 'r') as f, open(args.label, 'r') as flabel, \
            open(args.out, 'w') as fout:
        statistics(
            f,
            flabel, fout, featurestype=args.featurestype, verbose=args.verbose)
