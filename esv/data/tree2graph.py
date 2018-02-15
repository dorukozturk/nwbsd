import json
import sys


def walk(t, label, nodes, links, level):
    if type(t) == dict:
        key = list(t.keys())[0]
        val = t[key]

        nodes.add(key)
        if label:
            links.add((label, key))

        walk(val, key, nodes, links, level+1)
    elif type(t) == list:
        for x in t:
            walk(x, label, nodes, links, level+1)

    elif type(t) == str:
        nodes.add(t)
        links.add((label, t))
    else:
        raise RuntimeError


def main():
    # Load a tree from stdin.
    tree = json.loads(sys.stdin.read())

    # Walk the tree, recording nodes and links.
    nodes = set()
    links = set()
    walk(tree, None, nodes, links, 0)

    # Create a table of nodes and links suitable for WebCola.
    nodes = list(map(lambda x: {'name': x}, nodes))
    index = {n['name']: i for i, n in enumerate(nodes)}

    links = [{'source': index[s], 'target': index[t]} for s, t in links]

    # Dump out a json representation of the node and link tables.
    print(json.dumps({'nodes': nodes, 'links': links}, indent=2))

    return 0


if __name__ == '__main__':
    sys.exit(main())
