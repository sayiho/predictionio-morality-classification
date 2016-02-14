import argparse
import json
import math


def getContentArray(line):
    return json.loads('[' + line + ']')


def getHead(line, featurestype, gcount):
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
                        'count': 0,
                        'max': None,
                        'min': None,
                        'avg': 0,
                        '-1': 0,
                        'sd': 0,
                        'distribution': [0 for i in range(0, gcount)]
                    },
                    0: {
                        'count': 0,
                        'max': None,
                        'min': None,
                        'avg': 0,
                        '-1': 0,
                        'sd': 0,
                        'distribution': [0 for i in range(0, gcount)]
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


def statistics(file, label, out, featurestype, verbose, csv, gcount):
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
                info['count'] += 1
        count += 1
        if count % 200 == 0:
            print('deal %d lines' % count)

    print('compute standard deviation and distribution...')
    file.seek(0)
    file.readline()
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
                if x != -1:
                    info['sd'] += (x - info['avg']) * (x - info['avg'])
        count += 1
        if count % 200 == 0:
            print('deal %d lines' % count)
    for i in range(0, feature_count):
        if head[i]['type'] == 'numeric':
            info = head[i]['info']
            info[0]['sd'] = math.sqrt(info[0]['sd'] / info[0]['count'])
            info[1]['sd'] = math.sqrt(info[1]['sd'] / info[1]['count'])

    print('output...')
    if csv == '0':
        for i in range(0, feature_count):
            target = head[i]
            if target['type'] == 'numeric':
                out.write(json.dumps(target) + '\r\n')
    else:
        titles = [
            'feature',
            '0:count', '0:-1', '0:avg', '0:min',
            '0:max', '0:standard deviation',
            '1:count', '1:-1', '1:avg', '1:min',
            '1:max', '1:standard deviation'
        ]
        titles = ['"' + i + '"' for i in titles]
        out.write(','.join(titles) + '\r\n')
        for i in range(0, feature_count):
            target = head[i]
            if target['type'] == 'numeric':
                line = [
                    target['key'],
                    target['info'][0]['count'],
                    target['info'][0]['-1'],
                    target['info'][0]['avg'],
                    target['info'][0]['min'],
                    target['info'][0]['max'],
                    target['info'][0]['sd'],
                    target['info'][1]['count'],
                    target['info'][1]['-1'],
                    target['info'][1]['avg'],
                    target['info'][1]['min'],
                    target['info'][1]['max'],
                    target['info'][1]['sd']
                ]
                out.write(json.dumps(line)[1:-1].replace(' ', '') + '\r\n')
    print('done')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Make a train data features distribution statistics.")
    parser.add_argument('--file', default=None)
    parser.add_argument('--out', default=None)
    parser.add_argument('--featurestype', default=None)
    parser.add_argument('--label', default=None)
    parser.add_argument('--verbose', default="0")
    parser.add_argument('--csv', default="0")
    parser.add_argument('--distributiongroupcount', default="20")

    args = parser.parse_args()
    print(args)
    if args.file is None or args.featurestype is None:
        parser.print_help()
        exit()

    with open(args.file, 'r') as f, open(args.label, 'r') as flabel, \
            open(args.out, 'w') as fout:
        statistics(
            f,
            flabel,
            fout,
            featurestype=args.featurestype,
            verbose=args.verbose,
            csv=args.csv,
            gcount=int(args.distributiongroupcount)
        )
