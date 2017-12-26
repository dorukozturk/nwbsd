import abc
import six

# TODO: Should get the field names from yaml spec files (Currently hardcoded)


@six.add_metaclass(abc.ABCMeta)
class AbstractContainer(object):

    def __init__(self, pipeline, container):
        self.pipeline = pipeline
        self.container = self.pipeline.get_container(container)

    @abc.abstractmethod
    def getTimeSeries(self):
        pass

    @abc.abstractmethod
    def getTimeSeriesTimeStamps(self, timeSeries):
        pass


class BehavioralTimeSeriesAdapter(AbstractContainer):
    def getTimeSeries(self):
        fields = self.container.fields
        return [fields['time_series'].name]

    def getTimeSeriesTimeStamps(self, timeSeries):
        return self.container.time_series.timestamps.value


class DfOverFAdapter(AbstractContainer):
    def getTimeSeries(self):
        fields = self.container.fields
        return [i.name for i in fields['roi_response_series']]

    def getTimeSeriesTimeStamps(self, timeSeries):
        return self.container.roi_response_series[0].timestamps


class EyeTrackingAdapter(AbstractContainer):
    def getTimeSeries(self):
        fields = self.container.fields
        return [i.name for i in fields['spatial_series']]

    def getTimeSeriesTimeStamps(self, timeSeries):
        return [i.timestamps for i in self.container.spatial_series
                if i.name == timeSeries][0]


class FluorescenceAdapter(AbstractContainer):
    def getTimeSeries(self):
        fields = self.container.fields
        return [i.name for i in fields['roi_response_series']]

    def getTimeSeriesTimeStamps(self, timeSeries):
        return [i.timestamps for i in self.container.roi_response_series
                if i.name == timeSeries][0]


class ImageSegmentationAdapter(AbstractContainer):
    def getTimeSeries(self):
        fields = self.container.fields
        return [i.name for i in fields['plane_segmentations']]

    def getTimeSeriesTimeStamps(self, timeSeries):
        return None


class MotionCorrectionAdapter(AbstractContainer):
    def getTimeSeries(self):
        fields = self.container.fields
        return [i.name for i in fields['corrected_image_stacks']]

    def getTimeSeriesTimeStamps(self, timeSeries):
        return self.container.corrected_image_stacks[0].corrected.timestamps


class PupilTrackingAdapter(AbstractContainer):
    def getTimeSeries(self):
        fields = self.container.fields
        return [fields['time_series'].name]

    def getTimeSeriesTimeStamps(self, timeSeries):
        return self.container.time_series.timestamps.value


def getTimeSeriesAdapter(pipeline, container):
    if container == 'MotionCorrection':
        return MotionCorrectionAdapter(pipeline, container)
    elif container == 'DfOverF':
        return DfOverFAdapter(pipeline, container)
    elif container == 'Fluorescence':
        return FluorescenceAdapter(pipeline, container)
    elif container == 'BehavioralTimeSeries':
        return BehavioralTimeSeriesAdapter(pipeline, container)
    elif container == 'ImageSegmentation':
        return ImageSegmentationAdapter(pipeline, container)
    elif container == 'PupilTracking':
        return PupilTrackingAdapter(pipeline, container)
    elif container == 'EyeTracking':
        return EyeTrackingAdapter(pipeline, container)
