import json
import sys


def walk(t, label, nodes, links, depths, level):
    if type(t) == dict:
        key = list(t.keys())[0]
        val = t[key]

        if not key.startswith('roi'):
            nodes.add(key)
            if key not in depths:
                depths[key] = level
            if label and not label.startswith('roi'):
                links.add((label, key))

        walk(val, key, nodes, links, depths, level+1)
    elif type(t) == list:
        for x in t:
            walk(x, label, nodes, links, depths, level+1)

    elif type(t) == str:
        if not t.startswith('roi'):
            nodes.add(t)
            if t not in depths:
                depths[t] = level
            if not label.startswith('roi'):
                links.add((label, t))
    else:
        raise RuntimeError


def main():
    # Load a tree from stdin.
    tree = json.loads(sys.stdin.read())

    # Walk the tree, recording nodes and links.
    nodes = set()
    links = set()
    depths = {}
    walk(tree, None, nodes, links, depths, 0)

    # Create a table of nodes and links suitable for WebCola.
    nodes = list(map(lambda x: {'name': x, 'depth': depths[x]}, nodes))
    index = {n['name']: i for i, n in enumerate(nodes)}

    links = [{'source': index[s], 'target': index[t]} for s, t in links]

    # Dump out a json representation of the node and link tables.
    print(json.dumps({'nodes': nodes, 'links': links}, indent=2))

    return 0


if __name__ == '__main__':
    sys.exit(main())
