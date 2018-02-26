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


def unleaf(tt):
    def unleaf_helper(t):
        if type(t) == str:
            return t

        keys = list(t.keys())
        if len(keys) != 1:
            raise RuntimeError('non-unique label')

        key = keys[0]
        val = t[key]

        if type(val) == list and val and type(val[0]) == str:
            return key
        elif type(val) == list and val and type(val[0]) == dict:
            return {key: list(map(unleaf_helper, val))}
        else:
            raise RuntimeError

    return {k: list(map(unleaf_helper, v)) for k, v in tt.items()}

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
tree_flat = unleaf(tree_norm)

# Dump the normalized tree out as JSON.
print(json.dumps(tree_flat, indent=2))
