import datetime
from nwbsd.slicerdicer import NwbSd
import pynwb
import pytest
import os


def _compareLists(list1, list2):
    assert len(list1) == len(list2)
    assert sorted(list1) == sorted(list2)


@pytest.fixture(scope="module")
def nwbSd():
    return NwbSd(os.path.join('tests', '570014520.nwb'))


def test_nwbsd_constructor(nwbSd):
    assert isinstance(nwbSd.nwb, pynwb.file.NWBFile) is True


def test_nwbsd_tree(nwbSd):
    tree = nwbSd.tree.to_dict()
    modules = [i for i in tree['/']['children'] if not isinstance(i, dict)]
    expected = ['analysis', 'epochs', 'file_create_date', 'identifier',
                'nwb_version', 'session_description', 'session_start_time']
    _compareLists(modules, expected)


def test_stimulus_list(nwbSd):
    stimuli = nwbSd.getStimuli()
    expected = ['natural_movie_one_stimulus', 'natural_scenes_stimulus',
                'spontaneous_stimulus', 'static_gratings_stimulus']

    _compareLists(stimuli, expected)


def test_container_list(nwbSd):
    containers = nwbSd.getContainers()
    expected = ['BehavioralTimeSeries', 'DfOverF', 'EyeTracking',
                'Fluorescence', 'ImageSegmentation', 'MotionCorrection',
                'PupilTracking']

    _compareLists(containers, expected)


def test_session_start_time(nwbSd):
    startTime = nwbSd.getSessionStartTime()
    expected = datetime.datetime(2017, 2, 16, 16, 0, 7)

    assert isinstance(startTime, datetime.datetime) is True
    assert startTime == expected


@pytest.mark.parametrize('stimulus, length', [
    ('natural_movie_one_stimulus', 9000),
    ('natural_scenes_stimulus', 5950),
    ('spontaneous_stimulus', 2),
    ('static_gratings_stimulus', 6000)
])
def test_get_stimulus_timestamps(nwbSd, stimulus, length):
    timeStamp = nwbSd.getStimulusTimeStamps(stimulus)
    assert len(timeStamp) == length


@pytest.mark.parametrize('stimulus, length', [
    ('natural_movie_one_stimulus', 9000),
    ('natural_scenes_stimulus', 5950),
    ('spontaneous_stimulus', 2),
    ('static_gratings_stimulus', 6000)
])
def test_get_stimulus_data_length(nwbSd, stimulus, length):
    assert len(nwbSd.nwb.get_stimulus(stimulus).data.value) == length


@pytest.mark.parametrize('stimulus, index, shape', [
    ('natural_movie_one_stimulus', 3000, (1, 304, 608)),
    ('natural_scenes_stimulus', 2000, (1, 918, 1174)),
    ('spontaneous_stimulus', 1, (1,)),
    ('static_gratings_stimulus', 2500, (1, 3))
])
def test_get_stimulus_data_shape(nwbSd, stimulus, index, shape):
    timeStamp = nwbSd.getStimulusTimeStamps(stimulus)[index]
    data = nwbSd.getStimulusData(stimulus, timeStamp)
    assert data.shape == shape


@pytest.mark.parametrize('container, timeSeries', [
    ('BehavioralTimeSeries', ['running_speed']),
    ('DfOverF', ['imaging_plane_1']),
    ('EyeTracking', ['pupil_location', 'pupil_location_spherical']),
    ('Fluorescence', [
        'imaging_plane_1',
        'imaging_plane_1_demixed_signal',
        'imaging_plane_1_neuropil_response'
    ]),
    ('ImageSegmentation', ['imaging_plane_1']),
    ('MotionCorrection', ['2p_image_series']),
    ('PupilTracking', ['pupil_size'])
])
def test_get_timeseries_from_container(nwbSd, container, timeSeries):
    series = nwbSd.getTimeSeries(container)
    _compareLists(series, timeSeries)


@pytest.mark.parametrize('container, timeSeries, length', [
    ('BehavioralTimeSeries', 'running_speed', 113654),
    ('DfOverF', 'imaging_plane_1', 113820),
    ('EyeTracking', 'pupil_location', 113820),
    ('EyeTracking', 'pupil_location_spherical', 113820),
    ('Fluorescence', 'imaging_plane_1', 113820),
    ('Fluorescence', 'imaging_plane_1_demixed_signal', 113820),
    ('Fluorescence', 'imaging_plane_1_neuropil_response', 113820),
    ('ImageSegmentation', 'imaging_plane_1', None),
    ('MotionCorrection', '2p_image_series', 113820),
    ('PupilTracking', 'pupil_size', 113820)
])
def test_get_timestamps_from_timeseries(nwbSd, container, timeSeries, length):
    timeStamps = nwbSd.getTimeSeriesTimeStamps(container, timeSeries)
    if length is not None:
        assert len(timeStamps) == length
    else:
        assert timeStamps is None
