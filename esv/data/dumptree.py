import functools
import json
from nwbsd.slicerdicer import NwbSd
import sys


def normalize(t):
    '''
    Rearrange tree nodes so they all have canonical structure: a "name" field,
    "path" field, and then optionally a list of children.
    '''

    def compute_path(d):
        if type(d) == str:
            return '/'
        else:
            return d['path']

    def compute_link(d):
        if type(d) == str:
            return None
        else:
            return d.get('SoftLink')

    def strip_empty(rec):
        if not rec['children']:
            del rec['children']

        if not rec['link']:
            del rec['link']

        return rec

    items = t.items()
    if len(items) > 1:
        raise RuntimeError('too many cooks')

    key, val = list(items)[0]

    return strip_empty({
        'name': key,
        'path': compute_path(val['data']),
        'link': compute_link(val['data']),
        'children': list(map(normalize, val.get('children', [])))
    })


# Grab filename from commandline.
if len(sys.argv) < 2:
    print('usage: dumptree.py <nwbfile>', file=sys.stderr)
    sys.exit(1)

inputfile = sys.argv[1]

# Load the data and extract the tree view.
data = NwbSd(inputfile)
tree = data.tree.to_dict(with_data=True)

# Normalize the tree into something more easily traversable.
tree_norm = normalize(tree)

# Dump the normalized tree out as JSON.
print(json.dumps(tree_norm, indent=2))
