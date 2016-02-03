import predictionio
import argparse


def query(attrs):
    ret = {}
    for i, attr in enumerate(attrs):
        ret['attr%d' % i] = int(attr)
    return ret


def test_event(client, file):
    f = open(file, 'r')
    count = 0
    success = 0
    distribution = {}
    print("Testing data...")
    for line in f:
        data = line.rstrip('\r\n').split(",")
        if distribution.get(data[0], None) is None:
            distribution[data[0]] = {
                "count": 0,
                "success": 1
            }
        plan = float(data[0])
        attr = data[1].split(" ")
        plan_query = client.send_query(query(attr))['label']
        print({
            'expect': plan,
            'attrs': attr,
            'get': plan_query
        })
        count += 1
        distribution[data[0]]['count'] += 1
        if plan == plan_query:
            success += 1
            distribution[data[0]]['success'] += 1

    f.close()
    print('------------RESULT------------')
    print('Test Count: %d' % count)
    print('Success: %d' % success)
    print('Fail: %d' % (count - success))
    print('Success Rate: %f' % (success / count))
    print('------------DETAIL------------')
    for key in distribution.keys():
        d = distribution[key]
        print("For label '%s':" % key)
        print('  Count: %d' % d['count'])
        print('  Success: %d' % d['success'])
        print('  Fail: %d' % (d['count'] - d['success']))
        print('  Success Rate: %f' % (d['success'] / d['count']))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Import sample data for classification engine")
    parser.add_argument('--url', default="http://localhost:8000")
    parser.add_argument('--file', default="./data/data.txt")

    args = parser.parse_args()
    print(args)

    client = predictionio.EngineClient(url=args.url)
    test_event(client, args.file)
