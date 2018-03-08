import h5py
import numpy as np
import os
from treelib import Tree


class NwbSd(object):

    def __init__(self, nwbPath):
        self.hdf = h5py.File(nwbPath, 'r')
        self._tree = None

    @staticmethod
    def _isNotHardLink(obj):
        """ Only need soft and external links """
        try:
            link = obj.parent.get(obj.name, getlink=True)
            if not isinstance(link, h5py.HardLink):
                return True
        except AttributeError:
            pass

    @staticmethod
    def _attachLinkedNodes(obj, tree, root):
        # Because of the issue a hack is needed
        # https://github.com/h5py/h5py/issues/671

        siblings = [i for i in list(obj.parent.values()) if NwbSd._isNotHardLink(i)]
        for item in siblings:
            if not tree.contains(item.name):
                link = item.parent.get(item.name, getlink=True)
                data = {'hdf_type': item.__class__.__name__,
                        'path': item.name,
                        link.__class__.__name__: link.path}
                tree.create_node(os.path.basename(item.name),
                                 os.path.join(root, item.name),
                                 parent=os.path.join(root, item.parent.name),
                                 data=data)

    @property
    def tree(self):
        """Returns tree representation of an nwb file"""

        root = '/'
        tree = Tree()
        tree.create_node(root, root, data='Group')

        def _traverseTree(name, obj):
            # Need to have a closure since there is
            # a strict signature for the visititems method.

            data = {'hdf_type': obj.__class__.__name__,
                    'path': obj.name}
            tree.create_node(os.path.basename(obj.name),
                             os.path.join(root, name),
                             parent=os.path.join(root, obj.parent.name),
                             data=data)

            NwbSd._attachLinkedNodes(obj, tree, root)

        self.hdf.visititems(_traverseTree)
        if not self._tree:
            self._tree = tree

        return tree

    def getChildItems(self, path):
        return [str(i.name) for i in list(self.hdf.get(path).values())]

    def getTimeStamps(self, path):
        try:
            return self.hdf.get(os.path.join(path, 'timestamps')).value
        except AttributeError:
            pass

    def getIndexFromTimeStamp(self, path, timeStamp):
        timeStamps = self.getTimeStamps(path).tolist()
        closest = min(timeStamps, key=lambda x: abs(x-timeStamp))

        return timeStamps.index(closest)

    def getValueFromIndex(self, path, index):
        try:
            indexed = self.hdf.get(os.path.join(path, 'indexed_timeseries/data')).value
            return indexed[self.hdf.get(os.path.join(path, 'data')).value[index]]
        except AttributeError:
            return self.hdf.get(os.path.join(path, 'data')).value[index]

    def getValueFromTimeStamp(self, path, timeStamp):
        index = self.getIndexFromTimeStamp(path, timeStamp)
        try:
            indexed = self.hdf.get(os.path.join(path, 'indexed_timeseries/data')).value
            return indexed[self.hdf.get(os.path.join(path, 'data')).value[index]]
        except AttributeError:
            return self.hdf.get(os.path.join(path, 'data')).value[index]
