import datetime
import pynwb
import numpy as np
from .timeseries import getTimeSeriesAdapter


class NwbSd(object):

    def __init__(self, nwbPath):
        legacy_map = pynwb.legacy.get_type_map()
        self.nwb = pynwb.NWBHDF5IO(nwbPath, extensions=legacy_map, mode='r').read()

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
        nwbTime = str.join(' ', self.nwb.session_start_time.split(None)[1:7])
        return datetime.datetime.strptime(nwbTime, '%b %d %H:%M:%S %Y')

    def getStimulusTimeStamps(self, stimulus):
        """Returns a list of timestamps for a stimulus"""
        stim = self.nwb.get_stimulus(stimulus)
        return stim.timestamps.value

    def _getStimulusDataIndex(self, stimulus):
        stim = self.nwb.get_stimulus(stimulus)
        return stim.data.value

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
