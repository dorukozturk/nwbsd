import json
import sys


def ensure_node(node_list, depth_list, name, path, link, level):
    depth_list[path] = max(level, depth_list.get(path, -1))

    if path not in node_list:
        node_list[path] = {
            'name': name,
            'path': path
        }

    if link:
        node_list[path]['link'] = link

    return node_list[path]


def walk(t, label, nodes, links, depths, level):
    name = t['name']
    path = t['path']
    link = t.get('link')
    children = t.get('children', [])

    if not name.startswith('roi'):
        node = ensure_node(nodes, depths, name, path, link, level)

        if label and not label.startswith('roi'):
            links.add((label, path, False))

        # If the new node is a softlink, ensure there's a node for the target
        # already, and install a special link.
        if 'link' in node:
            ensure_node(nodes, depths, link.split('/')[-1], link, None, level + 1)

            links.add((path, link, True))

        for c in children:
            walk(c, path, nodes, links, depths, level + 1)


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
        path = item[1][0]
        data = item[1][1]

        return {
            'name': data['name'],
            'index': index,
            'path': path,
            'depth': depths[path]
        }

    nodes = list(map(make_node, enumerate(nodes.items())))
    index = {n['path']: i for i, n in enumerate(nodes)}

    links = [{'source': index[s], 'target': index[t], 'softlink': l} for s, t, l in links]

    # Dump out a json representation of the node and link tables.
    print(json.dumps({'nodes': nodes, 'links': links}, indent=2))

    return 0


if __name__ == '__main__':
    sys.exit(main())
