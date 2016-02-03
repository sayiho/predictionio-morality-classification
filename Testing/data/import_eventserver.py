import predictionio
import argparse


def query(plan, attrs):
    ret = {
        "plan": int(plan)
    }
    for i, attr in enumerate(attrs):
        ret['attr%d' % i] = int(attr)
    return ret


def import_events(client, file):
    f = open(file, 'r')
    count = 0
    print("Importing data...")
    for line in f:
        data = line.rstrip('\r\n').split(",")
        plan = data[0]
        attr = data[1].split(" ")
        client.create_event(
            event="$set",
            entity_type="user",
            entity_id=str(count),
            properties=query(plan, attr)
        )
        count += 1
        print(count)
    f.close()
    print("%s events are imported." % count)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Import sample data for classification engine")
    parser.add_argument('--access_key', default='invald_access_key')
    parser.add_argument('--url', default="http://localhost:7070")
    parser.add_argument('--file', default="./data/data.txt")

    args = parser.parse_args()
    print(args)

    client = predictionio.EventClient(
        access_key=args.access_key,
        url=args.url,
        threads=5,
        qsize=500)
    import_events(client, args.file)
