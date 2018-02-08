import functools
import json
from nwbsd.slicerdicer import NwbSd
import os.path


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

# Load the data and extract the tree view.
data = NwbSd(os.path.join('tests', '570014520.nwb'))
tree = data.tree.to_dict()

sample = {
    'a': {
        'children': [
            {
                'b': {
                    'children': ['c', 'd', 'e']
                },
            },
            {
                'f': {
                    'children': [
                        {
                            'h': {'children': ['g']}
                        },
                        {
                            'k': {'children': ['i']}
                        }
                    ]
                }
            }
        ]
    }
}

# Normalize the tree into something more easily traversable.
tree_norm = normalize(tree)
tree_flat = unleaf(tree_norm)

sample_norm = normalize(sample)
sample_flat = unleaf(sample_norm)

# Dump the normalized tree out as JSON.
print(json.dumps(tree_flat, indent=2))
