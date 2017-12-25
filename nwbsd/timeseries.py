import abc
import six


@six.add_metaclass(abc.ABCMeta)
class AbstractContainer(object):

    def __init__(self, pipeline, container):
        self.pipeline = pipeline
        self.container = self.pipeline.get_container(container)

    @abc.abstractmethod
    def getTimeSeries(self):
        pass


class BehavioralTimeSeriesAdapter(AbstractContainer):
    def getTimeSeries(self):
        fields = self.container.fields
        return [fields['time_series'].name]


class DfOverFAdapter(AbstractContainer):
    def getTimeSeries(self):
        fields = self.container.fields
        return [i.name for i in fields['roi_response_series']]


class EyeTrackingAdapter(AbstractContainer):
    def getTimeSeries(self):
        fields = self.container.fields
        return [i.name for i in fields['spatial_series']]


class FluorescenceAdapter(AbstractContainer):
    def getTimeSeries(self):
        fields = self.container.fields
        return [i.name for i in fields['roi_response_series']]


class ImageSegmentationAdapter(AbstractContainer):
    def getTimeSeries(self):
        fields = self.container.fields
        return [i.name for i in fields['plane_segmentations']]


class MotionCorrectionAdapter(AbstractContainer):
    def getTimeSeries(self):
        fields = self.container.fields
        return [i.name for i in fields['corrected_image_stacks']]


class PupilTrackingAdapter(AbstractContainer):
    def getTimeSeries(self):
        fields = self.container.fields
        return [fields['time_series'].name]


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
