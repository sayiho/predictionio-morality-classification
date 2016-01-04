import sys
import json
from optparse import OptionParser


class config(object):
    parser = None

    usage = 'Usage: %prog [options]'
    parser_options = [
        {
            "short": "-a",
            "long": "--attribute",
            "action": "append",
            "dest": "attrs",
            "default": [],
            "help": "wanted attributes",
            "type": "string"
        },
        {
            "short": "-f",
            "long": "--file",
            "action": "store",
            "dest": "file",
            "default": None,
            "help": "source file path",
            "type": "string"
        },
        {
            "short": "-o",
            "long": "--output",
            "action": "store",
            "dest": "output",
            "default": None,
            "help": "output file path",
            "type": "string"
        },
        {
            "short": "--start",
            "long": None,
            "action": "store",
            "dest": "start",
            "default": 1,
            "help": "start line, zero-based, include title line",
            "type": "int"
        },
        {
            "short": "--end",
            "long": None,
            "action": "store",
            "dest": "end",
            "default": 10,
            "help": "end line, zero-based, include title line",
            "type": "int"
        },
    ]

    def __init__(self, args):
        self.parser = OptionParser(usage=self.usage)
        for opt in self.parser_options:
            self.parser.add_option(
                opt['short'],
                opt['long'],
                action=opt['action'],
                dest=opt['dest'],
                default=opt['default'],
                help=opt['help'],
                type=opt['type'])
        (self.options, self.args) = self.parser.parse_args(args)
        self.verify()

    def verify(self):
        if len(self.options.attrs) == 0:
            self.parser.error('attributes miss.')
        if self.options.file is None:
            self.parser.error('source file miss.')
        if self.options.start >= self.options.end:
            self.parser.error(
                'start line index should less than end line index')


def csvCellConverter(value):
    value = value.replace('\n', '')
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    else:
        try:
            return float(value)
        except Exception as e:
            return value


def csvConverter(line):
    ret = line.split(',')
    id = ret[0]
    ret = [csvCellConverter(attr) for attr in ret]
    ret[0] = id
    return ret


def deal_train_x(stream, start=1, end=10, attrs=[], output=None):
    th = csvConverter(stream.readline())
    attrs = [th.index(attr) for attr in attrs]
    # skip lines
    for line in range(1, start):
        stream.readline()
    for line in range(start, end):
        tr = csvConverter(stream.readline())
        tr_attrs = [tr[0]]
        tr_attrs.extend([tr[attr] for attr in attrs])
        if output is None:
            print(tr_attrs)
        else:
            output.write(json.dumps(tr_attrs) + '\n')
            print(tr_attrs[0])


def main(conf):
    with open(conf.options.file) as train_x:
        train_x = open(conf.options.file)
        output = None
        if conf.options.output is not None:
            output = open(conf.options.output, 'w')
        ret = deal_train_x(
            train_x,
            start=conf.options.start,
            end=conf.options.end,
            attrs=conf.options.attrs,
            output=output
        )
        if conf.options.output is not None:
            output.close()
    print('finish')


if __name__ == '__main__':
    main(config(sys.argv))
