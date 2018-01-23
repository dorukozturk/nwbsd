import pynwb
import numpy as np
from .timeseries import getTimeSeriesAdapter
from dateutil import parser
import h5py
import os
from treelib import Tree


class NwbSd(object):

    def __init__(self, nwbPath):
        legacy_map = pynwb.legacy.get_type_map()
        self.nwb = pynwb.NWBHDF5IO(nwbPath, extensions=legacy_map, mode='r').read()
        self.hdf = h5py.File(nwbPath)
        self._tree = None

    @property
    def tree(self):
        """Returns the tree of the nwb file"""

        module = 'processing'
        group = self.hdf.get(module)
        root = '/{}'.format(module)
        tree = Tree()
        tree.create_node(module, root, data='Group')

        def _traverseTree(name, obj):
            if isinstance(obj, h5py.Group):
                type_ = 'Group'
            elif isinstance(obj, h5py.Dataset):
                type_ = 'Dataset'
            tree.create_node(os.path.basename(name),
                             os.path.join(root, name),
                             parent=os.path.join(root, obj.parent.name),
                             data=type_)

        group.visititems(_traverseTree)
        if not self._tree:
            self._tree = tree

        return tree

    def getStimuli(self):
        """Returns a list of all stimulus"""
        return [i.name for i in self.nwb.stimulus]

    def _getProcessingModuleName(self):
        return list(self.nwb.modules.keys())[0]

    def getContainers(self):
        """Returns a list of all containers"""
        module = self._getProcessingModuleName()
        return [i.name for i in self.nwb.get_processing_module(module).containers]

    def getSessionStartTime(self):
        """Returns the session start time"""
        nwbTime = str(self.nwb.session_start_time)
        return parser.parse(nwbTime)

    def getStimulusTimeStamps(self, stimulus):
        """Returns a list of timestamps for a stimulus"""
        stim = self.nwb.get_stimulus(stimulus)
        return stim.timestamps.value

    def getStimulusData(self, stimulus, timeStamp):
        """Returns the stimulus data node for a given timestamp"""
        timeStamps = self.getStimulusTimeStamps(stimulus)
        index = np.where(timeStamps == timeStamp)

        stim = self.nwb.get_stimulus(stimulus)
        if isinstance(stim, pynwb.image.IndexSeries):
            index = stim.data.value[index]
            return stim.indexed_timeseries.data.value[index]
        else:
            return stim.data.value[index]

    def getTimeSeries(self, container):
        """Returns all available timeseries in a given container"""
        module = self._getProcessingModuleName()
        pipeline = self.nwb.get_processing_module(module)
        adapter = getTimeSeriesAdapter(pipeline, container)
        return adapter.getTimeSeries()

    def getTimeSeriesTimeStamps(self, container, timeSeries):
        """Returns a list of timestamps for a timeSeries"""
        module = self._getProcessingModuleName()
        pipeline = self.nwb.get_processing_module(module)
        adapter = getTimeSeriesAdapter(pipeline, container)
        return adapter.getTimeSeriesTimeStamps(timeSeries)
