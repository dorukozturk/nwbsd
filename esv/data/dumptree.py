import functools
import json
from nwbsd.slicerdicer import NwbSd
import sys


def normalize(t):
    if type(t) == dict:
        val = {k: list(map(normalize, v['children'])) for k, v in t.items()}
        return val
    elif type(t) == str:
        return t
    else:
        raise RuntimeError(type(t))


# Grab filename from commandline.
if len(sys.argv) < 2:
    print('usage: dumptree.py <nwbfile>', file=sys.stderr)
    sys.exit(1)

inputfile = sys.argv[1]

# Load the data and extract the tree view.
data = NwbSd(inputfile)
tree = data.tree.to_dict()

# Normalize the tree into something more easily traversable.
tree_norm = normalize(tree)

# Dump the normalized tree out as JSON.
print(json.dumps(tree_norm, indent=2))
