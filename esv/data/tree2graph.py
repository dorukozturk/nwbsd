import json
import sys


def walk(t, label, nodes, links, depths, level):
    name = t['name']
    path = t['path']
    link = t.get('link')
    children = t.get('children', [])

    # If there's a "link" property, it is the true node name.
    key = link or path

    if not name.startswith('roi'):
        nodes[key] = {
            'name': name,
            'key': key
        }

        if key not in depths:
            depths[key] = level
        if label and not label.startswith('roi'):
            links.add((label, key))

        for c in children:
            walk(c, key, nodes, links, depths, level + 1)


def main():
    # Load a tree from stdin.
    tree = json.loads(sys.stdin.read())

    # Walk the tree, recording nodes and links.
    nodes = {}
    links = set()
    depths = {}
    walk(tree, None, nodes, links, depths, 0)

    # Create a table of nodes and links suitable for WebCola.
    def make_node(item):
        index = item[0]
        key = item[1][0]
        data = item[1][1]

        return {
            'name': data['name'],
            'index': index,
            'key': key,
            'depth': depths[key]
        }

    nodes = list(map(make_node, enumerate(nodes.items())))
    index = {n['key']: i for i, n in enumerate(nodes)}

    links = [{'source': index[s], 'target': index[t]} for s, t in links]

    # Dump out a json representation of the node and link tables.
    print(json.dumps({'nodes': nodes, 'links': links}, indent=2))

    return 0


if __name__ == '__main__':
    sys.exit(main())
